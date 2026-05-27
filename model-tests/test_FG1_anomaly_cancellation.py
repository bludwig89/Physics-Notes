"""
FG-1 — Anomaly cancellation across a single first-generation Standard-Model
       chiral fermion content, in the GUT/Ludwig convention Q = T_3 + Y/2.

Specced in first-gen-completeness-review.md §5.1:
    "Anomaly cancellation across the generation:
     sum Y = 0, sum Y^3 = 0, SU(2)^2-U(1), SU(3)^2-U(1), grav-U(1)"

This is a Tier-1 algebraic test. All arithmetic is done with
fractions.Fraction so every result is an exact rational; 0 means 0,
not "< 1e-17". We additionally compute the pure SU(2)^3 and SU(3)^3
anomaly coefficients, which the SM relies on but which the review's
shorthand list does not call out explicitly.

Hypercharge convention (Q = T_3 + Y/2), as used in the review's table:

    Particle     SU(3)_c     SU(2)_L     Y         Q
    -----------  ----------  ----------  --------  ----------
    L=(nu, e)_L  1           2           -1        ( 0, -1)
    e_R          1           1           -2         -1
    Q=(u, d)_L   3           2           +1/3      (+2/3, -1/3)
    u_R          3           1           +4/3       +2/3
    d_R          3           1           -2/3       -1/3

For anomaly bookkeeping every fermion is rewritten as a left-handed
Weyl fermion; right-handed Dirac components become charge-conjugate
left-handed Weyls with the SU(3) rep dualised and Y flipped in sign:

    e_R   ->  e^c_L  :  (1,    1, +2 )
    u_R   ->  u^c_L  :  (3bar, 1, -4/3)
    d_R   ->  d^c_L  :  (3bar, 1, +2/3)

The Standard-Model anomaly-cancellation conditions then read:

    (A) [grav]^2 . U(1)_Y       :  sum Y           = 0
    (B) U(1)_Y^3                 :  sum Y^3         = 0
    (C) [SU(2)_L]^2 . U(1)_Y    :  sum T(R_2) Y    = 0   (over SU(2) doublets)
    (D) [SU(3)_c]^2 . U(1)_Y    :  sum T(R_3) Y    = 0   (over color (anti)triplets)
    (E) [SU(2)_L]^3              :  identically zero (SU(2) reps pseudo-real)
    (F) [SU(3)_c]^3              :  sum A(R_3)     = 0   (3 contributes +1, 3bar -1)

Dynkin indices used:  T(fundamental of SU(N)) = 1/2,
                      T(antifund. of SU(N))   = 1/2,
                      A(3) = +1, A(3bar) = -1.

Multiplicity of each Weyl in a trace is dim(other reps) (e.g. a colour
triplet that is also part of an SU(2) doublet enters the SU(3)^2-U(1)
sum with weight 2 because there are two such triplets, one for each
doublet component).

Run with:  python3 model-tests/test_FG1_anomaly_cancellation.py
JSON dump: test-results/FG1_anomaly_cancellation.json
"""

from __future__ import annotations
from fractions import Fraction
from dataclasses import dataclass, asdict
from typing import Optional
import json
import os
import sys
from datetime import datetime


# --------------------------------------------------------------------------
# Field content (one generation, left-handed Weyl basis)
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Weyl:
    """A single left-handed Weyl fermion species in one SM generation."""
    name: str
    color: str          # '1', '3', or '3bar'
    isospin: int        # SU(2)_L dimension (1 = singlet, 2 = doublet)
    Y: Fraction         # hypercharge in the Q = T_3 + Y/2 convention

    @property
    def color_dim(self) -> int:
        return {'1': 1, '3': 3, '3bar': 3}[self.color]

    @property
    def multiplicity(self) -> int:
        """Number of Weyl components contributing to gauge/grav traces."""
        return self.color_dim * self.isospin


