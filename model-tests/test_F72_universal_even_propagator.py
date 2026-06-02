"""
F70 — Can the F69 paired/even-law photon propagator be adopted *universally*,
retiring the chiral propagator (w_propagation_step_chiral) for the W/Z/gluon
sectors too?

This re-tests the question raised after F69 ("use the same method everywhere").
It does NOT re-derive any propagator; it confronts the model's real operators
(ca_wmu, ca_bcc, ca_gluon, ca_z_field) with the F68 selection criterion and
measures, per sector, the cost of forcing the even law.

The F68 criterion (the thing that *forced* the even law for the photon):
    a gauge field rides the EVEN (paired) law iff its minimal-coupling
    operator commutes with the Weyl unitary U^±(k)=u I - i(n.sigma), i.e. it
    is the IDENTITY/singlet channel in helicity space (helicity-blind).
    If the coupling lives in the sigma-vector channel (does NOT commute), the
    two RS helicities carry distinct rates Omega^+ != Omega^- and the chiral
    propagator is the faithful one; the even law is then only an imposed
    override (the sourceless Delta-Omega/2 of F67 S3), not a derivation.

Sections:
  C1  U(1)_EM identity coupling commutes with n.sigma            -> even FORCED
  C2  sigma-vector channel (W and the as-built gluon bilinear)   -> does NOT
      commute -> chiral faithful; even law = sourceless override
  C3  Quantify the branch split Delta-Omega the even law discards (= the
      F67 S3 cost), and confirm it is O(k^2) (linear/speed term untouched)
  C4  Empirical: forcing the even law on the W field erases the branch
      splitting that distinguishes its two helicities (the parity content)
  C5  Map the current code state and report what is self-consistent

All matrix work is done with explicit 2x2 complex arithmetic to avoid the
numpy/scipy chiral-transform pitfalls flagged in CLAUDE.md.

Run:  python3 test_F72_universal_even_propagator.py
"""
import os, sys, json, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ca-simulation"))

import ca_bcc as bcc
import ca_wmu as cwmu
import ca_fft as _fft
import ca_photon_pair as pp


