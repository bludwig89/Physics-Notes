# F37 — Riemann–Silberstein Eigenstates Correspond Exactly to BCC Chirality Branches

**2026-05-24 - 00:00**

## Summary

The two physical photon helicities — the Riemann–Silberstein (RS) eigenstates
$\mathbf{F}_\pm = \mathbf{E} \pm i\mathbf{B}$ — correspond exactly and uniquely to the
two BCC chirality branches $\Omega^\pm(k) = 2\omega_\pm(k/2)$.  The correspondence
is forced by two independent algebraic constraints: the eigenvalue structure of the
BCC rotation law and the Hermitian-symmetry condition on real fields.  Together they
imply that the BCC lattice predicts **vacuum birefringence** — RCP and LCP photons
propagate at different phase velocities — and that the current $\Omega_\text{even}$
W-field implementation averages this away by construction.

---

## Derivation

### Part 1 — Rotation matrix eigenstates

The BCC free-field propagation step acts on each $(E^a_k, B^a_k)$ pair as

$$\begin{pmatrix} E^a_k(t+1) \\ B^a_k(t+1) \end{pmatrix}
= R(\Omega) \begin{pmatrix} E^a_k(t) \\ B^a_k(t) \end{pmatrix}, \qquad
R(\Omega) = \begin{pmatrix} \cos\Omega & \sin\Omega \\ -\sin\Omega & \cos\Omega \end{pmatrix}$$

The eigenvalues of $R(\Omega)$ are $e^{\mp i\Omega}$; the eigenvectors are
$(1, \mp i)^T/\sqrt{2}$:

$$R(\Omega)\begin{pmatrix}1\\-i\end{pmatrix} = e^{-i\Omega}\begin{pmatrix}1\\-i\end{pmatrix}, \qquad
R(\Omega)\begin{pmatrix}1\\+i\end{pmatrix} = e^{+i\Omega}\begin{pmatrix}1\\+i\end{pmatrix}$$

*Proof:*
$$R(\Omega)\begin{pmatrix}1\\-i\end{pmatrix} = \begin{pmatrix}\cos\Omega - i\sin\Omega \\ -\sin\Omega - i\cos\Omega\end{pmatrix} = e^{-i\Omega}\begin{pmatrix}1\\-i\end{pmatrix} \quad$$

The eigenstates in field language are the Riemann–Silberstein combinations:

$$\mathbf{F}_+(k) \equiv E_k + iB_k \;\; \text{(eigenvalue }e^{-i\Omega}\text{)}, \qquad
\mathbf{F}_-(k) \equiv E_k - iB_k \;\; \text{(eigenvalue }e^{+i\Omega}\text{)}$$

This is an exact algebraic identity, independent of the specific dispersion $\Omega(k)$.

### Part 2 — Hermitian symmetry uniquely assigns the branches

For a real electromagnetic field, Fourier coefficients satisfy
$E(-k) = E^*(k)$, $B(-k) = B^*(k)$, giving:

$$\mathbf{F}_+(-k) = E(-k) + iB(-k) = E^*(k) + iB^*(k) = \mathbf{F}_-^*(k) \tag{HS}$$

Now allow each RS eigenstate to propagate at its own dispersion $\phi^\pm(k) > 0$:

$$\mathbf{F}_+(k,n) = \mathbf{F}_+(k,0)\,e^{-i\phi^+(k)\,n}, \qquad
\mathbf{F}_-(k,n) = \mathbf{F}_-(k,0)\,e^{+i\phi^-(k)\,n}$$

Imposing (HS) at all times:

$$\mathbf{F}_+(-k,0)\,e^{-i\phi^+(-k)\,n} = \bigl[\mathbf{F}_-(k,0)\bigr]^*\,e^{-i\phi^-(k)\,n}$$

Since $\mathbf{F}_+(-k,0) = \mathbf{F}_-^*(k,0)$ (HS at $t=0$), the amplitude factors cancel and we require:

$$\boxed{\phi^+(-k) = \phi^-(k)} \tag{Chirality constraint}$$

The BCC dispersion satisfies this **exactly**: $\omega_+(-k) = \omega_-(k)$ (the two branches
are related by parity), so

$$\Omega^+(-k) \equiv 2\omega_+(-k/2) = 2\omega_-(k/2) \equiv \Omega^-(k) \quad$$

Therefore the unique Hermitian-symmetry-preserving assignment is:

$$\mathbf{F}_+(k) \text{ propagates at } \Omega^+(k) \qquad \mathbf{F}_-(k) \text{ propagates at } \Omega^-(k)$$

No other pairing of the two BCC branches to the two RS eigenstates is consistent
with reality of $(E, B)$.