# Color Dynkin index T(R) and pure-SU(3) anomaly coefficient A(R).
T_SU3 = {'1': Fraction(0), '3': Fraction(1, 2), '3bar': Fraction(1, 2)}
A_SU3 = {'1': 0,           '3': +1,             '3bar': -1}
# SU(2): T(doublet) = 1/2, T(singlet) = 0.  SU(2)^3 anomaly identically zero.
T_SU2 = {1: Fraction(0), 2: Fraction(1, 2)}


GENERATION: list[Weyl] = [
    Weyl('L_L  (nu_L, e_L)', color='1',    isospin=2, Y=Fraction(-1)),
    Weyl('e^c_L  ( = e_R conj )',         color='1',    isospin=1, Y=Fraction(+2)),
    Weyl('Q_L  (u_L, d_L)',               color='3',    isospin=2, Y=Fraction(+1, 3)),
    Weyl('u^c_L ( = u_R conj )',          color='3bar', isospin=1, Y=Fraction(-4, 3)),
    Weyl('d^c_L ( = d_R conj )',          color='3bar', isospin=1, Y=Fraction(+2, 3)),
]


# --------------------------------------------------------------------------
# Electric-charge cross-check  Q = T_3 + Y/2
# --------------------------------------------------------------------------

def physical_charges() -> dict[str, Fraction]:
    """Return Q for each *physical* (right-handed-as-itself) particle."""
    half = Fraction(1, 2)
    charges = {
        'nu_e':   Fraction(0)  + Fraction(-1)/2,         # T_3=+1/2 in L
        'e_L':    -half        + Fraction(-1)/2,         # T_3=-1/2 in L
        'e_R':    Fraction(0)  + Fraction(-2)/2,         # T_3= 0
        'u_L':    +half        + Fraction(+1, 3)/2,
        'd_L':    -half        + Fraction(+1, 3)/2,
        'u_R':    Fraction(0)  + Fraction(+4, 3)/2,
        'd_R':    Fraction(0)  + Fraction(-2, 3)/2,
    }
    # Re-do with explicit T_3 to be unambiguous:
    return {
        'nu_e_L':  half  + Fraction(-1)/2,
        'e_L':    -half  + Fraction(-1)/2,
        'e_R':     0     + Fraction(-2)/2,
        'u_L':    +half  + Fraction(+1, 3)/2,
        'd_L':    -half  + Fraction(+1, 3)/2,
        'u_R':     0     + Fraction(+4, 3)/2,
        'd_R':     0     + Fraction(-2, 3)/2,
    }


# --------------------------------------------------------------------------
# Anomaly traces
# --------------------------------------------------------------------------

def anomaly_grav_U1(gen: list[Weyl]) -> Fraction:
    """[grav]^2 . U(1)_Y :  sum_i n_i Y_i ."""
    return sum((w.multiplicity * w.Y for w in gen), Fraction(0))


def anomaly_U1_cubed(gen: list[Weyl]) -> Fraction:
    """U(1)_Y^3 :  sum_i n_i Y_i^3 ."""
    return sum((w.multiplicity * w.Y ** 3 for w in gen), Fraction(0))


def anomaly_SU2sq_U1(gen: list[Weyl]) -> Fraction:
    """[SU(2)_L]^2 . U(1)_Y :  sum_i color_dim_i T(R2_i) Y_i ."""
    return sum(
        (w.color_dim * T_SU2[w.isospin] * w.Y for w in gen),
        Fraction(0),
    )


def anomaly_SU3sq_U1(gen: list[Weyl]) -> Fraction:
    """[SU(3)_c]^2 . U(1)_Y :  sum_i isospin_i T(R3_i) Y_i ."""
    return sum(
        (w.isospin * T_SU3[w.color] * w.Y for w in gen),
        Fraction(0),
    )


def anomaly_SU3_cubed(gen: list[Weyl]) -> Fraction:
    """[SU(3)_c]^3 :  sum_i isospin_i A(R3_i) ."""
    return sum(
        (Fraction(w.isospin * A_SU3[w.color]) for w in gen),
        Fraction(0),
    )


