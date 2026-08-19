# d=4 confinement on the genuine BCC lattice

Generated 2026-08-17 - 21:44 in 6.59 s.

Lattice `BCC_3 spatial x Z Euclidean time`, shape (6, 6, 6, 6), SU(3), 324 genuine BCC sites, 10 plaquettes per site (6 rhombi + 4 mixed rectangles).
beta_s = 5.9, beta_t = 23.6; xi = 1.732051 = 1/c_lat, beta_t/beta_s derived 4 = 4/3 x xi^2 (the 4/3 is BCC geometry).
Anisotropy source: derived: beta_t/beta_s = 4 lambda^2/a_t^2 = 4/(3 c_lat^2) = 4, xi = 1/c_lat = 1.732051.

Mean plaquette: spatial 0.799799, temporal 0.896906.
|Polyakov| = 0.757807. Unitarity residual 7.77e-16.

## Wilson loops

| R x T | W | err |
|---|---:|---:|
| 1 x 1 | 0.896906 | 0.000637 |
| 1 x 2 | 0.838163 | 0.001137 |
| 1 x 3 | 0.795353 | 0.001711 |
| 2 x 1 | 0.813948 | 0.001174 |
| 2 x 2 | 0.730850 | 0.001649 |
| 2 x 3 | 0.681127 | 0.002098 |
| 3 x 1 | 0.739325 | 0.001662 |
| 3 x 2 | 0.639453 | 0.002148 |
| 3 x 3 | 0.588666 | 0.002479 |

## Creutz ratios  chi(R,T)

| R x T | chi |
|---|---:|
| 2 x 2 | 0.039951 |
| 2 x 3 | 0.018032 |
| 3 x 2 | 0.037436 |
| 3 x 3 | 0.012296 |

## F299 d=4 Casimir successor

3 configs; character polynomials verified against explicit rep matrices at 3.38e-16.

| R x T | sigma_6/sigma_3 | 5/2 | sigma_8/sigma_3 | 9/4 | sigma_10/sigma_3 | 9/2 |
|---|---:|---:|---:|---:|---:|---:|
| 2 x 2 | 2.4660 | 2.5 | 2.2243 | 2.25 | 4.3776 | 4.5 |
| 2 x 3 | 2.6450 | 2.5 | 2.3196 | 2.25 | 5.1413 | 4.5 |
| 3 x 2 | 2.5091 | 2.5 | 2.2351 | 2.25 | 4.6677 | 4.5 |
| 3 x 3 | 2.2838 | 2.5 | 2.1388 | 2.25 | 3.6318 | 4.5 |

4 usable (R,T) row(s); 0 (rep,R,T) Creutz ratio(s) undefined -- see `dropped`

Casimir scaling is expected at INTERMEDIATE R only. The triality-0 reps 8 and 10 must fall below the Casimir line asymptotically once the string breaks; locating that is why d=4 was asked for and d=2 could not answer.

## Scope

Wilson loops and Creutz ratios on the model's own BCC action, and (with --casimir) F299's d=4 higher-rep successor. NOT a claim of an area law or a string tension: row B7's residual is a missing transfer matrix with positivity, which no amount of sampling supplies. The anisotropy IS derived (see couplings.source); what is not derived is the radiative correction to it -- the Karsch coefficients of the hypercubic literature -- since the matching here is tree level.
