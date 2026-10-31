"""Deterministic, engine-independent battle-resolution harness.

All combat values are synthetic test fixtures, not approved game rules.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable, Mapping, Optional, Tuple

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


@dataclass(frozen=True)
class BattleRules:
    """Explicit prototype assumptions; none are approved gameplay rules."""
    active_monster_slots: int = 2
    automatic_end_turn_replacement: bool = True
    replacement_order: str = "roster_order"
    victory_policy: str = "commander_defeat"
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


class BattleValidationError(ValueError):
    """Raised when setup or a complete turn command set is invalid."""


def validate_state(state: BattleState, rules: BattleRules) -> None:
    if rules.active_monster_slots < 1:
        raise BattleValidationError("active_monster_slots must be at least one")
    if rules.replacement_order != "roster_order":
        raise BattleValidationError("unsupported fixture replacement order")
    if rules.victory_policy != "commander_defeat":
        raise BattleValidationError("unsupported fixture victory policy")
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
        target = by_id.get(command.target_id)
        actor = by_id[command.actor_id]
        if target is None or target.status != ACTIVE:
            raise BattleValidationError(
                f"target {command.target_id} must be active at command lock"
            )
        if target.side_id == actor.side_id:
            raise BattleValidationError("fixture attacks must target the opposing side")
    return command_tuple


def _finish_if_commander_defeated(
    state: BattleState,
) -> Tuple[BattleState, Tuple[BattleEvent, ...]]:
    commanders = {u.side_id: u for u in state.units if u.kind == COMMANDER}
    defeated_sides = sorted(
        side_id for side_id, unit in commanders.items() if unit.status == DEFEATED
    )
    if not defeated_sides:
        return state, ()
    if len(defeated_sides) == 2:
        finished = replace(state, is_finished=True, winner_side_id=None, is_draw=True)
        return finished, (
            BattleEvent("BattleFinished", detail="draw: both commanders defeated"),
        )
    winner = next(side_id for side_id in commanders if side_id not in defeated_sides)
    finished = replace(state, is_finished=True, winner_side_id=winner, is_draw=False)
    return finished, (BattleEvent("BattleFinished", detail=f"winner:{winner}"),)


class BattleResolver:
    """Pure turn resolver. Returns a new state and never mutates its input."""

    def __init__(self, rules: BattleRules = BattleRules()) -> None:
        self._rules = rules

    def resolve_turn(
        self,
        state: BattleState,
        commands: Iterable[ActionCommand],
        moves: Mapping[str, MoveDefinition],
    ) -> TurnResult:
        validate_state(state, self._rules)
        if state.is_finished:
            raise BattleValidationError("cannot resolve a finished battle")
        _validate_moves(moves)
        locked_commands = _validate_commands(state, commands, moves)

        units = {unit.unit_id: unit for unit in state.units}
        start_units = dict(units)
        ordered = sorted(
            locked_commands,
            key=lambda command: (
                -moves[command.move_id].priority,
                -start_units[command.actor_id].speed,
                command.actor_id,
            ),
        )
        events = [BattleEvent("TurnStarted", detail=str(state.turn_number))]

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
            actual_damage = min(move.fixture_damage, target.vitality)
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
                for reserve in reserves[:vacancies]:
                    units[reserve.unit_id] = replace(reserve, status=ACTIVE)
                    events.append(BattleEvent(
                        "ReserveDeployed", target_id=reserve.unit_id, detail=side_id,
                    ))

        next_state = replace(
            state,
            units=tuple(sorted(
                units.values(),
                key=lambda unit: (unit.side_id, unit.roster_order, unit.unit_id),
            )),
            turn_number=state.turn_number + 1,
        )
        next_state, finish_events = _finish_if_commander_defeated(next_state)
        events.extend(finish_events)
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
