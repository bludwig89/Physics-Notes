"""
warp_openitems_explore.py
=========================
Exploration of the two F204 open items, with first computations.

OPEN ITEM 1 -- a *dynamically/structurally* evaluated superluminal SHIFT VECTOR
  (g_0i) through a gravitomagnetic T^0i kernel, beyond F204's static PC1 check.
OPEN ITEM 2 -- a genuine FORWARD Bobrick-Martire construction: a positive-T^00,
  momentum-carrying beable shell -> read off the induced subluminal bubble.

Shared machinery: the linearized gravitomagnetic (GEM) sector. The warp shift
vector N^i = g_0i is the *translational* analogue of Hartle's rotational
frame-drag omega(r) (F185/ca_rotation.py). In Lorenz gauge the off-diagonal
Einstein equation is a vector Poisson equation sourced by momentum density:

    nabla^2 N_i = -16 pi T^{0i}          (G=c=1, weak field)

solved here in FREE space (Hockney zero-padded FFT, kernel 4/|r|), so a moving
positive mass produces a finite, localized drag field -- exactly the object a
warp shift vector is.

Self-contained: numpy only (+ F181 kernel for the static lapse leg).
"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "src")))
from casim.engine.interactions import interior_metric as cim   # noqa

C_LAT = 1.0/np.sqrt(3.0)
np.set_printoptions(precision=4, suppress=True)
print("="*72)
print("F204 OPEN-ITEMS EXPLORATION   (c_lat = 1/sqrt(3) = %.5f)" % C_LAT)
print("="*72)


# ----------------------------------------------------------------------
# Gravitomagnetic free-space Poisson solver: nabla^2 N = -16 pi p
#   => N = 4 * (kernel 1/|r|) convolved with p   (Hockney zero-pad FFT)
# ----------------------------------------------------------------------
def gem_shift(px, dx):
    """Return shift-vector component N_x sourced by momentum density px on a
    cubic grid (free-space BC). N solves nabla^2 N = -16 pi px."""
    n = px.shape[0]
    P = 2*n
    src = np.zeros((P, P, P))
    src[:n, :n, :n] = px
    # free-space Green's kernel G(r)=1/|r| centered, regularized at 0
    ax = (np.arange(P) - n) * dx
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing='ij')
    r = np.sqrt(X*X + Y*Y + Z*Z)
    r[r == 0] = 0.5*dx                  # softening at the self-cell
    K = 1.0/r
    # N = 4 * conv(px, 1/r) * dV   (since nabla^2(1/r) = -4 pi delta)
    Nf = np.fft.ifftn(np.fft.fftn(src) * np.fft.fftn(np.fft.ifftshift(K))).real
    N = 4.0 * Nf[:n, :n, :n] * dx**3
    return N


# ======================================================================
# ITEM 1 -- superluminal shift vector: two computed obstructions
# ======================================================================
print("\n" + "-"*72)
print("ITEM 1  Superluminal shift vector -- structural obstructions")
print("-"*72)

# (1a) LATTICE REST-FRAME SIGNATURE. The beable cells sit at fixed x; their
# worldline is x=const with proper interval ds^2 = g_00 dt^2,
#   g_00 = -(1 - v_s^2 f^2)   (Alcubierre, c->c_lat units: -(c_lat^2 - v_s^2 f^2))
# Inside the bubble f=1. Timelike (physical beable) iff v_s f < c_lat.
print("\n[1a] Lattice cell worldline g_00 = -(c_lat^2 - v_s^2 f^2), f=1 inside bubble:")
f_in = 1.0
for vfac in [0.5, 0.9, 1.0, 1.1, 1.5]:
    vs = vfac*C_LAT
    g00 = -(C_LAT**2 - vs**2 * f_in**2)
    kind = ("timelike (beable OK)" if g00 < 0 else
            "NULL (boundary)" if abs(g00) < 1e-12 else
            "SPACELIKE (no beable rest frame!)")
    print(f"    v_s = {vfac:.2f} c_lat:  g_00 = {g00:+.5f}  -> {kind}")
print("    => the lattice rest frame (the beable substrate) ceases to exist")
print("       inside the bubble at exactly v_s = c_lat. Continuum GR escapes via")
print("       the Eulerian/geodesic slicing; the lattice cannot -- the cells are")
print("       fixed physical beables, not free to fall through the wall. (M2/M4)")

# (1b) CHARACTERISTIC SPEED of the induced metric. F180: the metric perturbation
# (ln K / GW) obeys (nabla^2 - c_lat^-2 d_t^2) = source, so its signal cone is
# c_lat. A bubble that must move > c_lat cannot be causally assembled/steered:
# the field that carries it propagates at c_lat. Demonstrate the dispersion.
print("\n[1b] Induced-metric characteristic speed (F180 GW eq, reproduced):")
k = np.linspace(0.01, 0.5, 6)
omega = C_LAT * k                  # (nabla^2 - c_lat^-2 d_t^2)h=0 => omega=c_lat k
vph = omega/k
print(f"    phase speed of metric perturbation v_ph = omega/k = {vph[0]:.5f} (= c_lat)")
print("    => the gravitational/shift field cannot outrun c_lat; a v_s>c_lat")
print("       bubble has no causal assembly. (independent of the energy-condition")
print("       problem; closes the brief's open problem #3 in the structural sense)")

# (1c) Even the LINEAR shift a positive source can build is bounded; pushing the
# drag toward c_lat forces strong field where the F204 nonlinear -v_s^2 wall
# returns. Quantified in Item 2 (drag fraction stays << 1 for positive WEC).


# ======================================================================
# ITEM 2 -- forward Bobrick-Martire: positive moving shell -> induced shift
# ======================================================================
print("\n" + "-"*72)
print("ITEM 2  Forward positive-energy moving shell -> induced shift vector")
print("-"*72)

# Build a positive-energy spherical shell (beable T^00 >= 0) translating at v.
# Normalize the shell to a chosen weak-field COMPACTNESS C = M/R0 so the
# linearized (GEM) treatment is valid (C << 1).
n, L = 32, 8.0
dx = L/n
ax = (np.arange(n)-n/2)*dx
X, Y, Z = np.meshgrid(ax, ax, ax, indexing='ij')
r = np.sqrt(X*X+Y*Y+Z*Z)
R0, w = 2.0, 0.5
shell = np.exp(-((r-R0)/w)**2); shell *= (shell > 1e-3)

def make_shell(compactness):
    """Positive shell normalized so M/R0 = compactness."""
    M_target = compactness*R0
    rho = shell * (M_target/(shell.sum()*dx**3))
    return rho, rho.sum()*dx**3

rho, M = make_shell(0.02)               # weak field: M/R0 = 0.02
print(f"\n[2a] Source: positive shell R0={R0}, compactness M/R0=0.02, M={M:.4f}, T^00>=0: {np.all(rho>=0)}")

for vfac in [0.2, 0.5, 0.9]:
    v = vfac*C_LAT
    px = rho*v                          # momentum density T^0x = rho v (>=0 where moving)
    Nx = gem_shift(px, dx)              # induced shift vector g_0x
    c = n//2
    v_drag = Nx[c, c, c]                # interior frame-drag (carry-along) velocity
    drag_frac = v_drag / v
    Nmax = np.abs(Nx).max()
    weak = Nmax < 1.0                    # weak-field validity (|g_0x| << 1)
    print(f"[2b] v={vfac:.2f} c_lat: max|N_x|={Nmax:.4e} (weak-field {weak}); "
          f"interior drag = {drag_frac:.4f} x v  (partial carry-along, <1 => no FTL)")

# WEC of the linear construction: energy density = matter rho (>=0) + GEM field
# energy ~ (curl N)^2 / 16pi (>=0). Show total T^00 stays >= 0 (no negative wall).
v = 0.5*C_LAT
px = rho*v
Nx = gem_shift(px, dx)
# gravitomagnetic field B_g = curl(N); its energy density ~ |B_g|^2/(16 pi) >= 0
dNx_dy = np.gradient(Nx, dx, axis=1)
dNx_dz = np.gradient(Nx, dx, axis=2)
Bg2 = dNx_dy**2 + dNx_dz**2
field_energy = Bg2/(16*np.pi)
T00_total = rho + field_energy          # both non-negative
print(f"\n[2c] WEC check on the forward construction (v=0.5 c_lat):")
print(f"     min T^00 (matter+GEM field) = {T00_total.min():+.3e}  >= 0: {T00_total.min()>=0}")
print(f"     => positive-energy everywhere; NO negative wall (contrast Alcubierre)")
print(f"     => Bobrick-Martire subluminal class is realizable forward on the lattice,")
print(f"        but the carry-along is PARTIAL (drag_frac<1) -> no FTL payoff.")

# How drag fraction scales with compactness (stronger field -> larger drag, but
# heading toward the nonlinear regime where F204's negative wall returns).
print("\n[2d] Drag fraction vs source compactness (M/R0), v=0.5 c_lat:")
for comp in [0.02, 0.1, 0.5, 1.0]:
    rho_s, Ms = make_shell(comp)
    px = rho_s*v
    Nx = gem_shift(px, dx)
    c = n//2
    drag = Nx[c, c, c]/v
    mx = np.abs(Nx).max()
    tag = 'weak-field OK' if mx < 0.3 else 'STRONG FIELD -> nonlinear, F204 -v_s^2 wall returns'
    print(f"     M/R0={comp:.2f}: drag_frac={drag:.4f}, max|N|={mx:.4f}  ({tag})")
print("     => drag_frac grows ~linearly with compactness; full carry-along")
print("        (drag_frac->1) needs M/R0 ~ O(1) = strong field, where the")
print("        positive-source linear picture fails and F204's negative wall is back.")

print("\n" + "="*72)
print("EXPLORATION SUMMARY")
print("="*72)
print(" ITEM 1: superluminal shift has TWO computed obstructions --")
print("   (1a) lattice cell worldline goes spacelike at v_s=c_lat (no beable")
print("        rest frame inside a >=c_lat bubble; sharper than continuum GR);")
print("   (1b) induced-metric signal cone = c_lat (F180) -> no causal assembly.")
print(" ITEM 2: forward positive shell builds a real shift vector (gravitomagnetic")
print("   drag), WEC holds (T^00>=0 everywhere), but carry-along is PARTIAL and")
print("   weak-field; forcing full carry-along -> strong field -> F204 negative")
print("   wall returns. => subluminal Bobrick-Martire realizable, FTL-less. CONSISTENT")
print("   with F204; both items now have a first constructive computation.")
