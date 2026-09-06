import sys, os
ROOT = "/sessions/rcw-01knjcldc3ziujwecvbejtmh/mnt/AI--Physics Notes"
sys.path.insert(0, os.path.join(ROOT, "src"))
from casim.engine.interactions import ns_eos as e
import numpy as np

def scan(name, n=80):
    s = e.summarize(e.PiecewisePolytrope(name), n=n)
    c = s["curve"]; i = int(np.argmax(c["M_msun"]))
    Ms, Rs = c["M_msun"][:i+1], c["R_km"][:i+1]
    R1418 = float(np.interp(1.418, Ms, Rs)) if Ms.max() >= 1.418 else None
    return s["M_max"], R1418

for name in ["SLy","APR","MPA1","WFF1","MS1"]:
    Mmax, R1418 = scan(name)
    print(f"{name:6s} Mmax={Mmax:.4f}  R(1.418)={R1418}")
