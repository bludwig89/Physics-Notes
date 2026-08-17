#!/usr/bin/env bash
# =====================================================================
# audit_v_battery.sh — Physics Audit V, Tier-B handoff
#
#   Written 2026-08-01 by the audit session (claim `audit-v`).
#   Companion manifest: test-results/audit-v/MANIFEST.md
#   Report:             docs/audits/physics-audit-report-2026-08-01.md
#
# WHAT THIS IS.  Everything Audit V could NOT run in the sandbox, because a
# single bash call there is killed at ~45 s.  Each item writes one JSON into
# test-results/audit-v/ so the next session can complete the report by reading
# files rather than re-deriving the plan.
#
# HOW IT BEHAVES.
#   * Resumable — an item whose JSON already exists is skipped.  Delete the JSON
#     (or pass --force) to re-run one.
#   * Journalled — every item appends a verdict line to the journal, so a run
#     that dies halfway still says what it established.
#   * Non-destructive by default — the two items that would rewrite committed
#     baselines are OFF unless you pass --arm, and they --restore first.
#
# USAGE
#   bash tools/audit_v_battery.sh                 # everything safe, resumable
#   bash tools/audit_v_battery.sh --only B3       # one item
#   bash tools/audit_v_battery.sh --arm           # include the baseline re-runs
#   bash tools/audit_v_battery.sh --force         # ignore existing JSONs
#
# ESTIMATED WALL TIME: ~3.5 h without --arm, ~6 h with (see MANIFEST.md).
# =====================================================================
set -uo pipefail

# --- preamble (exactly as CLAUDE.md specifies) -----------------------
cd "$(dirname "$0")/.." || exit 1
REPO="$PWD"
# shellcheck source=/dev/null
source "$REPO/.vendor/activate.sh"          # no download; CPython 3.10 linux-aarch64
export PYTHONPATH="$REPO/src:${PYTHONPATH:-}"
PY=python3                                  # NEVER bare `pytest` — always `python3 -m pytest`

OUT="$REPO/test-results/audit-v"
LOGS="$OUT/logs"
JOURNAL="$OUT/battery-journal.txt"
mkdir -p "$OUT" "$LOGS"

ONLY=""; ARM=0; FORCE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --only) ONLY="$2"; shift 2 ;;
    --arm)  ARM=1; shift ;;
    --force) FORCE=1; shift ;;
    *) echo "unknown flag: $1"; exit 2 ;;
  esac
done

stamp() { date "+%Y-%m-%d - %H:%M"; }
note()  { printf '%s  %s\n' "$(stamp)" "$*" | tee -a "$JOURNAL"; }

# run_item <id> <json-name> <estimated-minutes> <command...>
run_item() {
  local id="$1" json="$2" est="$3"; shift 3
  [ -n "$ONLY" ] && [ "$ONLY" != "$id" ] && return 0
  local target="$OUT/$json"
  if [ -f "$target" ] && [ "$FORCE" -eq 0 ]; then
    note "SKIP  $id — $json exists (delete it or pass --force to re-run)"; return 0
  fi
  note "START $id  (est ${est} min)  -> $json"
  local t0 rc; t0=$(date +%s)
  ( "$@" ) > "$LOGS/$id.log" 2>&1; rc=$?
  local dt=$(( ($(date +%s) - t0) / 60 ))
  if [ $rc -eq 0 ]; then note "OK    $id  (${dt} min)"; else note "FAIL  $id  rc=$rc  (${dt} min) — see logs/$id.log"; fi
  return 0
}

note "=== Audit V Tier-B battery, run started ==="
note "repo=$REPO  arm=$ARM  force=$FORCE  only=${ONLY:-<all>}"

# =====================================================================
# B1 — the full grouped battery.  Hours, not minutes.
# =====================================================================
run_item B1 B1_full_smoke_battery.json 150 \
  $PY -m casim.cli test --scale smoke --json "$OUT/B1_full_smoke_battery.json"

# =====================================================================
# B2 — gauge_mc at production L.  The one channel the sandbox cannot size.
# =====================================================================
run_item B2 B2_gauge_mc_production.json 60 \
  $PY -m casim.cli test --sector gauge --kind result_dump --json "$OUT/B2_gauge_mc_production.json"

