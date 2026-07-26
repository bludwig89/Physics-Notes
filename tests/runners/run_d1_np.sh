#!/usr/bin/env bash
# run_d1_np.sh — execute the d1 non-perturbative (static-potential) pin.
#
# WHY these parameters (diagnosis of the existing test-results/d1_static_potential.json):
#   The prior run used L=10, beta in {5.8,6.0,6.2} and landed at
#   Lambda_MSbar/sqrt(sigma) = 0.320 vs world ~0.55, routes 1 & 2 disagreeing ~33%.
#   That is BELOW the 4D pure-gauge scaling window and finite-volume-limited:
#     - L=10 is too small: at beta=6.2, sqrt(sigma) a = 0.162 => the box is only
#       ~1.6/sqrt(sigma) across, so the Cornell fit's Coulomb arm is unresolved and
#       the string tension is contaminated by finite-V.
#     - beta<=6.2 is at the low edge; asymptotic scaling (route 1) needs weaker
#       coupling, but beta too high shrinks sqrt(sigma) a below what a small L can hold.
#   Fix: push L up (16 -> 20) so a larger physical box resolves BOTH the short-range
#   Coulomb (alpha_V) and the linear term (sigma) at the SAME beta, add a 4th beta to
#   see the scaling plateau, and raise statistics + fit window (rmax, tmax).
#
# COST: each beta is a full MC, ~(L/10)^3 x (nmeas/400) x the prior ~45 min/beta.
#   L=16 -> ~4x, L=20 -> ~8x per beta. This is a NATIVE, multi-hour job; do NOT run
#   it inside the 45 s sandbox. Output goes to a NEW file so it never clobbers the
#   existing results.
#
# Usage:  bash tests/runners/run_d1_np.sh            # full production sweep (L=18)
#         L=16 bash tests/runners/run_d1_np.sh       # lighter, faster
#         SMOKE=1 bash tests/runners/run_d1_np.sh    # ~1 min sanity, separate out file

set -euo pipefail
cd "$(dirname "$0")/../.."

L="${L:-18}"
OUT="${OUT:-test-results/d1_static_potential_L${L}.json}"

if [[ "${SMOKE:-0}" == "1" ]]; then
  python3 tests/runners/run_d1_static_potential.py \
      --beta 6.0 6.2 --L 8 --ntherm 60 --nmeas 80 --meas_every 4 \
      --rmax 4 --tmax 5 --seed 1 \
      --out test-results/d1_static_potential_smoke.json
  exit 0
fi

# Production sweep: 4 betas spanning the scaling window, larger L, more stats,
# wider Cornell fit window. Writes to a dedicated L-tagged file.
python3 tests/runners/run_d1_static_potential.py \
    --beta 5.9 6.1 6.3 6.5 \
    --L "${L}" \
    --ntherm 600 \
    --nmeas 800 \
    --meas_every 5 \
    --rmax 8 \
    --tmax 8 \
    --seed 1 \
    --out "${OUT}"

echo "wrote ${OUT}"
