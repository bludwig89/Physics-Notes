"""
ca_bethe_log.py — the hydrogen Bethe logarithm ln k0(n,l) computed FROM THE
MODEL'S OWN Coulomb spectrum, with no literature input (F257).

Context: the F252 Lamb shift used the tabulated Bethe logarithm (Drake/Klarsfeld)
as a literature constant. This module removes that input: it computes ln k0 from
first principles using the model Hamiltonian's Coulomb resolvent, so the F252
Lamb shift becomes a fully model-derived number.

METHOD — Dalgarno-Lewis resolvent (no slow state-sum)
====================================================
The Bethe logarithm is the log-weighted mean excitation energy

    ln k0(n,l) = [ Σ_m |<n|p|m>|^2 (E_m-E_n) ln|E_m-E_n| ] / [ Σ_m |<n|p|m>|^2 (E_m-E_n) ]

with the sum over the FULL intermediate spectrum (discrete + continuum). A direct
pseudostate sum converges very slowly (the log weight emphasises high-energy
virtual states). Instead we use the integral identity

    ln(e) = ∫_0^∞ [ 1/(1+t) - 1/(e+t) ] dt          (e>0)

which turns the sum into a one-dimensional t-integral of the CoulombGreen's
function (Dalgarno-Lewis):

    ln k0 = (1/D) ∫_0^∞ [ M3/(1+t) - M2 + t M1 - t^2 M0 + t^3 F(t) ] dt  + ln2,

    F(t) = <g_r|(H_l - E_n + t)^{-1}|g_r>,   g_r = r·u_n  (length source),
    M_p  = <g_r|(H_l - E_n)^p|g_r>  (energy moments),  D = M3 = Σ|<p>|^2 ΔE,

where the +ln2 converts the Hartree-unit energies in the log to Rydberg (the
convention of the tabulated values). F(t) is a stable tridiagonal solve of the
inhomogeneous radial equation on the model's finite-difference Coulomb
Hamiltonian — i.e. it samples the model's own spectrum through its resolvent.

Below-threshold / degenerate intermediate states (the 2p case: the 1s lies below
2p, the 2s is degenerate) violate the e>0 identity; they are PROJECTED OUT of the
resolvent and added explicitly (the degenerate ΔE=0 state contributes 0; the
below state contributes |<p>|^2 ΔE ln|ΔE| with ΔE<0).

SCOPE / PRECISION (honest)
==========================
On a uniform radial grid the result converges to the accepted Bethe logs as
O(h) and is limited to ~2-3% by the discretisation of the high-energy continuum
(the origin/short-distance region that dominates M3). O(h) Richardson
extrapolation is applied. Reaching the tabulated 6-digit values needs a
nucleus-clustered (log) grid or a Sturmian basis with analytic continuum — noted
as a refinement. The point established here: ln k0 is DERIVABLE from the model's
spectrum (no literature constant), reproducing 2.984 / 2.812 / -0.030 to a few
percent, which propagates to a Lamb shift within ~1% of measured.

Pure numpy (real tridiagonal solves; no np.linalg.eig on chiral matrices,
CLAUDE.md — nothing chiral here).
"""
from __future__ import annotations

import math

import numpy as np

# accepted values (for comparison only — NOT used in the computation)
ACCEPTED = {"1s": 2.9841285558, "2s": 2.8117698931, "2p": -0.0300167089}

# exact hydrogen radial u-functions u(r)=r R(r), atomic units, Z=1
U_FUNCS = {
    "1s": (0, 1, lambda r: 2.0 * r * np.exp(-r), -0.5),
    "2s": (0, 2, lambda r: (1.0 / (2.0 * math.sqrt(2.0))) * (2.0 - r) * r * np.exp(-r / 2.0), -0.125),
    "2p": (1, 2, lambda r: (1.0 / (2.0 * math.sqrt(6.0))) * r * r * np.exp(-r / 2.0), -0.125),
}


# ----------------------------------------------------------------------
# tridiagonal machinery (batched over t)
# ----------------------------------------------------------------------
def _bt(sub, diag, sup, rhs):
    nt, N = diag.shape
    cp = np.empty((nt, N)); dp = np.empty((nt, N))
    cp[:, 0] = sup[0] / diag[:, 0]; dp[:, 0] = rhs[0] / diag[:, 0]
    for i in range(1, N):
        m = diag[:, i] - sub[i] * cp[:, i - 1]
        cp[:, i] = sup[i] / m
        dp[:, i] = (rhs[i] - sub[i] * dp[:, i - 1]) / m
    x = np.empty((nt, N)); x[:, -1] = dp[:, -1]
    for i in range(N - 2, -1, -1):
        x[:, i] = dp[:, i] - cp[:, i] * x[:, i + 1]
    return x