def anomaly_SU2_cubed(_: list[Weyl]) -> Fraction:
    """[SU(2)_L]^3 :  identically zero (SU(2) reps are pseudo-real)."""
    return Fraction(0)


ANOMALIES = [
    ('grav^2_U1',    anomaly_grav_U1,    '[grav]^2 . U(1)_Y'),
    ('U1_cubed',     anomaly_U1_cubed,   'U(1)_Y^3'),
    ('SU2sq_U1',     anomaly_SU2sq_U1,   '[SU(2)_L]^2 . U(1)_Y'),
    ('SU3sq_U1',     anomaly_SU3sq_U1,   '[SU(3)_c]^2 . U(1)_Y'),
    ('SU3_cubed',    anomaly_SU3_cubed,  '[SU(3)_c]^3'),
    ('SU2_cubed',    anomaly_SU2_cubed,  '[SU(2)_L]^3'),
]


# --------------------------------------------------------------------------
# Per-particle breakdown (so the JSON / report shows *where* it cancels)
# --------------------------------------------------------------------------

def per_particle_breakdown(gen: list[Weyl]) -> dict:
    rows = []
    for w in gen:
        rows.append({
            'name': w.name,
            'color': w.color,
            'isospin_dim': w.isospin,
            'Y': str(w.Y),
            'multiplicity_n': w.multiplicity,
            'n_Y': str(w.multiplicity * w.Y),
            'n_Y^3': str(w.multiplicity * w.Y ** 3),
            'SU2sq_term  (cdim . T2 . Y)':
                str(w.color_dim * T_SU2[w.isospin] * w.Y),
            'SU3sq_term  (i . T3 . Y)':
                str(w.isospin * T_SU3[w.color] * w.Y),
            'SU3^3_term  (i . A3)':
                str(w.isospin * A_SU3[w.color]),
        })
    return {'particles': rows}


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def run() -> dict:
    results = {}
    all_zero = True
    for key, fn, label in ANOMALIES:
        val = fn(GENERATION)
        ok = (val == 0)
        all_zero &= ok
        results[key] = {
            'label': label,
            'value': str(val),
            'is_zero_exact': ok,
        }

    # Q = T_3 + Y/2 cross-check
    qs = physical_charges()
    charge_check = {name: str(q) for name, q in qs.items()}

    return {
        'test': 'FG-1',
        'name': 'First-generation anomaly cancellation',
        'tier': 'Tier 1 (algebraic, exact rationals)',
        'spec_source': 'first-gen-completeness-review.md  Section 5.1 / Section 2.3',
        'convention': 'Q = T_3 + Y/2  (review Section 1 table)',
        'date': datetime.now().strftime('%Y-%m-%d - %H:%M'),
        'all_anomalies_cancel_exactly': all_zero,
        'anomalies': results,
        'gell_mann_nishijima_charges': charge_check,
        'breakdown': per_particle_breakdown(GENERATION),
    }


def main(argv: list[str]) -> int:
    out = run()

    # Console summary
    print('=' * 72)
    print('FG-1  First-generation anomaly cancellation  (exact rationals)')
    print('=' * 72)
    print(f"Date: {out['date']}")
    print(f"Convention: {out['convention']}")
    print()
    print(f"{'Anomaly':28s}  {'sum':>10s}   exact zero?")
    print('-' * 60)
    for key, fn, label in ANOMALIES:
        v = out['anomalies'][key]
        print(f"  {label:26s}  {v['value']:>10s}   {v['is_zero_exact']}")
    print()
    print('Q = T_3 + Y/2  cross-check:')
    for name, q in out['gell_mann_nishijima_charges'].items():
        print(f"  Q({name:7s}) = {q}")
    print()
    print('ALL ANOMALIES CANCEL EXACTLY:',
          out['all_anomalies_cancel_exactly'])
    print('=' * 72)

    # JSON dump
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)
    out_dir = os.path.join(repo, 'test-results')
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, 'FG1_anomaly_cancellation.json')
    with open(json_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"Wrote results -> {json_path}")

    return 0 if out['all_anomalies_cancel_exactly'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
