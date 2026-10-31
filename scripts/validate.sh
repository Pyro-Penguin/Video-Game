#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

run_check() {
    local label="$1"
    shift
    printf '\n==> %s\n' "$label"
    "$@"
}

run_check "Shared damage candidate tests" bash -c 'cd experiments/common && python3 -m unittest -v'
run_check "Damage RNG tests" bash -c 'cd experiments/damage_rng && python3 -m unittest -v'
run_check "Damage equation tests" bash -c 'cd experiments/damage_equation && python3 -m unittest -v'
run_check "Stat-range sensitivity tests" bash -c 'cd experiments/stat_range_sensitivity && python3 -m unittest -v'
run_check "Battle simulation tests" bash -c 'cd experiments/battle_sim && python3 -m unittest -v'
run_check "Documentation validator tests" bash -c 'cd tools && python3 -m unittest -v test_validate_docs.py'
run_check "Documentation validation" python3 tools/validate_docs.py

printf '\nAll local validation checks passed.\n'
