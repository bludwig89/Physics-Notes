# F129 — Block-spin RG for the free paired-photon sector

c_lat = 1/sqrt(3) = 0.577350269189626

R_b: average b^d cells, rescale space & time by b; coarse rule Omega_coarse(kappa) = Omega(kappa/b).


## A. Analytic block map (sympy, exact)

- block map  Omega_b(kappa) = b*Omega(kappa/b)  =>  [kappa^n] = a_n * b^(1-n)  : PASS
- c_lat (n=1) coefficient invariant (eigenvalue 1): PASS
- even-law body-diagonal a_1 = 0.577350269189626  (= 1/sqrt3: PASS)
- even-law body-diagonal a_3 = -sqrt(3)/486  (= -1/(162 sqrt3), matches F30 dv/c=-k^2/54: PASS)
- leading correction is kappa^3 in Omega -> eigenvalue b^(1-3)=b^-2 (irrelevant).

## T1. c_lat is an RG fixed point  (b * c_coarse(b) = 1/sqrt3)

- axis:  [np.float64(0.57735026919), np.float64(0.577350269189), np.float64(0.577350269188), np.float64(0.577350269193), np.float64(0.577350269189)]  : PASS
- body:  [np.float64(0.577350269196), np.float64(0.577350269194), np.float64(0.577350269192), np.float64(0.577350269202), np.float64(0.577350269181)]

## T2. LIV operators are irrelevant  (eigenvalue b^-2)

- b=2: measured 0.2500000000  vs  b^-2 0.2500000000
- b=3: measured 0.1111111111  vs  b^-2 0.1111111111
- b=4: measured 0.0625000000  vs  b^-2 0.0625000000
- b=5: measured 0.0400000000  vs  b^-2 0.0400000000
- leading g2(body) = -0.0061728416  (= -1/162 = -0.0061728395: PASS)

## K. Anti-alias: box form factor D_b zero at fold points 2*pi*m/b

- max |D_b(fold)| over b=2..5 = 1.67e-16  : PASS

## RS. Real-space faithfulness: R_b o evolve_fine^{bN} == evolve_coarse^N o R_b

- b=2: L 24->12, 16 fine vs 8 coarse ticks, rel residual = 5.54e-15
- b=3: L 24->8, 24 fine vs 8 coarse ticks, rel residual = 1.25e-14
- band-limited gate (residual < 1e-9): PASS
- residual across resolved band (b=2, modes < coarse Nyquist): {'2': 5.540348977272516e-15, '4': 7.052370244444033e-15, '5': 4.91576900330103e-15}

## V. Measured rotation rate of a planted on-axis mode (genuine evolution)

- fine:   Omega/|k| = 0.577350269189631  (c_lat = 0.577350269189626)
- coarse: Omega/|q| = 0.577350269189626  (same physical speed, b=2)
- both = 1/sqrt3 to 1e-9: PASS

## Summary: 5/5 PASS

