import sys, os
ROOT = "/sessions/rcw-01knjcldc3ziujwecvbejtmh/mnt/AI--Physics Notes"
sys.path.insert(0, os.path.join(ROOT, "src"))
from casim.engine.interactions import ns_eos as e
import numpy as np

eos = e.PiecewisePolytrope("SLy")
rho_c = 1.2e15  # near turnover-ish density
for h in [100.0, 250.0, 500.0, 1000.0, 2000.0]:
    R, M, z = e.integrate_tov(eos, rho_c, h_cm=h)
    print(f"h={h:7.1f}  R={R:.5f} km  M={M:.5f} Msun  z={z:.5f}")
