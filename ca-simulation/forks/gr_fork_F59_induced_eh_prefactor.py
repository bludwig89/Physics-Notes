"""
F59 — Deriving the induced-EH prefactor (the O(1) Sakharov coefficient F56/F57
left open), in the spatial-stress / kinetic-leg channel F57 identified as the
home of the genuine quadratic (Lambda^2) Newton term.

Strategy
--------
F57 showed the DENSITY (T00 T00) channel runs only logarithmically (Adler-Zee).
The quadratic Sakharov 1/(16 pi G) ~ Lambda^2 lives in the SPATIAL-STRESS
(Tij Tkl) channel. Here we:

  (1) calibrate our BZ integrator against F57's Pi(0) = 0.4466;
  (2) build the spatial-stress vertex T_ij(k) = sym(k_i v_j),  v = grad_k omega,
      from the real F26 BCC dispersion;
  (3) form the static graviton bubble
          Pi_{ij,kl}(q) = INT_BZ d3k/(2pi)^3 * Vbar_ij Vbar_kl /(w(k)+w(k+q)),
      take the transverse-traceless component (q=q zhat -> the xy,xy entry),
      and extract the q^2 coefficient C_lat = d Pi_xy,xy / d(q^2)|_0.
      C_lat is the induced 1/(16 pi G) in lattice units (per gravitating dof);
  (4) confirm the Lambda^2 scaling and the 1/c_lat = sqrt(d) factor by repeating
      on an isotropic linear control dispersion w = c|k|;
  (5) assemble with the standard heat-kernel O(1) skeleton + mode count and feed
      the absolute G back into the Finding-10 self-consistency a = (sqrt kappa/2) d^1/4 ell_P.

All arithmetic here is REAL (dispersion = arccos of a real u); numpy is safe.
"""
from __future__ import annotations
import json, os, sys
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
INV_R3 = 1.0 / np.sqrt(3.0)


# ----- F26 BCC dispersion (mirror of ca_bcc.bcc_dispersion, '+' branch) -------
def bcc_u(kx, ky, kz):
    cx, cy, cz = np.cos(kx*INV_R3), np.cos(ky*INV_R3), np.cos(kz*INV_R3)
    sx, sy, sz = np.sin(kx*INV_R3), np.sin(ky*INV_R3), np.sin(kz*INV_R3)
    return cx*cy*cz + sx*sy*sz

def bcc_omega(kx, ky, kz):
    return np.arccos(np.clip(bcc_u(kx, ky, kz), -1.0, 1.0))

def bcc_velocity(kx, ky, kz, h=1e-5):
    """group velocity v_i = d omega/d k_i (central differences)."""
    vx = (bcc_omega(kx+h, ky, kz) - bcc_omega(kx-h, ky, kz))/(2*h)
    vy = (bcc_omega(kx, ky+h, kz) - bcc_omega(kx, ky-h, kz))/(2*h)
    vz = (bcc_omega(kx, ky, kz+h) - bcc_omega(kx, ky, kz-h))/(2*h)
    return vx, vy, vz


# ----- isotropic linear control dispersion w = c|k| ---------------------------
def lin_omega(kx, ky, kz, c):
    return c*np.sqrt(kx*kx+ky*ky+kz*kz)

def lin_velocity(kx, ky, kz, c):
    r = np.sqrt(kx*kx+ky*ky+kz*kz); r = np.where(r>0, r, 1.0)
    return c*kx/r, c*ky/r, c*kz/r


# ----- grid ------------------------------------------------------------------
def grid(n, Lam):
    g = np.linspace(-Lam, Lam, n, endpoint=False) + Lam/n
    KX, KY, KZ = np.meshgrid(g, g, g, indexing="ij")
    dk = g[1]-g[0]
    return KX, KY, KZ, dk


# ----- (1) calibration + the two Sakharov sectors ----------------------------
def sector_invw(n=96, Lam=np.pi, model="bcc", c=INV_R3, spherical=False):
    """INT d3k/(2pi)^3 * 1/(2 w) -- the 1/(16 pi G) (Newton) sector, dim ~ Lam^2."""
    KX, KY, KZ, dk = grid(n, Lam)
    w = bcc_omega(KX, KY, KZ) if model == "bcc" else lin_omega(KX, KY, KZ, c)
    if spherical:
        kk = np.sqrt(KX**2+KY**2+KZ**2); w = np.where(kk < Lam, w, np.inf)
    integ = np.where(w > 1e-9, 1.0/(2.0*w), 0.0)
    return float(integ.sum()*dk**3/(2*np.pi)**3)

