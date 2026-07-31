"""
GR-3 candidate-fix forks
========================
Three variants of the L4 metric ansatz that attempt to resolve the Finding
14.5 factor-of-2 Pound-Rebka problem without breaking GR-1 (deflection) or
GR-2 (Shapiro).  Each fork exposes the same three callables so the cross-
fork harness in `gr3_fork_harness.py` can run identical line integrals on
each:

    c_photon(phi, c_0)     — effective light speed seen by photons
    c_matter(phi, c_0)     — effective light speed seen by matter packets
    tau_rate(phi, c_0)     — local proper-time tick rate (1 at infinity)

* Baseline (Paper 6)     — c_photon == c_matter, tau_rate = c/c_0 (factor 2)
* Fork A  (phase-tick)   — c_photon = c_matter = Paper 6;  tau_rate = 1+phi/c^2
* Fork B  (anisotropic)  — c_photon = c_0 sqrt(|g00|/g_xx);  tau_rate = sqrt(|g00|)
* Fork C  (restricted-c) — c_photon = Paper 6;  c_matter = c_0/(1-phi/c^2)

The harness then composes:
  GR-1 (deflection)   uses c_photon line integral
  GR-2 (Shapiro)      uses c_photon line integral
  GR-3 (Pound-Rebka)  uses tau_rate at two cells
  GR-4 (Mercury)      uses the timelike geodesic of (g00, g_ii) recovered
                       from (c_matter, tau_rate)
"""