def wrap(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def helicity_phases(E, B, m, Fp0, Fm0):
    """Accumulated phases of the two RS helicity eigenstates F^± = E ± iB at
    mode index (m,m,m). (Same observable as test_F69 PP2.)"""
    idx = (m, m, m)
    Eh = np.array([_fft.fftn(E[a])[idx] for a in range(3)])
    Bh = np.array([_fft.fftn(B[a])[idx] for a in range(3)])
    Fp = Eh + 1j * Bh
    Fm = Eh - 1j * Bh
    ap = np.vdot(Fp0, Fp) / np.vdot(Fp0, Fp0)
    am = np.vdot(Fm0, Fm) / np.vdot(Fm0, Fm0)
    return np.angle(ap), np.angle(am)

I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def U_pm(kx, ky, kz, sign):
    """Weyl unitary U^±(k) = u I - i (n.sigma) as an explicit 2x2."""
    u, nx, ny, nz = bcc._bcc_uvec(kx, ky, kz, sign=sign)
    return u * I2 - 1j * (nx * SX + ny * SY + nz * SZ)


def n_dot_sigma(kx, ky, kz, sign):
    u, nx, ny, nz = bcc._bcc_uvec(kx, ky, kz, sign=sign)
    return nx * SX + ny * SY + nz * SZ


def comm(A, B):
    return A @ B - B @ A


def fro(M):
    return float(np.sqrt(np.sum(np.abs(M) ** 2)))


def main():
    rng = np.random.default_rng(70)
    out = {"finding": "F72", "sections": {}}

    # ---- C1: U(1)_EM identity coupling commutes -> even forced ----------
    max_c_u1 = 0.0
    for _ in range(4000):
        k = rng.uniform(-np.pi, np.pi, 3)
        theta = rng.uniform(-np.pi, np.pi)
        P = np.exp(1j * theta) * I2          # minimal-coupling operator (F68)
        for s in ("+", "-"):
            U = U_pm(*k, s)
            max_c_u1 = max(max_c_u1, fro(comm(P, U)))
    out["sections"]["C1_U1_identity_commutes"] = {
        "max_||[e^{i.theta}I, U^pm]||": max_c_u1,
        "verdict": "commutes -> helicity-blind -> EVEN law forced (F68)",
        "pass": max_c_u1 < 1e-12,
    }

    # ---- C2: sigma-vector channel does NOT commute ----------------------
    # The W triplet (F29) and the as-built gluon octet (F43) are sigma-vector
    # bilinears phi^dag (tau^a) sigma^i psi.  In helicity space the carried
    # operator is sigma^i, NOT the identity.  Test all three sigma^i.
    min_c_sv = np.inf
    for _ in range(4000):
        k = rng.uniform(-np.pi, np.pi, 3)
        for s in ("+", "-"):
            nds = n_dot_sigma(*k, s)
            for S in (SX, SY, SZ):
                min_c_sv = min(min_c_sv, fro(comm(S, nds)))
    out["sections"]["C2_sigma_vector_channel"] = {
        "min_||[sigma^i, n.sigma]|| (over W/gluon bilinear channel)": min_c_sv,
        "verdict": ("does NOT commute -> branch-split intrinsic -> CHIRAL "
                    "faithful; even law would be a sourceless override (F67 S3)"),
        "pass": min_c_sv > 1e-3,   # generically O(1); only vanishes at measure-zero k
    }

    # ---- C3: the branch split the even law discards = O(k^2) ------------
    # Delta-Omega(k) = Omega^+ - Omega^- = 2[w_+(k/2) - w_-(k/2)]; the chiral
    # law keeps it, the even law (Omega_pair = w_+(k/2)+w_-(k/2)) zeroes it.
    # Confirm it is purely O(k^2): the linear (speed-of-light) term is common.
    ks = np.linspace(1e-3, 0.6, 60)
    diag = np.array([1, 1, 1]) / np.sqrt(3.0)   # body diagonal
    dOmega = []
    for kk in ks:
        kx, ky, kz = kk * diag
        wp = bcc.bcc_dispersion(kx / 2, ky / 2, kz / 2, sign="+")
        wm = bcc.bcc_dispersion(kx / 2, ky / 2, kz / 2, sign="-")
        dOmega.append(2.0 * (wp - wm))
    dOmega = np.array(dOmega)
    # Fit dOmega = a1*k + a2*k^2 + a3*k^3 ; a1 (the speed-of-light split) must
    # vanish, a2 (the birefringence coefficient) must not.
    a3, a2, a1, a0 = np.polyfit(ks, dOmega, 3)
    dOm_over_k_smallk = float(dOmega[0] / ks[0])         # -> 0 as k -> 0
    out["sections"]["C3_branch_split_is_O_k2"] = {
        "linear_coef_a1 (speed-of-light split, expect ~0)": float(a1),
        "quadratic_coef_a2 (birefringence coef, nonzero)": float(a2),
        "dOmega/k at k=1e-3 (expect ~0)": dOm_over_k_smallk,
        "max|dOmega| over k<=0.6": float(np.max(np.abs(dOmega))),
        "verdict": ("even and chiral laws share the linear (c=1/sqrt3) term "
                    "(a1~0); they differ only at O(k^2) (a2!=0) -> the quantity "
                    "the even law discards is exactly the vacuum birefringence"),
        "pass": abs(a1) < 1e-3 and abs(a2) > 1e-3 and abs(dOm_over_k_smallk) < 1e-3,
    }

    # ---- C4: forcing even on the real W field erases the branch split ----
    # Build a linearly polarized body-diagonal mode (both RS helicities equally
    # populated), propagate N ticks under (a) the chiral law the W currently
    # uses, (b) the even/paired photon law. The birefringence observable
    # S = phi_+ + phi_- (F69 PP2) is the helicity-distinguishing content.
    # Chiral keeps it (S = -dOmega*N); even zeroes it (S = 0).
    L, m, N = 24, 1, 6
    khat = np.array([1.0, 1.0, 1.0]) / np.sqrt(3.0)
    E0, B0, e1, e2 = pp.build_pair_mode(L, m, khat, [1.0, -1.0, 0.0])
    Fp0, Fm0 = e1 + 1j * e2, e1 - 1j * e2
    k = 2 * np.pi * m / L
    dOm = float(pp.pair_birefringence(k, k, k))

    Ec, Bc = E0.copy(), B0.copy()
    for _ in range(N):
        Ec, Bc = cwmu.w_propagation_step_chiral(Ec, Bc)
    pc, mc = helicity_phases(Ec, Bc, m, Fp0, Fm0)
    S_chiral = float(wrap(pc + mc))

    Ee, Be = E0.copy(), B0.copy()
    for _ in range(N):
        Ee, Be = pp.photon_step_spectral(Ee, Be)     # the even / paired law
    pe, me = helicity_phases(Ee, Be, m, Fp0, Fm0)
    S_even = float(wrap(pe + me))

    out["sections"]["C4_even_erases_W_branch_content"] = {
        "S_chiral (keeps branch split)": S_chiral,
        "S_chiral_pred_-dOmega*N": float(wrap(-dOm * N)),
        "S_even (paired law, erases it)": S_even,
        "verdict": ("chiral law gives S = -dOmega*N (the two W helicities ride "
                    "Omega^+/Omega^- -> branch content present); the even/paired "
                    "law gives S~0 -> that helicity-distinguishing content is "
                    "discarded. For the W this content carries its parity "
                    "violation, so the even law is not a free swap."),
        "pass": (abs(S_chiral - wrap(-dOm * N)) < 1e-10 and abs(S_even) < 1e-12),
    }

    # ---- C5: current code map -------------------------------------------
    out["sections"]["C5_current_code_map"] = {
        "photon  (ca_photon_pair.photon_step_spectral)": "EVEN  (_f26_rotation_step)  [F69]",
        "Z       (ca_z_field.z_propagation_step_spectral)": "EVEN  (_f26_rotation_step)",
        "hyperch.(ca_wmu.hypercharge_propagation_step)": "EVEN  (_f26_rotation_step)",
        "W       (ca_wmu.w_propagation_step_chiral)": "CHIRAL (Omega^+/Omega^- split) [F37]",
        "gluon   (ca_gluon.gluon_rotation_step_spectral_bcc)": "CHIRAL (reuses W chiral step) [F43]",
    }

    secs = out["sections"]
    passed = all(s.get("pass", True) for s in secs.values())
    out["all_pass"] = passed
    return out


if __name__ == "__main__":
    t0 = time.time()
    res = main()
    res["wall_seconds"] = round(time.time() - t0, 2)
    outdir = os.path.join(HERE, "..", "test-results")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "F72_universal_even_propagator.json"), "w") as f:
        json.dump(res, f, indent=2)
    print(json.dumps(res, indent=2))
    print("\nALL PASS:", res["all_pass"], f"({res['wall_seconds']}s)")