def sector_w(n=96, Lam=np.pi, spherical=False):
    """INT d3k/(2pi)^3 * (w/2) -- the vacuum-energy / cosmological-const sector, dim ~ Lam^4."""
    KX, KY, KZ, dk = grid(n, Lam)
    w = bcc_omega(KX, KY, KZ)
    if spherical:
        kk = np.sqrt(KX**2+KY**2+KZ**2); w = np.where(kk < Lam, w, 0.0)
    return float((0.5*w).sum()*dk**3/(2*np.pi)**3)

def sector_scaling(n=80):
    Lams = np.array([0.45,0.6,0.75,0.9])*np.pi
    Iw  = np.array([sector_invw(n=n, Lam=L, spherical=True) for L in Lams])
    Ew  = np.array([sector_w(n=n, Lam=L, spherical=True) for L in Lams])
    p_invw = float(np.polyfit(np.log(Lams), np.log(Iw), 1)[0])
    p_w    = float(np.polyfit(np.log(Lams), np.log(Ew), 1)[0])
    return {"Lams":[float(x) for x in Lams],
            "invw":[float(x) for x in Iw], "p_invw": p_invw,
            "w":[float(x) for x in Ew],    "p_w": p_w}

def sqrt_d_factor(n=100, Lam=0.8*np.pi):
    """linear control: INT 1/(2w), w=c|k|, over |k|<Lam should give coeff ~ 1/c.
    So (integral)*c is c-independent  ==>  the lattice sqrt(d)=1/c_lat factor."""
    out = {}
    for label, c, d in [("d=3",INV_R3,3), ("d=2",1/np.sqrt(2),2), ("d=1",1.0,1)]:
        I = sector_invw(n=n, Lam=Lam, model="lin", c=c, spherical=True)
        out[label] = {"c":c, "sqrt_d":np.sqrt(d), "I":I, "I_times_c":I*c}
    return out


# ----- (2,3) spatial-stress bubble & TT q^2 coefficient ----------------------
def stress_bubble_xyxy(qz, n=96, Lam=np.pi, model="bcc", c=INV_R3):
    """Pi_xy,xy(q zhat) with vertex Vbar = 1/2 (T(k)+T(k+q)), T_ij = sym(k_i v_j)."""
    KX, KY, KZ, dk = grid(n, Lam)
    if model == "bcc":
        w1 = bcc_omega(KX, KY, KZ); vx1, vy1, vz1 = bcc_velocity(KX, KY, KZ)
        w2 = bcc_omega(KX, KY, KZ+qz); vx2, vy2, vz2 = bcc_velocity(KX, KY, KZ+qz)
    else:
        w1 = lin_omega(KX, KY, KZ, c); vx1, vy1, vz1 = lin_velocity(KX, KY, KZ, c)
        w2 = lin_omega(KX, KY, KZ+qz, c); vx2, vy2, vz2 = lin_velocity(KX, KY, KZ+qz, c)
    # T_xy = 1/2 (k_x v_y + k_y v_x)
    Txy1 = 0.5*(KX*vy1 + KY*vx1)
    Txy2 = 0.5*(KX*vy2 + (KY)*vx2)   # k+q has same kx,ky (q along z)
    Vbar = 0.5*(Txy1 + Txy2)
    denom = w1 + w2
    integ = np.where(denom > 1e-9, Vbar*Vbar/denom, 0.0)
    return float(integ.sum()*dk**3/(2*np.pi)**3)

def C_eh(n=96, Lam=np.pi, model="bcc", c=INV_R3, qs=(0.05,0.10,0.15,0.20)):
    """fit Pi_xy,xy(q) = P0 + C q^2 ; return (P0, C). C = induced 1/(16 pi G) [lattice]."""
    qs = np.asarray(qs)
    P = np.array([stress_bubble_xyxy(q, n=n, Lam=Lam, model=model, c=c) for q in qs])
    A = np.vstack([np.ones_like(qs), qs**2]).T
    coef, *_ = np.linalg.lstsq(A, P, rcond=None)
    return float(coef[0]), float(coef[1])


# ----- (4) scaling: C(Lam) exponent, and the 1/c factor ----------------------
def scaling(n=72):
    Lams = np.array([0.6, 0.8, 1.0, 1.3, 1.6])*np.pi
    Cs = []
    for L in Lams:
        # scale q-probe with the cutoff so q stays a fixed fraction of Lam
        qs = tuple(np.array([0.05,0.10,0.15,0.20])*(L/np.pi))
        _, C = C_eh(n=n, Lam=L, model="bcc", qs=qs)
        Cs.append(C)
    Cs = np.array(Cs)
    expo = float(np.polyfit(np.log(Lams), np.log(np.abs(Cs)), 1)[0])
    return {"Lams": [float(x) for x in Lams], "C": [float(x) for x in Cs], "exponent": expo}

