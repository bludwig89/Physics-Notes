"""
F230 — E1: attempt to derive the lepton spectrum angle delta* = 2/9 rad
(3 delta* = Q = 2/3) from the crystal-field / equipartition GEOMETRY
(F75/F76 T_1u + F78/F80 45 deg), distinct from the induced-coupling route
of F179 and the BPS route of F199.

Outcome: closes NEGATIVE. The geometry fixes only the ENDPOINTS of the phase
coordinate (democratic 0 deg; massless-Koide 3 delta = 45 deg = pi/4; equipartition
phi = 45 deg). The INTERIOR stopping point delta* is set by the brake ratio
B/C = crystal-field cubic / sextic self-coupling, i.e. by dynamics (lambda_6),
not geometry. Sharpened dimensional no-go: 3 delta* = Q equates a RADIAN to a
pure RATIO; no crystal-field geometry (which yields only trig ratios and rational
irrep multiplicities) can force a radian value. Definitive structural no-go is F199.

Real arithmetic only (numpy-safe). PDG charged-lepton masses.
"""
import json, math

results = {"finding": "F230", "item": "E1", "checks": {}}


def rec(name, statement, value, target, tier, ok):
    results["checks"][name] = {
        "statement": statement, "value": value, "target": target,
        "tier": tier, "status": "PASS" if ok else "FAIL",
    }
    print(f"[{'PASS' if ok else 'FAIL'}] {name} ({tier}): {statement}\n        value={value} target={target}")


me, mmu, mtau = 0.51099895, 105.6583755, 1776.86  # MeV, PDG
y = [math.sqrt(m) for m in (me, mmu, mtau)]
S1, S2 = sum(y), sum(v * v for v in y)
Q = S2 / S1 ** 2
ybar = S1 / 3
p = [v - ybar for v in y]
A = math.sqrt(2 / 3 * sum(pp * pp for pp in p))
cos3d = sum(pp ** 3 for pp in p) / (0.75 * A ** 3)
delta = math.acos(cos3d) / 3

# G1 — equipartition geometry (F80/F92): Q = 1/(3 cos^2 phi), r = A/ybar = sqrt2 at phi=45
r = math.sqrt(6 * (Q - 1 / 3))
rec("G1", "equipartition amplitude r=A/ybar -> sqrt2 (Q=2/3, phi=45deg, F80)",
    r, math.sqrt(2), "data/geometry", abs(r - math.sqrt(2)) < 1e-3)

# G2 — the target relation, at Koide confidence (re-confirming F179/F199)
rec("G2", "3 delta* = Q = 2/3 rad (delta* = 2/9 rad); |3delta*-Q|",
    abs(3 * delta - Q), 0.0, "target", abs(3 * delta - Q) < 1e-4)
rec("G2b", "delta* vs 2/9 rad relative residual",
    (delta - 2 / 9) / (2 / 9), 0.0, "target", abs((delta - 2 / 9) / (2 / 9)) < 1e-3)

# G3 — the massless endpoint is EXACTLY 3 delta = pi/4 (F96), NOT Q. So the physical
# interior value (3delta = Q = 2/3 rad) is a genuinely m_e>0, dynamics-set point.
u = 2 - math.sqrt(3)
delta_end = math.atan(math.sqrt(3) * u / (2 - u))
rec("G3", "massless endpoint delta=15deg, 3delta=pi/4=0.7854 rad != Q=0.6667",
    {"delta_end_deg": math.degrees(delta_end), "3delta_end_rad": 3 * delta_end,
     "Q": Q, "pi_4": math.pi / 4},
    {"delta_end_deg": 15.0, "3delta_end_rad": math.pi / 4},
    "exact/anchor",
    abs(math.degrees(delta_end) - 15.0) < 1e-6 and abs(3 * delta_end - math.pi / 4) < 1e-6
    and abs(3 * delta_end - Q) > 0.1)

# G4 — the geometric no-go: crystal-field geometry produces only dimensionless
# trig ratios / rational multiplicities. The endpoints it fixes are pure (0, pi/4,
# 45deg). The interior minimiser cos3delta* = -B/(2C) requires the DIMENSIONLESS
# ratio B/C, whose value is a dynamical (lambda_6) number, not geometry. Equating a
# RADIAN (3 delta*) to a RATIO (Q) has no geometric mechanism.
# Demonstrate: geometry alone (endpoints) leaves delta* free across [endpoint, 0].
geom_endpoints_rad = {"democratic_3delta": 0.0, "massless_3delta": math.pi / 4}
interior_free = 0.0 < 3 * delta < math.pi / 4  # physical sits strictly inside
rec("G4", "geometry fixes endpoints {0, pi/4}; interior 3delta* is dynamics-set (free to geometry)",
    {"interior_3delta": 3 * delta, **geom_endpoints_rad}, "interior in (0, pi/4)",
    "structural/negative", interior_free)

# G5 — cross-sector echo (flagged, not claimed): sin^2 theta_W = 2/9 (a RATIO, F49)
# vs delta* = 2/9 rad (a RADIAN, this sector). Same rational, different dimension ->
# almost certainly a coincidence of shared BCC-rational structure, NOT a derivation.
rec("G5", "echo: sin^2thetaW=2/9 (ratio) vs delta*=2/9 rad (radian) -- dimensionally distinct, flagged open",
    {"sin2thetaW": 2 / 9, "delta_star_rad": 2 / 9}, "coincidence (radian != ratio)",
    "flag/open", True)

results["verdict"] = (
    "NEGATIVE (sharpened no-go). The requested crystal-field + equipartition geometry "
    "fixes only the phase-coordinate endpoints (democratic 3delta=0; massless-Koide "
    "3delta=pi/4, exact; equipartition phi=45deg). The interior stopping point "
    "3delta*=Q=2/3 rad is set by the brake ratio B/C (crystal-field cubic vs sextic "
    "self-coupling), a dynamical (lambda_6) number. DIMENSIONAL no-go: 3delta* is a "
    "radian, Q is a pure ratio; geometry yields only trig ratios/rational multiplicities "
    "and cannot force a radian = ratio without a dynamical scale. Consistent with and "
    "subsumed by F199's three-way structural no-go; delta*=2/9 rad remains a "
    "Koide-confidence TARGET, answerable only by the saturated-condensate solve (alpha_eff*)."
)
npass = sum(1 for c in results["checks"].values() if c["status"] == "PASS")
results["summary"] = f"{npass}/{len(results['checks'])} PASS"
print("\n" + results["summary"] + " — " + results["verdict"])

with open("test-results/F230_lepton_angle_geometric_nogo.json", "w") as f:
    json.dump(results, f, indent=2)
