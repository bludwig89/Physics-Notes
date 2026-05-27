# F30 — Leading photon-dispersion correction order (BCC vacuum)

c_lat = 1/sqrt(3) = 0.5773502692

Photon: Omega^pm(k) = 2 arccos( cx cy cz pm sx sy sz ), ci=cos((ki/2)/sqrt3)

delta v_phi/c = Omega^+/(c_lat k) - 1


## (1,0,0) axis  (n_hat=(1, 0, 0))

- Omega^+(k) = `sqrt(3)*k/3`
- c_lat coefficient (k^1): `sqrt(3)/3`  (expect 1/sqrt3)
- leading correction: **none — exactly linear, no LIV in this direction**
- numeric log-log slope of residual: -0.7083 (independent confirmation of correction order in Omega)
- birefringence: 0
- unpolarised time-of-flight (chirality-even): no correction
- birefringence (chirality-odd): 0

## (1,1,0) face-diagonal  (n_hat=(1, 1, 0))

- Omega^+(k) = `-7*sqrt(3)*k**5/829440 - sqrt(3)*k**3/864 + sqrt(3)*k/3`
- c_lat coefficient (k^1): `sqrt(3)/3`  (expect 1/sqrt3)
- leading correction to Omega: `-sqrt(3)/864 * k^3`
- **delta v_phi/c = `-1/288 * k^2`  ->  n_LIV = 2**
- numeric log-log slope of residual: 3.0000 (independent confirmation of correction order in Omega)
- birefringence: 0
- **unpolarised time-of-flight** (chirality-even): delta v/c = `-1/288 * k^2`  -> n_LIV = 2
- birefringence (chirality-odd): 0

## (1,1,1) body-diagonal  (n_hat=(1, 1, 1))

- Omega^+(k) = `-sqrt(3)*k**5/787320 - sqrt(3)*k**4/8748 - sqrt(3)*k**3/486 - sqrt(3)*k**2/54 + sqrt(3)*k/3`
- c_lat coefficient (k^1): `sqrt(3)/3`  (expect 1/sqrt3)
- leading correction to Omega: `-sqrt(3)/54 * k^2`
- **delta v_phi/c = `-1/18 * k^1`  ->  n_LIV = 1**
- numeric log-log slope of residual: 2.0020 (independent confirmation of correction order in Omega)
- birefringence Omega^+ - Omega^- leading term: `-sqrt(3)/27 * k^2`
- **unpolarised time-of-flight** (chirality-even): delta v/c = `-1/162 * k^2`  -> n_LIV = 2
- **birefringence** (chirality-odd): delta v/c split = `-1/18 * k^1`  -> n_LIV = 1

## Energy mapping (Planck-tick assumption)

With tick = Planck time and spacing = Planck length, dimensionless lattice k maps to
k = sqrt(3) * E/E_P (since Omega = c_lat k and E = hbar*Omega/tau).
Along (1,1,1): delta v_g/c = -k/9 = -(sqrt3/9)(E/E_P) ~ -0.1925 (E/E_P),
i.e. an effective linear-LIV scale E_QG,1 ~ E_P/0.1925 ~ 5.2 E_P (subluminal).
