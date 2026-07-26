#!/usr/bin/env bash
# run_d1_sweep.sh — n-convergence sweep for the scheme-consistent d1 self-energy
# (ca_lpt_selfenergy: lattice Abbott = exact symmetric + DERIVED gauge-fixing vertex).
#
# Reads the transverse finite constant C and the implied Lambda-ratio for BOTH the
# Wilson and the (tadpole-free) rule kernels at increasing even n, so the digit can
# be read from the n->inf trend.  n>=8 exceeds the 45 s sandbox cap, so this is a
# NATIVE job (n=8 ~40 s/Q/kernel; n=12 a few min; n=16 ~10 min).
#
# Usage:  bash tests/runners/run_d1_sweep.sh              # n = 8 12 16
#         N="8 12" bash tests/runners/run_d1_sweep.sh     # lighter
#         SMOKE=1 bash tests/runners/run_d1_sweep.sh      # n=6 sanity, separate file

set -euo pipefail
cd "$(dirname "$0")/../.."

if [[ "${SMOKE:-0}" == "1" ]]; then
  python3 tests/runners/run_d1_selfenergy.py --n 6 --Q 0.15 0.25 \
      --out test-results/d1_selfenergy_smoke.json
  exit 0
fi

NS="${N:-8 12 16}"
OUT="${OUT:-test-results/d1_selfenergy_sweep.json}"

# EVEN n only (odd n places a grid point on k=0). Small Q for the flatness read.
python3 tests/runners/run_d1_selfenergy.py \
    --n ${NS} \
    --Q 0.1 0.15 0.2 0.3 \
    --out "${OUT}"

echo "wrote ${OUT}"
