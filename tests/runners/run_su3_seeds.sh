#!/usr/bin/env bash
# run_su3_seeds.sh — extra-seed SU(3) static-potential runs for error bars on σ
# (and a cleaner α_V short-distance fit) at β=9 and β=12.
#
# Companion to run_su3_3d_string_tension.py. The seed=1 runs already exist
# (su3_static_potential_b{9,12}.json); this adds seeds 2,3,4 at each β so the
# A-NP leg (F155 §5) has statistics. Each run is ~3.5 h native — the script
# runs them SEQUENTIALLY and logs to test-results/logs/.
#
# Usage (from repo root):
#   bash tests/runners/run_su3_seeds.sh                # seeds 2 3 4 at β=9 and β=12
#   SEEDS="2 3" BETAS="9.0 12.0" bash tests/runners/run_su3_seeds.sh
#   BETAS="18.0" SEEDS="1 2 3" bash tests/runners/run_su3_seeds.sh   # wider-β lever
#
# Resumable: a run whose output JSON already exists is skipped, so you can
# Ctrl-C and re-launch without redoing finished seeds.

set -u
cd "$(dirname "$0")/../.." || exit 1   # repo root

BETAS="${BETAS:-9.0 12.0}"
SEEDS="${SEEDS:-2 3 4}"
L="${L:-24}"
NTHERM="${NTHERM:-4000}"
NMEAS="${NMEAS:-2000}"
RMAX="${RMAX:-10}"
TMAX="${TMAX:-10}"

mkdir -p test-results/logs

for beta in $BETAS; do
  btag="$(printf '%g' "$beta")"          # 9.0 -> 9, 12.0 -> 12, 18.0 -> 18
  for seed in $SEEDS; do
    out="test-results/su3_static_potential_b${btag}_s${seed}.json"
    log="test-results/logs/su3_b${btag}_s${seed}.log"
    # skip completed runs; re-run only an explicit checkpoint partial
    # ("complete": false). Legacy files with no "complete" field count as done.
    if [ -f "$out" ] && ! grep -q '"complete": false' "$out"; then
      echo "[skip] $out already complete"
      continue
    fi
    if [ -f "$out" ]; then
      echo "[redo] $out is a partial checkpoint — re-running for full stats"
    fi
    echo "[run ] beta=$beta seed=$seed L=$L -> $out  (log: $log)"
    python3 tests/runners/run_su3_3d_string_tension.py \
        --beta "$beta" --L "$L" --ntherm "$NTHERM" --nmeas "$NMEAS" \
        --rmax "$RMAX" --tmax "$TMAX" --seed "$seed" --out "$out" \
        2>&1 | tee "$log"
  done
done

echo "[done] all requested seeds complete. Re-open Claude and say the seeds are done."