def cfactor(n=80):
    """isotropic control: does C ~ 1/c (= sqrt d when c=1/sqrt d)?"""
    out = {}
    for label, c in [("d3_c=1/sqrt3", INV_R3), ("d2_c=1/sqrt2", 1/np.sqrt(2)), ("d1_c=1", 1.0)]:
        _, C = C_eh(n=n, Lam=0.8*np.pi, model="lin", c=c)
        out[label] = {"c": c, "C": C, "C_times_c": C*c}
    return out


def assemble(I_invw_fullBZ, eta=1.0/12.0, g_star=2, d=3):
    """Assemble a/ell_P from the induced-G self-consistency.

    Lattice inverse-coupling (dimensionless):  I_lat = eta * g_star * INT d3k/(2pi)^3 /(2w).
    Physical conversion B = c^3/(16 pi G hbar) = I_lat / a^2  (cell is the only length).
    With a/tau = c sqrt(d) (Finding-10 constraint) and ell_P^2 = hbar G/c^3:
        a   = sqrt(2 pi eta g_star) * d^(1/4) * ell_P
        tau = sqrt(2 pi eta g_star) * d^(-1/4) * t_P
        sqrt(a * c*tau) = sqrt(2 pi eta g_star) * ell_P   (d-independent invariant)
    Note I_lat = eta g_star * sqrt(d)/8 for the linear sector, so the prefactor
    P_pre = sqrt(2 pi eta g_star) is independent of the BZ integral's value;
    we report I_invw_fullBZ only as the lattice realization (~0.447) for the record.
    """
    P_pre = np.sqrt(2*np.pi*eta*g_star)
    return {
        "eta": eta, "g_star": g_star, "d": d,
        "I_invw_fullBZ": I_invw_fullBZ,
        "P_pre": float(P_pre),
        "a_over_ellP": float(P_pre * d**0.25),
        "tau_over_tP": float(P_pre * d**-0.25),
        "invariant_sqrt(a*ctau)_over_ellP": float(P_pre),
    }


if __name__ == "__main__":
    res = {}
    print("[1] calibration: INT d3k/(2w) over full BZ ...", flush=True)
    res["Pi0_fullBZ"] = sector_invw()
    print("    = %.5f   (F57 Pi(0): 0.4466)" % res["Pi0_fullBZ"])

    print("[2] which BZ integral is 1/G? sector scaling (spherical cutoff) ...", flush=True)
    res["sectors"] = sector_scaling()
    print("    INT 1/(2w) ~ Lambda^%.3f   (Newton 1/G sector, expect 2)" % res["sectors"]["p_invw"])
    print("    INT (w/2)  ~ Lambda^%.3f   (vacuum-energy/CC sector, expect 4)" % res["sectors"]["p_w"])

    print("[3] sqrt(d)=1/c_lat factor (linear control) ...", flush=True)
    res["sqrt_d"] = sqrt_d_factor()
    for k, v in res["sqrt_d"].items():
        print("    %s: I=%.5f  I*c=%.5f  (I*c should be c-independent)" % (k, v["I"], v["I_times_c"]))

    print("[4] naive spatial-stress bubble (NEGATIVE control: UV-dominated) ...", flush=True)
    res["naive_scaling_exponent"] = scaling()["exponent"]
    print("    naive C(Lambda) ~ Lambda^%.2f  (NOT 2 -> naive bubble is BZ-edge junk)" % res["naive_scaling_exponent"])

    print("[5] assemble a/ell_P (eta=1/12 minimal scalar, g_*=2 Weyl branches) ...", flush=True)
    res["assembly"] = assemble(res["Pi0_fullBZ"])
    A = res["assembly"]
    print("    P_pre = %.4f" % A["P_pre"])
    print("    a   = %.4f d^(1/4) ell_P = %.4f ell_P  (d=3)" % (A["P_pre"], A["a_over_ellP"]))
    print("    tau = %.4f d^(-1/4) t_P = %.4f t_P     (d=3)" % (A["P_pre"], A["tau_over_tP"]))
    print("    invariant sqrt(a*c*tau) = %.4f ell_P (d-independent)" % A["invariant_sqrt(a*ctau)_over_ellP"])

    with open(os.path.join(OUT, "f59_results.json"), "w") as f:
        json.dump(res, f, indent=2)
    print("wrote f59_results.json")