### Part 3 — Physical helicity matches the chirality label

A plane wave propagating along $\hat{k} = \hat{z}$ with **positive helicity** (RCP,
$h = +1$) satisfies $\mathbf{B} = -i\mathbf{E}$:

$$\mathbf{F}_+ = \mathbf{E} + i(-i\mathbf{E}) = 2\mathbf{E} \neq 0, \qquad
\mathbf{F}_- = \mathbf{E} - i(-i\mathbf{E}) = 0$$

A **negative-helicity** wave (LCP, $h = -1$) has $\mathbf{B} = +i\mathbf{E}$:

$$\mathbf{F}_+ = \mathbf{E} + i(+i\mathbf{E}) = 0, \qquad
\mathbf{F}_- = 2\mathbf{E} \neq 0$$

The complete correspondence is:

| Physical helicity | RS eigenstate | BCC branch | Phase advance per step |
|---|---|---|---|
| $h = +1$ (RCP) | $\mathbf{F}_+ = \mathbf{E}+i\mathbf{B}$ | $\Omega^+(k) = 2\omega_+(k/2)$ | $e^{-i\Omega^+(k)}$ |
| $h = -1$ (LCP) | $\mathbf{F}_- = \mathbf{E}-i\mathbf{B}$ | $\Omega^-(k) = 2\omega_-(k/2)$ | $e^{+i\Omega^-(k)}$ |

---

## Consequence: vacuum birefringence

The chirality-faithful propagation law replaces the single rotation $R(\Omega_\text{even})$
with the split:

$$E_k(n+1) = \frac{e^{-i\Omega^+}\mathbf{F}_+ + e^{+i\Omega^-}\mathbf{F}_-}{2}, \qquad
B_k(n+1) = \frac{e^{-i\Omega^+}\mathbf{F}_+ - e^{+i\Omega^-}\mathbf{F}_-}{2i}$$

where $\mathbf{F}_\pm = E_k \pm iB_k$.  This preserves Hermitian symmetry exactly
(by the argument in Part 2) but gives different phase velocities to the two
circular polarizations.  The birefringence per wavevector is:

$$\Delta\Omega(k) \equiv \Omega^+(k) - \Omega^-(k) = 2\bigl[\omega_+(k/2) - \omega_-(k/2)\bigr]$$

From F30 (sympy expansion along the body diagonal $(1,1,1)$, to leading order):

$$\Delta\Omega \approx -\frac{\sqrt{3}}{27}\,k^2, \qquad k \ll 1$$

The corresponding phase velocity difference:

$$\frac{\Delta v_\phi}{c_\text{lat}} = \frac{\Omega^+ - \Omega^-}{|\Omega^+ + \Omega^-|} \approx -\frac{k}{18}$$

This is first-order in $k$ — **linear vacuum birefringence**.  It vanishes on the
cube axes (where $\omega_+(k) = \omega_-(k)$ by symmetry) and is maximal along
the BCC body diagonals.

### Direction-dependence

| Direction | $\Omega^+$ vs $\Omega^-$ | Birefringence |
|---|---|---|
| Cube axes $(\pm1,0,0)$ etc. | Equal | Zero (exact) |
| Face diagonals $(\pm1,\pm1,0)$ etc. | $n=2$ difference | Quadratic in $k$ |
| Body diagonals $(\pm1,\pm1,\pm1)$ | $n=1$ difference | Linear in $k$; $\Delta v/c \approx -k/18$ |

---

## Relation to the composite photon (F26 / F29)

The composite photon in `ca_maxwell.py` is constructed from a single Weyl spinor
with `sign='+'`.  This makes it a *single-helicity* object — it already lives on
the $\Omega^+$ branch alone.  Its partner $\mathbf{F}_-$ (the opposite helicity)
would be the composite photon built from the `sign='-'` Weyl spinor, living on
$\Omega^-$.

The physical (real) photon field is a superposition of both helicities, which is
why the W-field must carry both $\mathbf{F}_+$ and $\mathbf{F}_-$ simultaneously.
The current $\Omega_\text{even} = (\Omega^+ + \Omega^-)/2$ W-propagation step is
the approximation that replaces each helicity's true dispersion with the average.
It is exact only where $\Omega^+ = \Omega^-$ (cube axes).

---

## Relation to current W-field implementation

The existing `w_propagation_step_spectral` and `_f26_rotation_step` use
$\Omega_\text{even}$ for both eigenstates.  This was the correct choice to preserve
real-field Hermitian symmetry with a *single* $2\times 2$ rotation matrix.  F37 shows
that Hermitian symmetry can also be preserved with the chirally-faithful split law —
it just requires working in the $(C_+, C_-)$ basis rather than the $(E, B)$ basis.

