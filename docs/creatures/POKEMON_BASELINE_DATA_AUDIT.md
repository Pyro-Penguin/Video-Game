# Pokémon Final-Stage Baseline Data Audit

**Status:** External-data audit / research evidence only. This does not select our creature stat ranges, normalization formula, stat budget, or transformation rules.

## Purpose

Separate the stable baseline identity of final-stage creatures from temporary transformation forms, then compare the proposed synthetic endgame bands against a real creature-stat distribution. The source contains base stats for Gen I–IX and Mega Evolution name fields, but does not include transformed Mega stat lines.

## Source and reproducibility boundary

- Dataset: [cristobalmitchell/pokedex — pokemon_utf8.csv](https://raw.githubusercontent.com/cristobalmitchell/pokedex/main/data/pokemon_utf8.csv)
- Retrieved: 2026-10-30.
- Source rows: 1,025; unique national-number rows: 1,025.
- The CSV is a third-party community dataset, not an official authoritative game-data export. Treat it as a comparative sample, not a canonical rules source.
- Final-stage identification: for each row, read the populated species slots in `evochain_0`, `evochain_2`, `evochain_4`, and `evochain_6`; include the row when its English name matches the last populated species slot.
- Ordinary final-stage cohort: exclude rows flagged sublegendary, legendary, or mythical. This is a useful working cohort, not a perfect taxonomy of competitive eligibility.
- Type summaries use **primary type only**. Dual types are not counted twice.
- Mega-capable base species remain in the baseline cohort. The dataset's Mega columns identify transformation names, not transformed stat values; no Mega stats are synthesized here.
- Alternate forms and regional forms may be represented as separate rows. This can affect cohort counts and means.

## Cohort summary

| Cohort | Entries | Mean BST | Median BST | 75th percentile | 90th percentile |
|---|---:|---:|---:|---:|---:|
| All identified final-stage entries | 546 | 509.2 | 500 | 540 | 600 |
| Excluding sublegendary, legendary, mythical | 456 | 491.2 | 494 | 520 | 540 |

The user's cited approximate final-evolution mean of 507 is close to the all-final-stage mean in this dataset (509.2), but the ordinary non-legendary cohort is lower (491.2). Cohort definitions matter: inclusion of legendary/sublegendary/mythical entries materially changes the result. The supplied summary's Gen VIII and type-specific figures should not be treated as directly replicated by this Gen I–IX dataset.

## Ordinary final-stage base-stat distribution

| Base stat | Mean | Median | 75th percentile | 90th percentile |
|---|---:|---:|---:|---:|
| HP | 81.3 | 76 | 84 | 109 |
| Attack | 90.2 | 90 | 100 | 125 |
| Defense | 83.2 | 79 | 93 | 119 |
| Special Attack | 79.5 | 80 | 98 | 115 |
| Special Defense | 81.2 | 80 | 95 | 110 |
| Speed | 75.8 | 75 | 95 | 111 |

## Level-100 comparison transform

To compare with the earlier synthetic stat bands, apply the experiment's simplified transform:

- HP / Vitality: `2 × base HP + 141`
- Other stats: `2 × base stat + 36`

This deliberately omits IVs, EVs, nature, items, abilities, and other official battle modifiers. It is a scale translation only.

### Ordinary final-stage derived stats (n=456)

| Derived stat | Median | 75th percentile | 90th percentile | Observed max |
|---|---:|---:|---:|---:|
| Vitality (HP transform) | 293 | 321 | 359 | 651 |
| Attack | 216 | 256 | 286 | 366 |
| Defense | 194 | 226 | 274 | 496 |
| Special Attack | 196 | 232 | 266 | 326 |
| Special Defense | 196 | 226 | 256 | 496 |
| Speed | 186 | 226 | 258 | 336 |

Observed maxima are outlier checks, not recommended caps. For example, very high HP/Defense values can belong to exceptional species; they should not define the center of the roster.

## Primary-type signatures among ordinary final-stage entries

Primary type only; means are base-stat values, not transformed values.

| Primary type | n | Mean BST | Mean Attack | Mean Defense |
|---|---:|---:|---:|---:|
| Dragon | 13 | 560.1 | 115.0 | 84.5 |
| Fairy | 13 | 520.4 | 80.7 | 86.9 |
| Fire | 27 | 514.2 | 94.9 | 80.7 |
| Steel | 17 | 513.8 | 96.4 | 121.7 |
| Ground | 19 | 504.5 | 107.6 | 99.9 |
| Rock | 28 | 503.6 | 99.3 | 105.9 |
| Ghost | 18 | 503.2 | 83.0 | 84.7 |
| Dark | 19 | 501.4 | 99.6 | 80.8 |
| Flying | 5 | 498.0 | 92.0 | 79.8 |
| Grass | 42 | 497.7 | 90.6 | 83.1 |
| Fighting | 22 | 496.8 | 116.6 | 81.6 |
| Poison | 18 | 495.8 | 88.2 | 83.2 |
| Ice | 13 | 493.8 | 83.1 | 81.8 |
| Water | 60 | 486.9 | 86.0 | 81.4 |
| Electric | 28 | 482.4 | 81.3 | 72.0 |
| Psychic | 20 | 472.7 | 64.8 | 69.8 |
| Normal | 57 | 461.1 | 86.1 | 69.5 |
| Bug | 37 | 457.2 | 82.5 | 82.3 |

This sample supports several broad signatures: Dragon has the highest mean BST; Steel has the highest mean Defense; Bug has the lowest mean BST. It does **not** reproduce every supplied numerical claim: Bug's mean Attack here is 82.5 rather than 90.59, and Dragon's ordinary-cohort BST mean is 560.1 rather than 540–547. Likely causes include different generation cutoffs, final-stage definitions, form handling, and legendary/sublegendary inclusion. Resolve cohort definitions before treating differences as substantive.

## Implications for our proposed synthetic bands

Earlier synthetic endgame ranges:
- Attack: 200–400
- Defense: 200–350
- Vitality: 250–500

Against the ordinary final-stage Level-100 transform:
- Attack 200–400 starts near the median (216), but its upper end exceeds the cohort's observed maximum (366).
- Defense 200–350 starts above the median (194); 350 is above the 90th percentile (274).
- Vitality 250–500 starts below the median (293); 500 is well above the 90th percentile (359), while exceptional HP outliers extend higher.

**Assessment:** These ranges are plausible as an intentionally elevated/normalized competitive roster, but they are not representative central ranges for ordinary final-stage creatures under this transform. Do not reject or approve them from this comparison alone. First clarify whether our target roster is:
1. a broad population with meaningful weak/unevolved story creatures;
2. a final-stage story roster; or
3. a normalized competitive roster where every creature is raised to a common competitive power floor.

The third model can legitimately compress species power differences and create a narrower, higher range. If that is the goal, this Pokémon audit is a role-shape reference, not a direct stat-budget target.

## Mega Evolution: separate transformation layer

The CSV identifies Mega-capable base species and their Mega names, but does not contain transformed stat lines. Therefore:
- Keep the normal species row as the baseline identity.
- Store each transformation as a separate form/configuration with its own stat deltas, typing, ability, restrictions, duration, and activation cost when authoritative data is available.
- Do not assume every transformation is a uniform +100 BST or a universal upgrade.
- Do not add HP, offensive, defensive, or speed changes based on a generalization; verify each transformation's actual stat line from a dedicated source.
- Test transformation balance as a before/after role reassignment, including stats that decrease.

The design lesson is useful even without importing Pokémon's exact rules: **baseline form defines identity; transformation is a deliberate, temporary change in role and matchup profile.**

## Recommended next work

1. Establish our target roster cohort: broad story population, final-stage story roster, or normalized competitive roster.
2. Define whether creature identity is represented by a fixed base-stat budget, role template, or both.
3. Map the user's 70-point / 30-per-stat allocation proposal onto percentile-derived baselines; keep it provisional.
4. Re-run the existing damage sensitivity harness using profiles sampled from the chosen target cohort rather than arbitrary synthetic coordinates.
5. Keep transformation data separate from species baselines and test it as a discrete configuration change.

No game rule or stat range is selected by this report.