# =====================================================================
# B3 — V2.4 doublers at L=96 and 128.  Cheap; the sandbox stopped at 64.
# =====================================================================
run_item B3 B3_doublers_large_L.json 10 $PY - <<'PYEOF'
import json, numpy as np, os
from casim.engine.lattice.bcc import bcc_dispersion
out = {}
for L in (64, 96, 128):
    n = np.arange(L); K = 2*np.pi*(n - L//2)/L
    KX, KY, KZ = np.meshgrid(K, K, K, indexing='ij')
    per = {}
    for s in '+-':
        w = bcc_dispersion(KX, KY, KZ, sign=s)
        z = np.argwhere(np.isclose(w, 0.0, atol=1e-9))
        p = np.argwhere(np.isclose(w, np.pi, atol=1e-9))
        per[s] = {"n_zero": int(len(z)), "n_pi": int(len(p)),
                  "zero_at_origin": bool(len(z) == 1 and (z[0] == L//2).all()),
                  "omega_max": float(w.max())}
    out[f"L={L}"] = per
out["verdict"] = ("no doubler at any L" if all(v[s]["n_zero"] == 1 and v[s]["n_pi"] == 0
                  for v in out.values() if isinstance(v, dict) for s in '+-')
                  else "ESCALATE — a doubler appeared")
json.dump(out, open(os.environ["OUT"] + "/B3_doublers_large_L.json", "w"), indent=1)
print(json.dumps(out, indent=1))
PYEOF

# =====================================================================
# B4 — V4.3, THE DECISIVE TEST.  Highest-value item in this file.
#      Rebuild the walk on an EXPLICIT two-sublattice BCC site set with
#      integer np.roll hops (no fractional shift), so momentum space
#      genuinely tiles the truncated octahedron, then measure <cot w>.
#        cube value (~0.221) -> Reading 1 ; exactly 0 -> Reading 2.
#      NOT IMPLEMENTED HERE ON PURPOSE: this is physics and needs a
#      deliberate construction, not a script the audit wrote in passing.
#      See MANIFEST.md §B4 for the specification.
# =====================================================================
if [ -z "$ONLY" ] || [ "$ONLY" = "B4" ]; then
  note "TODO  B4 — the explicit-BCC-crystal <cot w> discriminator is SPECIFIED, not written."
  note "      See test-results/audit-v/MANIFEST.md section B4. It is the one experiment"
  note "      that settles Reading 1 vs Reading 2, and it should be built deliberately."
fi

# =====================================================================
# B5 — V-023.  Quantify the three live F272 refold sites WITHOUT fixing
#      them: measure each with and without the wrap, over a grid refinement.
# =====================================================================
run_item B5 B5_refold_defect_quantified.json 20 $PY - <<'PYEOF'
import json, os, math, numpy as np, inspect, re
from casim.engine.interactions import qed_vacuum_polarization as VP
from casim.engine.interactions import qed_electron_self_energy as SE
out = {"about": "V-023: the % 2pi refold on a kernel whose period lattice is sqrt3.fcc"}
# kernel periodicity
rng = np.random.default_rng(0); k = rng.uniform(-2, 2, size=(4, 300))
out["kernel_periodicity_2pi"] = {
    "qed_K_lat": float(np.abs(VP._K_lat(k[0]+2*math.pi, k[1], k[2], k[3]) - VP._K_lat(*k)).max()),
}
# vacuum polarization, shipped vs un-refolded
src = inspect.getsource(VP._fermion_B)
patched = src.replace("kxpw = ((KX + Q + math.pi) % (2 * math.pi)) - math.pi",
                      "kxpw = KX + Q")
ns = {}
exec(patched, {"math": math, "np": np, "_K_lat": VP._K_lat}, ns)
fb = ns["_fermion_B"]
rows = []
for n in (10, 14, 18, 22, 26, 30):
    c = VP._fermion_B(0.3, n, 'cont')
    rows.append({"n": n, "shipped": VP._fermion_B(0.3, n, 'rule') - c,
                 "no_refold": fb(0.3, n, 'rule') - c})
out["vacuum_polarization_Q0.3"] = rows
out["self_energy_P0.2"] = [
    {"n": n,
     "dA": SE._selfenergy_AB(0.2, n, 'rule')[0] - SE._selfenergy_AB(0.2, n, 'cont')[0],
     "dB": SE._selfenergy_AB(0.2, n, 'rule')[1] - SE._selfenergy_AB(0.2, n, 'cont')[1]}
    for n in (10, 14, 18, 22, 26)]
json.dump(out, open(os.environ["OUT"] + "/B5_refold_defect_quantified.json", "w"), indent=1)
print(json.dumps(out, indent=1))
PYEOF

# =====================================================================
# B6 — V6.4's open half: SU(3) Gauss law, and a live three-sector run.
# =====================================================================
run_item B6 B6_su3_gauss_and_three_sector.json 45 \
  $PY -m casim.cli run scenarios/unified_hydrogen.yaml --json "$OUT/B6_su3_gauss_and_three_sector.json"

# =====================================================================
# B7 — the 55 F270-affected dumps.  DESTRUCTIVE: rewrites committed
#      baselines.  Off unless --arm.  ORDER IS ALWAYS run -> --restore
#      -> --apply (trap #3; forgetting --restore has bitten twice).
# =====================================================================
if [ "$ARM" -eq 1 ]; then
  run_item B7 B7_f270_2x_dumps.json 90 bash -c '
    set -e
    '"$PY"' tools/arm_test_registry.py --restore
    '"$PY"' tools/arm_test_registry.py --kind result_dump --journal '"$OUT"'/B7_f270_2x_dumps.json
    '"$PY"' tools/arm_test_registry.py --restore
    echo "NOTE: --apply is NOT run here. Inspect the journal, decide per record, then apply."'
else
  note "SKIP  B7 — the 55 F270 2x-dump re-run is destructive; pass --arm to include it."
fi

# =====================================================================
# B8 — make drift AFTER the re-runs (trap #1: never diff what you did
#      not re-run).  Only meaningful once B1/B2/B7 have actually run.
# =====================================================================
run_item B8 B8_drift_after_reruns.json 10 bash -c \
  "$PY tools/check_result_drift.py > $OUT/B8_drift_after_reruns.txt 2>&1; \
   $PY -c \"import json,os;json.dump({'see':'B8_drift_after_reruns.txt'},open(os.environ['OUT']+'/B8_drift_after_reruns.json','w'))\""

note "=== battery finished ==="
note "journal: $JOURNAL"
note "next: read test-results/audit-v/MANIFEST.md for which V-item each JSON closes."

# =====================================================================
# V2.5 — the cubic.py rename.  COMMENTED ON PURPOSE.  Run deliberately,
# not as part of a battery: this mount refuses `unlink` so it must happen
# on Ben's machine, and it is a rename with a blast radius the original
# handoff undercounted by a factor of four (audit finding V-018).
#
#   git mv src/casim/engine/lattice/core.py       src/casim/engine/lattice/cubic.py
#   git mv src/casim/engine/lattice/core_exact.py src/casim/engine/lattice/cubic_exact.py
#
# THEN REPOINT — the documented "8 importers plus the aliases" is right for
# src/ but omits tests/ entirely:
#
#   src/  8 importers:
#     engine/core/_viz_live_display.py       engine/gauge/bilinear_2d.py
#     engine/forks/gravity/dirac_gravity_fork.py   engine/gauge/propagator.py
#     engine/forks/particles/complex_mass_fork.py  engine/gauge/weak.py
#     engine/lattice/curved.py               engine/particles/dirac.py
#   src/  2 alias lines:
#     src/casim/lattice/__init__.py:17,18  (ca_core / ca_core_exact — keep the NAMES)
#   tests/ 27 import sites across 23 files:
#     findings/ 7 · priority/ 2 · runners/ 18
#     ( grep -rln "lattice.core_exact\|lattice import core_exact\|lattice.core import\|lattice import core\b" tests )
#   tools/ 0
#
# Also update the registry paths and re-run:  make indexes && make gate
# =====================================================================