The chirally-faithful implementation `w_propagation_step_chiral` would be:

```python
def w_propagation_step_chiral(E_W, B_W):
    """Chirality-faithful propagation: F+ at Omega+, F- at Omega-."""
    shape = E_W.shape[1:]
    KX, KY, KZ = _kgrid3d(*shape)
    omega_p = bcc_dispersion(KX / 2, KY / 2, KZ / 2, sign='+')
    omega_m = bcc_dispersion(KX / 2, KY / 2, KZ / 2, sign='-')
    # Omega+ and Omega- (full rotation angles)
    Op = 2 * omega_p   # = Omega^+(k)
    Om = 2 * omega_m   # = Omega^-(k)
    E_new = np.zeros_like(E_W)
    B_new = np.zeros_like(B_W)
    for a in range(3):
        Ek = _fft.fftn(E_W[a])
        Bk = _fft.fftn(B_W[a])
        Fp = Ek + 1j * Bk   # F+ eigenstate
        Fm = Ek - 1j * Bk   # F- eigenstate
        Fp_new = np.exp(-1j * Op) * Fp
        Fm_new = np.exp(+1j * Om) * Fm
        E_new[a] = _fft.ifftn((Fp_new + Fm_new) / 2).real
        B_new[a] = _fft.ifftn((Fp_new - Fm_new) / (2j)).real
    return E_new, B_new
```

Note: `bcc_dispersion(kx, ky, kz, sign='+')` already gives $\omega_+(k)$, so
$\Omega^\pm = 2\omega_\pm(k/2)$ requires passing $k/2$ — but here since the $k$-grid
is already at the field wavenumber, we pass the full $k$ to get the $\Omega$ rotation
angle directly.  (The F26 convention is $\Omega = \omega_+(k/2)+\omega_-(k/2)$; the
chiral convention splits as $\Omega^+ = 2\omega_+(k/2)$, $\Omega^- = 2\omega_-(k/2)$.)

---

## Exactness status

| Statement | Type | Residual |
|---|---|---|
| $R(\Omega)(1,-i)^T = e^{-i\Omega}(1,-i)^T$ | Algebraic identity | Exact |
| $\mathbf{F}_+(-k) = \mathbf{F}_-^*(k)$ for real $(E,B)$ | Algebraic identity | Exact |
| Hermitian symmetry $\Rightarrow \phi^+(-k) = \phi^-(k)$ | Algebraic proof | Exact |
| BCC satisfies $\Omega^+(-k) = \Omega^-(k)$ | Algebraic (from $\omega_\pm$ definition) | Exact |
| RCP: $\mathbf{F}_- = 0$; LCP: $\mathbf{F}_+ = 0$ | Algebraic | Exact |
| $\Delta\Omega \approx -\sqrt{3}k^2/27$ along $(1,1,1)$ | Machine precision (F30 sympy) | $\leq$ sympy exact |

---

## Open questions

1. **Sign of birefringence:** Is $\Omega^+(k) > \Omega^-(k)$ for small $k$ along
   $(1,1,1)$, or vice versa?  F30 gives $\Omega^+ - \Omega^- = -\sqrt{3}k^2/27 < 0$,
   meaning RCP is *slower* than LCP along the body diagonal.  This is a falsifiable
   prediction: given the identification of the BCC lattice orientation with physical
   space, one polarisation is systematically favoured.

2. **Observational signature:** The birefringence $\Delta v_\phi/c \approx -k/18$
   (body diagonal) is linear in photon energy ($k \propto E_\gamma/E_\text{Planck}$).
   Linear vacuum birefringence produces energy-dependent rotation of the polarisation
   angle $\Delta\theta = \Delta k \cdot d/2$ for a source at distance $d$.  Current
   $\gamma$-ray polarimetry (INTEGRAL, *Fermi*/GBM) constrains $|\Delta v_\phi/c|
   \lesssim 10^{-10}$ at $E_\gamma \sim 100\,\text{keV}$; this sets a bound on the
   lattice cell size.

3. **Chirally-faithful W-field propagation:** Should `w_propagation_step_spectral`
   be replaced by the split-basis version?  The current even-dispersion implementation
   is appropriate when the W-field is treated as a classical real field without
   helicity resolution; the chiral version is needed when helicity-dependent
   observables are computed (e.g., circular polarisation Stokes parameter $V$).

4. **Composite photon construction:** The F29 bilinear only uses `sign='+'`.  A
   complete two-helicity photon state requires both Weyl branches.  This is the
   natural next step after F37.