def _Hdiag(l, r, h):
    return 1.0 / h ** 2 + l * (l + 1) / (2.0 * r ** 2) - 1.0 / r


def _applyH(w, l, r, h):
    out = _Hdiag(l, r, h) * w
    off = -0.5 / h ** 2
    out[:-1] += off * w[1:]; out[1:] += off * w[:-1]
    return out


def _dl_channel(l, gr, Et, r, h, tt, proj=None):
    """Return (M3_channel, integrand(t)) for one intermediate l-channel.
    proj: list of normalised u-eigenfunctions to project OUT of the source
    (below-threshold / degenerate states handled explicitly by the caller)."""
    if proj:
        for ue in proj:
            gr = gr - (np.sum(ue * gr) * h) * ue
    g1 = _applyH(gr, l, r, h) - Et * gr
    g2 = _applyH(g1, l, r, h) - Et * g1
    g3 = _applyH(g2, l, r, h) - Et * g2
    M0 = np.sum(gr * gr) * h; M1 = np.sum(gr * g1) * h
    M2 = np.sum(gr * g2) * h; M3 = np.sum(gr * g3) * h
    sub = np.full(len(r), -0.5 / h ** 2); sup = np.full(len(r), -0.5 / h ** 2)
    base = _Hdiag(l, r, h) - Et
    x = _bt(sub, base[None, :] + tt[:, None], sup, gr)
    F = (x * gr[None, :]).sum(1) * h
    integ = M3 / (1 + tt) - M2 + tt * M1 - tt ** 2 * M0 + tt ** 3 * F
    return M3, integ


def bethe_log_raw(state, N, rmax=300.0, nt=800):
    """ln k0(state) on a single uniform grid of N points to r=rmax."""
    target_l, n_target, uf, Et = U_FUNCS[state]
    r = np.linspace(rmax / N, rmax, N); h = r[1] - r[0]
    uu = (np.arange(nt) + 0.5) / nt; tt = uu / (1 - uu); jac = 1.0 / (1 - uu) ** 2
    # explicit discrete intermediate states (below/degenerate) that must be
    # projected out of the resolvent and added by hand:
    proj_states = {}
    if state == "2p":
        # l=0 channel: 1s (below), 2s (degenerate)
        proj_states[0] = [("1s", -0.5), ("2s", -0.125)]
    D = 0.0; J = 0.0
    for l in [q for q in (target_l - 1, target_l + 1) if q >= 0]:
        gr = r * uf(r)
        proj = None
        if l in proj_states:
            proj = []
            for (sname, Ed) in proj_states[l]:
                ue = U_FUNCS[sname][2](r)
                ue = ue / math.sqrt(np.sum(ue * ue) * h)
                proj.append(ue)
                a = np.sum(ue * (r * uf(r))) * h
                eps = Ed - Et
                if abs(eps) > 1e-9:                       # below-threshold term
                    D += a * a * eps ** 3
                    J += a * a * eps ** 3 * math.log(abs(2.0 * eps))
        M3, integ = _dl_channel(l, gr, Et, r, h, tt, proj=proj)
        D += M3
        J += (np.sum(integ * jac) / nt) + math.log(2.0) * M3
    return J / D


def bethe_log(state, N=24000, rmax=300.0, nt=800):
    """O(h) Richardson-extrapolated ln k0(state): combine grids N and 2N.
    (Uniform-grid convergence is O(h); the extrapolation removes the leading
    linear term.)"""
    bN = bethe_log_raw(state, N, rmax, nt)
    b2N = bethe_log_raw(state, 2 * N, rmax, nt)
    return 2.0 * b2N - bN, {"raw_N": bN, "raw_2N": b2N}


def report(N=12000, rmax=300.0, nt=600):
    out = {}
    for s in ("1s", "2s", "2p"):
        val, detail = bethe_log(s, N=N, rmax=rmax, nt=nt)
        acc = ACCEPTED[s]
        out[s] = {"model_ln_k0": val, "accepted": acc,
                  "abs_err": val - acc,
                  "rel_err": (val - acc) / acc if abs(acc) > 1e-6 else None,
                  "raw": detail}
    out["method"] = ("Dalgarno-Lewis Coulomb-resolvent, uniform grid, O(h) "
                     "Richardson; no literature input")
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2, default=str))
