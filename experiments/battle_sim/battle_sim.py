"""Deterministic, engine-independent battle-resolution harness.

All combat values are synthetic test fixtures, not approved game rules.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from functools import cmp_to_key
from fractions import Fraction
from typing import Iterable, Mapping, Optional, Protocol, Tuple

ACTIVE = "active"
RESERVE = "reserve"
DEFEATED = "defeated"
COMMANDER = "commander"
MONSTER = "monster"


@dataclass(frozen=True)
class UnitState:
    unit_id: str
    side_id: str
    kind: str
    vitality: int
    max_vitality: int
    speed: int
    roster_order: int
    status: str = ACTIVE


@dataclass(frozen=True)
class BattleState:
    units: Tuple[UnitState, ...]
    turn_number: int = 1
    is_finished: bool = False
    winner_side_id: Optional[str] = None
    is_draw: bool = False


@dataclass(frozen=True)
class MoveDefinition:
    move_id: str
    fixture_damage: int
    priority: int = 0


@dataclass(frozen=True)
class ActionCommand:
    actor_id: str
    move_id: str
    target_id: str
    # Optional action-vs-target effectiveness supplied by the caller as an exact ratio.
    # None means the action has no defined effectiveness value for tie comparison.
    type_effectiveness: Optional[Tuple[int, int]] = None


@dataclass(frozen=True)
class BattleRules:
    """Explicit prototype assumptions; none are approved gameplay rules."""
    active_monster_slots: int = 2
    automatic_end_turn_replacement: bool = True
    replacement_order: str = "roster_order"
    exact_tie_break: str = "unit_id_ascending"


@dataclass(frozen=True)
class BattleEvent:
    event_type: str
    actor_id: Optional[str] = None
    target_id: Optional[str] = None
    amount: int = 0
    detail: str = ""


@dataclass(frozen=True)
class TurnResult:
    state: BattleState
    events: Tuple[BattleEvent, ...]


@dataclass(frozen=True)
class SideBattleFacts:
    side_id: str
    commander_defeated: bool
    active_monster_count: int
    reserve_monster_count: int

    @property
    def monster_team_wiped(self) -> bool:
        return self.active_monster_count + self.reserve_monster_count == 0


@dataclass(frozen=True)
class BattleFacts:
    sides: Tuple[SideBattleFacts, ...]


@dataclass(frozen=True)
class VictoryOutcome:
    is_finished: bool
    winner_side_id: Optional[str] = None
    is_draw: bool = False
    reason: str = ""


class VictoryPolicy(Protocol):
    """Pure encounter policy: classify derived battle facts, never mutate state."""

    def evaluate(self, facts: BattleFacts) -> VictoryOutcome:
        ...


@dataclass(frozen=True)
class ConfiguredVictoryPolicy:
    """Any enabled terminal condition can eliminate a side.

    Both flags enabled means commander defeat OR monster team wipe ends that
    side's encounter. Set both false to disable terminal classification.
    """

    commander_defeat: bool = True
    monster_team_wipe: bool = False

    def evaluate(self, facts: BattleFacts) -> VictoryOutcome:
        eliminated = []
        for side in facts.sides:
            reasons = []
            if self.commander_defeat and side.commander_defeated:
                reasons.append("commander_defeated")
            if self.monster_team_wipe and side.monster_team_wiped:
                reasons.append("monster_team_wiped")
            if reasons:
                eliminated.append((side.side_id, tuple(reasons)))

        if not eliminated:
            return VictoryOutcome(False)
        if len(eliminated) == len(facts.sides):
            reason = "; ".join(
                f"{side_id}:{'+'.join(reasons)}" for side_id, reasons in eliminated
            )
            return VictoryOutcome(True, None, True, f"draw:{reason}")

        eliminated_side = eliminated[0][0]
        winner = next(side.side_id for side in facts.sides if side.side_id != eliminated_side)
        reason = "+".join(eliminated[0][1])
        return VictoryOutcome(True, winner, False, f"winner:{winner};loser:{eliminated_side};reason:{reason}")


def build_battle_facts(state: BattleState) -> BattleFacts:
    side_ids = sorted({unit.side_id for unit in state.units})
    facts = []
    for side_id in side_ids:
        side_units = tuple(unit for unit in state.units if unit.side_id == side_id)
        commander = next(unit for unit in side_units if unit.kind == COMMANDER)
        facts.append(SideBattleFacts(
            side_id=side_id,
            commander_defeated=commander.status == DEFEATED,
            active_monster_count=sum(
                unit.kind == MONSTER and unit.status == ACTIVE for unit in side_units
            ),
            reserve_monster_count=sum(
                unit.kind == MONSTER and unit.status == RESERVE for unit in side_units
            ),
        ))
    return BattleFacts(tuple(facts))


class BattleValidationError(ValueError):
    """Raised when setup or a complete turn command set is invalid."""


class ReserveSelector(Protocol):
    """Pure policy seam for choosing reserves to fill end-of-turn vacancies."""

    def select_reserves(
        self,
        side_id: str,
        eligible_reserves: Tuple[UnitState, ...],
        vacancies: int,
        selections: Mapping[str, Tuple[str, ...]],
    ) -> Tuple[UnitState, ...]:
        ...


@dataclass(frozen=True)
class CommandReserveSelector:
    """Auto-select when there is no meaningful choice; otherwise require caller input."""

    def select_reserves(
        self,
        side_id: str,
        eligible_reserves: Tuple[UnitState, ...],
        vacancies: int,
        selections: Mapping[str, Tuple[str, ...]],
    ) -> Tuple[UnitState, ...]:
        if vacancies <= 0 or not eligible_reserves:
            if side_id in selections:
                raise BattleValidationError(f"unexpected reserve selection for side {side_id}")
            return ()

        if len(eligible_reserves) <= vacancies:
            if side_id in selections:
                raise BattleValidationError(f"reserve selection is unnecessary for side {side_id}")
            return eligible_reserves

        requested = selections.get(side_id)
        if requested is None:
            raise BattleValidationError(
                f"side {side_id} must select {vacancies} reserve unit(s)"
            )
        if len(requested) != vacancies or len(set(requested)) != len(requested):
            raise BattleValidationError(
                f"side {side_id} must select exactly {vacancies} unique reserve unit(s)"
            )
        eligible_by_id = {unit.unit_id: unit for unit in eligible_reserves}
        if any(unit_id not in eligible_by_id for unit_id in requested):
            raise BattleValidationError(f"side {side_id} selected an ineligible reserve")
        return tuple(eligible_by_id[unit_id] for unit_id in requested)


class DamageModel(Protocol):
    """Pure damage seam; production formula and rounding are intentionally absent."""

    def calculate_damage(
        self, actor: UnitState, target: UnitState, move: MoveDefinition
    ) -> int:
        ...


@dataclass(frozen=True)
class FixedDamageFixture:
    """Returns synthetic fixed damage stored on each fixture move."""

    def calculate_damage(
        self, actor: UnitState, target: UnitState, move: MoveDefinition
    ) -> int:
        return move.fixture_damage


def validate_state(state: BattleState, rules: BattleRules) -> None:
    if rules.active_monster_slots < 1:
        raise BattleValidationError("active_monster_slots must be at least one")
    if rules.replacement_order != "roster_order":
        raise BattleValidationError("unsupported fixture replacement order")
    if rules.exact_tie_break != "unit_id_ascending":
        raise BattleValidationError("unsupported fixture tie-break policy")

    ids = set()
    sides = set()
    commanders = {}
    for unit in state.units:
        if not unit.unit_id or unit.unit_id in ids:
            raise BattleValidationError("unit IDs must be non-empty and unique")
        ids.add(unit.unit_id)
        sides.add(unit.side_id)
        if unit.kind not in (COMMANDER, MONSTER):
            raise BattleValidationError(f"unsupported unit kind: {unit.kind}")
        if unit.status not in (ACTIVE, RESERVE, DEFEATED):
            raise BattleValidationError(f"unsupported unit status: {unit.status}")
        if unit.max_vitality <= 0 or not 0 <= unit.vitality <= unit.max_vitality:
            raise BattleValidationError(f"invalid vitality for {unit.unit_id}")
        if unit.status == DEFEATED and unit.vitality != 0:
            raise BattleValidationError(f"defeated unit {unit.unit_id} must have zero vitality")
        if unit.status != DEFEATED and unit.vitality == 0:
            raise BattleValidationError(f"living unit {unit.unit_id} must have positive vitality")
        if unit.kind == COMMANDER:
            if unit.side_id in commanders:
                raise BattleValidationError(f"side {unit.side_id} has multiple commanders")
            commanders[unit.side_id] = unit.unit_id

    if len(sides) != 2:
        raise BattleValidationError("a battle requires exactly two sides")
    if set(commanders) != sides:
        raise BattleValidationError("each side requires exactly one commander")
    for side_id in sides:
        commander = next(u for u in state.units if u.unit_id == commanders[side_id])
        if commander.status == RESERVE:
            raise BattleValidationError("a commander cannot be in reserve")


def _validate_moves(moves: Mapping[str, MoveDefinition]) -> None:
    for key, move in moves.items():
        if key != move.move_id or not key:
            raise BattleValidationError("move mapping keys must match non-empty move IDs")
        if move.fixture_damage <= 0:
            raise BattleValidationError(f"fixture damage for {key} must be positive")


def _compare_action_commands(
    left: ActionCommand,
    right: ActionCommand,
    moves: Mapping[str, MoveDefinition],
    start_units: Mapping[str, UnitState],
) -> int:
    """Sort higher-priority actions first; exact Speed ties follow D-021.

    Undefined or equal effectiveness advances to the next criterion. The final
    unit-ID comparison is a deterministic fixture fallback only.
    """
    left_move, right_move = moves[left.move_id], moves[right.move_id]
    if left_move.priority != right_move.priority:
        return -1 if left_move.priority > right_move.priority else 1
    left_actor, right_actor = start_units[left.actor_id], start_units[right.actor_id]
    if left_actor.speed != right_actor.speed:
        return -1 if left_actor.speed > right_actor.speed else 1

    if left.type_effectiveness is not None and right.type_effectiveness is not None:
        left_effect = Fraction(*left.type_effectiveness)
        right_effect = Fraction(*right.type_effectiveness)
        if left_effect != right_effect:
            return -1 if left_effect > right_effect else 1

    # Compare HP percentages exactly; avoid floating-point rounding.
    hp_cross_left = left_actor.vitality * right_actor.max_vitality
    hp_cross_right = right_actor.vitality * left_actor.max_vitality
    if hp_cross_left != hp_cross_right:
        return -1 if hp_cross_left > hp_cross_right else 1
    if left_actor.vitality != right_actor.vitality:
        return -1 if left_actor.vitality > right_actor.vitality else 1
    if left_actor.max_vitality != right_actor.max_vitality:
        return -1 if left_actor.max_vitality > right_actor.max_vitality else 1
    return -1 if left.actor_id < right.actor_id else (1 if left.actor_id > right.actor_id else 0)


def _validate_commands(
    state: BattleState,
    commands: Iterable[ActionCommand],
    moves: Mapping[str, MoveDefinition],
) -> Tuple[ActionCommand, ...]:
    command_tuple = tuple(commands)
    active_ids = {u.unit_id for u in state.units if u.status == ACTIVE}
    by_id = {u.unit_id: u for u in state.units}
    command_ids = [c.actor_id for c in command_tuple]
    if len(command_ids) != len(set(command_ids)):
        raise BattleValidationError("an actor may submit only one command")
    if set(command_ids) != active_ids:
        missing = sorted(active_ids - set(command_ids))
        extra = sorted(set(command_ids) - active_ids)
        raise BattleValidationError(
            f"commands must cover every active unit; missing={missing}, extra={extra}"
        )
    for command in command_tuple:
        if command.move_id not in moves:
            raise BattleValidationError(f"unknown move: {command.move_id}")
        if command.type_effectiveness is not None:
            numerator, denominator = command.type_effectiveness
            if numerator <= 0 or denominator <= 0:
                raise BattleValidationError("type effectiveness ratio must be positive")
        target = by_id.get(command.target_id)
        actor = by_id[command.actor_id]
        if target is None or target.status != ACTIVE:
            raise BattleValidationError(
                f"target {command.target_id} must be active at command lock"
            )
        if target.side_id == actor.side_id:
            raise BattleValidationError("fixture attacks must target the opposing side")
    return command_tuple


def _apply_victory_policy(
    state: BattleState,
    policy: VictoryPolicy,
) -> Tuple[BattleState, Tuple[BattleEvent, ...]]:
    outcome = policy.evaluate(build_battle_facts(state))
    if not outcome.is_finished:
        return state, ()
    finished = replace(
        state,
        is_finished=True,
        winner_side_id=outcome.winner_side_id,
        is_draw=outcome.is_draw,
    )
    return finished, (BattleEvent("BattleFinished", detail=outcome.reason),)


def _finish_if_commander_defeated(
    state: BattleState,
) -> Tuple[BattleState, Tuple[BattleEvent, ...]]:
    """Compatibility helper for tests of the default fixture policy."""
    return _apply_victory_policy(state, ConfiguredVictoryPolicy(commander_defeat=True))


class BattleResolver:
    """Pure turn resolver. Returns a new state and never mutates its input."""

    def __init__(
        self,
        rules: BattleRules = BattleRules(),
        damage_model: Optional[DamageModel] = None,
        reserve_selector: Optional[ReserveSelector] = None,
        victory_policy: Optional[VictoryPolicy] = None,
    ) -> None:
        self._rules = rules
        self._damage_model = damage_model if damage_model is not None else FixedDamageFixture()
        self._reserve_selector = reserve_selector if reserve_selector is not None else CommandReserveSelector()
        self._victory_policy = victory_policy if victory_policy is not None else ConfiguredVictoryPolicy()

    def resolve_turn(
        self,
        state: BattleState,
        commands: Iterable[ActionCommand],
        moves: Mapping[str, MoveDefinition],
        reserve_selections: Optional[Mapping[str, Tuple[str, ...]]] = None,
    ) -> TurnResult:
        validate_state(state, self._rules)
        if state.is_finished:
            raise BattleValidationError("cannot resolve a finished battle")
        _validate_moves(moves)
        locked_commands = _validate_commands(state, commands, moves)
        selections = {} if reserve_selections is None else dict(reserve_selections)
        side_ids = {unit.side_id for unit in state.units}
        unknown_sides = set(selections) - side_ids
        if unknown_sides:
            raise BattleValidationError(
                f"reserve selections supplied for unknown side(s): {sorted(unknown_sides)}"
            )
        if selections and not self._rules.automatic_end_turn_replacement:
            raise BattleValidationError("reserve selections are not valid when replacement is disabled")

        units = {unit.unit_id: unit for unit in state.units}
        start_units = dict(units)
        ordered = sorted(
            locked_commands,
            key=cmp_to_key(lambda left, right: _compare_action_commands(
                left, right, moves, start_units
            )),
        )
        events = [BattleEvent("TurnStarted", detail=str(state.turn_number))]
        events.append(BattleEvent("PhaseStarted", detail="action_resolution"))

        for command in ordered:
            actor = units[command.actor_id]
            target = units[command.target_id]
            if actor.status != ACTIVE:
                events.append(BattleEvent(
                    "ActionSkipped", actor_id=actor.unit_id, target_id=target.unit_id,
                    detail="actor_defeated_before_resolution",
                ))
                continue
            if target.status != ACTIVE:
                events.append(BattleEvent(
                    "ActionSkipped", actor_id=actor.unit_id, target_id=target.unit_id,
                    detail="target_not_active_at_resolution",
                ))
                continue

            move = moves[command.move_id]
            calculated_damage = self._damage_model.calculate_damage(actor, target, move)
            if not isinstance(calculated_damage, int) or calculated_damage <= 0:
                raise BattleValidationError("damage model must return a positive integer")
            actual_damage = min(calculated_damage, target.vitality)
            remaining = target.vitality - actual_damage
            units[target.unit_id] = replace(
                target,
                vitality=remaining,
                status=DEFEATED if remaining == 0 else ACTIVE,
            )
            events.append(BattleEvent(
                "DamageApplied", actor_id=actor.unit_id, target_id=target.unit_id,
                amount=actual_damage, detail=command.move_id,
            ))
            if remaining == 0:
                events.append(BattleEvent(
                    "UnitDefeated", actor_id=actor.unit_id, target_id=target.unit_id,
                ))

        events.append(BattleEvent("PhaseCompleted", detail="action_resolution"))
        events.append(BattleEvent("PhaseStarted", detail="end_of_turn_replacement"))
        if self._rules.automatic_end_turn_replacement:
            for side_id in sorted({unit.side_id for unit in units.values()}):
                active_count = sum(
                    unit.side_id == side_id and unit.kind == MONSTER and unit.status == ACTIVE
                    for unit in units.values()
                )
                vacancies = max(0, self._rules.active_monster_slots - active_count)
                reserves = sorted(
                    (
                        unit for unit in units.values()
                        if unit.side_id == side_id and unit.kind == MONSTER
                        and unit.status == RESERVE
                    ),
                    key=lambda unit: (unit.roster_order, unit.unit_id),
                )
                selected_reserves = self._reserve_selector.select_reserves(
                    side_id, tuple(reserves), vacancies, selections
                )
                for reserve in selected_reserves:
                    units[reserve.unit_id] = replace(reserve, status=ACTIVE)
                    events.append(BattleEvent(
                        "ReserveDeployed", target_id=reserve.unit_id, detail=side_id,
                    ))
        events.append(BattleEvent("PhaseCompleted", detail="end_of_turn_replacement"))
        events.append(BattleEvent("PhaseStarted", detail="victory_check"))
        next_state = replace(
            state,
            units=tuple(sorted(
                units.values(),
                key=lambda unit: (unit.side_id, unit.roster_order, unit.unit_id),
            )),
            turn_number=state.turn_number + 1,
        )
        next_state, finish_events = _apply_victory_policy(next_state, self._victory_policy)
        events.extend(finish_events)
        events.append(BattleEvent("PhaseCompleted", detail="victory_check"))
        if not next_state.is_finished:
            events.append(BattleEvent("TurnCompleted", detail=str(state.turn_number)))
        return TurnResult(next_state, tuple(events))


def make_test_battle() -> BattleState:
    """Synthetic fixture: commander + two active monsters + one reserve per side."""
    units = (
        UnitState("A-C", "A", COMMANDER, 120, 120, 80, 0),
        UnitState("A-M1", "A", MONSTER, 100, 100, 70, 1),
        UnitState("A-M2", "A", MONSTER, 100, 100, 60, 2),
        UnitState("A-R1", "A", MONSTER, 100, 100, 50, 3, RESERVE),
        UnitState("B-C", "B", COMMANDER, 120, 120, 75, 0),
        UnitState("B-M1", "B", MONSTER, 100, 100, 65, 1),
        UnitState("B-M2", "B", MONSTER, 100, 100, 55, 2),
        UnitState("B-R1", "B", MONSTER, 100, 100, 45, 3, RESERVE),
    )
    state = BattleState(units)
    validate_state(state, BattleRules())
    return state


def make_test_moves() -> Mapping[str, MoveDefinition]:
    return {
        "strike": MoveDefinition("strike", fixture_damage=40, priority=0),
        "quick_strike": MoveDefinition("quick_strike", fixture_damage=25, priority=1),
        "finisher": MoveDefinition("finisher", fixture_damage=100, priority=0),
    }
