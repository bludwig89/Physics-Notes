# F135 — Real-time wave-packet dynamics under block-spin coarse-graining

Massive 2D exact-QCA Dirac packet (ca_dirac). Coarse rule Omega_coarse(q)=b*omega(q/b); 1 coarse tick = b fine ticks.


## RT1. Faithfulness: R_b o evolve_fine^{bN} == evolve_coarse^N o R_b (tracked every coarse tick)

- b=2: L 48->24, 12 fine vs 6 coarse ticks; max rel residual over trajectory = 1.42e-15
- b=3: L 48->16, 18 fine vs 6 coarse ticks; max rel residual over trajectory = 2.52e-15
- gate (< 1e-9 at every tick): PASS

## RT2. Group velocity invariant (packet moves)

- v_fine = 0.532961 cells/tick;  v_coarse = 0.531727 (physical); moves: PASS; agree<5e-3: PASS

## RT3. Dispersive spreading invariant (packet spreads)

- d(rms)_fine = 0.0672 cells;  d(rms)_coarse = 0.0679 (in fine cells); spreads: PASS; agree: PASS

## RT4. Mass is the RELEVANT operator (rest-gap eigenvalue = b)

- m=0.1: gap=arcsin(m)=0.100167; eigenvalues (b=2,3,4) = [2.0, 3.0, 4.0] (= b); physical Compton wavelength invariant
- m=0.25: gap=arcsin(m)=0.252680; eigenvalues (b=2,3,4) = [2.0, 3.0, 4.0] (= b); physical Compton wavelength invariant
- m=0.5: gap=arcsin(m)=0.523599; eigenvalues (b=2,3,4) = [2.0, 3.0, 4.0] (= b); physical Compton wavelength invariant
- gap eigenvalue == b and lambda_phys invariant to 1e-12: PASS
- Contrast: c_lat marginal (eigenvalue 1, F129/F130-T1); LIV irrelevant (b^-n, F130-T2); mass relevant (b), like string tension (F130-C1).

## RT5. Norm conserved (unitarity survives R_b)

- fine norm drift = 7.77e-16; coarse norm drift = 2.22e-16: PASS

## Summary: 5/5 PASS

