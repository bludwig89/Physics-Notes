"""casim.engine.core.entanglement_register — the live genuine-many-body entanglement channel.

Every other casim sector is first-quantised / mean-field: a product of single-cell
amplitudes, Hilbert dimension ~O(cells), zero entanglement by construction
(``ca_manybody`` Hartree, the QM-1 CHSH hand-inserted "singlet").  This channel
is the exception — a genuine 2ⁿ tensor-product register (F212) wired into the
engine so multi-cell entanglement is **generated live**, tick by tick, at the
rate DERIVED from the ``ca_dirac`` hopping (F214 super-exchange).

Qubits sit on ``n`` designated lattice cells.  The state is the full 2ⁿ
amplitude vector, initialised as a PRODUCT (no entanglement supplied).  Each
tick applies the native spinor-exchange gate ``exp(−iθ σ_A·σ_B)`` to nearest-
neighbour cell pairs, with ``θ = J/4`` the derived per-tick entangling angle
(``ca_entanglement.exchange_angle_per_tick(m)``).  The ``EntanglementEntropy``
observer records the von Neumann entropy rising from 0 — the substrate
generating entanglement it was not given, now as a first-class engine run.
"""
from __future__ import annotations

import numpy as np

from .channel import Channel, register
from .observers import Observer, register_observer


def _E():
    """Lazy handle to the ca_entanglement kernel (via the fields wrapper)."""
    from casim.fields.entanglement import ca_entanglement as E
    if E is None:  # pragma: no cover
        raise RuntimeError("ca_entanglement kernel not importable")
    return E


def _init_product(E, n, kind):
    """Build a PRODUCT initial state vector (never entangled)."""
    if kind == "neel":                       # |0101…⟩ — classic AFM product
        kets = [E.KET0 if i % 2 == 0 else E.KET1 for i in range(n)]
    elif kind == "plus_first":               # |+00…⟩
        kets = [E.KETP] + [E.KET0] * (n - 1)
    elif kind == "all_up":                   # |00…⟩ (exchange-invariant control)
        kets = [E.KET0] * n
    elif kind == "all_plus":                 # |++…⟩
        kets = [E.KETP] * n
    else:
        raise ValueError(f"unknown init {kind!r}")
    return E.product_state(kets)


def _chain_pairs(n):
    return [(i, i + 1) for i in range(n - 1)]


@register
class EntanglementRegisterChannel(Channel):
    """A live 2ⁿ many-body register entangled by the derived spinor-exchange gate.

    Config
    ------
    n_qubits : int   number of qubits / cells (default 2)
    m        : float mass setting the derived exchange rate θ=J/4 (default 0.5)
    init     : str   product initial state: "neel"|"plus_first"|"all_up"|"all_plus"
    theta_per_tick : float  optional override of the derived per-tick angle
    cut      : list  subsystem qubits for the entropy observable (default [0])
    """
    type_name = "entanglement_register"
    label = "Entanglement Register"
    propagator = "even"           # exchange is branch-blind / permutation-symmetric
    topologies = ("cubic", "bcc")  # register is lattice-agnostic; qubits on n cells

    def init_state(self, lattice, rng):
        E = _E()
        n = int(self.config.get("n_qubits", 2))
        m = float(self.config.get("m", 0.5))
        init = str(self.config.get("init", "neel"))
        theta = self.config.get("theta_per_tick", None)
        theta = float(theta) if theta is not None else E.exchange_angle_per_tick(m)
        cut = list(self.config.get("cut", [0]))
        psi = _init_product(E, n, init)
        return {
            "psi": np.asarray(psi, dtype=complex),
            "n": n,
            "m": m,
            "theta": float(theta),
            "cut": np.asarray(cut, dtype=np.int64),
        }

    def step(self, state, lattice, context=None, rng=None):
        E = _E()
        n = int(state["n"])
        theta = float(state["theta"])
        gate = E.exchange_gate(theta)
        psi = state["psi"]
        for (q0, q1) in _chain_pairs(n):      # one brick-wall sweep of exchange
            psi = E.apply_gate(psi, gate, [q0, q1], n)
        out = dict(state)
        out["psi"] = psi
        return out

    def energy(self, state) -> float:
        return float(np.vdot(state["psi"], state["psi"]).real)   # norm² (≡1)

    # --- optional observer hook -------------------------------------------
    def observables(self, state, lattice) -> dict:
        E = _E()
        n = int(state["n"])
        psi = state["psi"]
        cut = [int(x) for x in np.asarray(state["cut"]).tolist()]
        S_cut = E.entropy_of_vector(psi, n, cut)
        S_single = [E.entropy_of_vector(psi, n, [q]) for q in range(n)]
        # purity of the cut subsystem
        keep = cut
        t = psi.reshape([2] * n)
        traced = [ax for ax in range(n) if ax not in keep]
        M = np.transpose(t, keep + traced).reshape(2 ** len(keep), -1)
        rho = M @ M.conj().T
        purity = float(np.real(np.trace(rho @ rho)))
        return {
            "entropy_cut": float(S_cut),
            "entropy_single": [float(s) for s in S_single],
            "purity_cut": purity,
            "norm": float(np.vdot(psi, psi).real),
            "n_qubits": n,
            "theta_per_tick": float(state["theta"]),
        }

    # register carries its own (already-coarse) meaning; block-spin is a no-op
    def block_spin(self, state, lattice, b: int):
        return state

    def density_field(self, state):
        raise ValueError("entanglement_register has no spatial density field")


@register
class QuantumCircuitChannel(Channel):
    """Run a quantum ALGORITHM live through the engine, one circuit layer per tick.

    The program is a list of layers; each layer is a list of JSON gate specs
    ([kind, *params]) over the native gate set (h/x/z/rz/exch/cz/cnot — all
    compiled exactly from the exchange interaction + rotors, F218).  The state is
    the genuine 2ⁿ register.  Config:
        n_qubits : int
        program  : list of layers (JSON-serializable)
        init     : "all_up" (|0…0⟩, default)
    """
    type_name = "quantum_circuit"
    label = "Quantum Circuit"
    propagator = "even"
    topologies = ("cubic", "bcc")

    def init_state(self, lattice, rng):
        E = _E()
        n = int(self.config.get("n_qubits", 2))
        program = self.config.get("program", [])
        psi = E.product_state([E.KET0] * n)
        # store the program flat (JSON-safe) + a layer cursor
        return {"psi": np.asarray(psi, complex), "n": n,
                "program": program, "layer": 0}

    def step(self, state, lattice, context=None, rng=None):
        E = _E()
        prog = state["program"]
        i = int(state["layer"])
        out = dict(state)
        if i < len(prog):
            out["psi"] = E.apply_layer(state["psi"], prog[i], int(state["n"]))
            out["layer"] = i + 1
        return out

    def energy(self, state) -> float:
        return float(np.vdot(state["psi"], state["psi"]).real)

    def observables(self, state, lattice) -> dict:
        E = _E()
        probs = E.probabilities(state["psi"])
        top = int(np.argmax(probs))
        return {"probabilities": [float(p) for p in probs],
                "argmax": top, "p_argmax": float(probs[top]),
                "layer": int(state["layer"]), "n_layers": len(state["program"]),
                "norm": float(np.vdot(state["psi"], state["psi"]).real)}

    def block_spin(self, state, lattice, b: int):
        return state

    def density_field(self, state):
        raise ValueError("quantum_circuit has no spatial density field")


@register_observer
class CircuitReadoutObserver(Observer):
    """Record the computational-basis probabilities of every quantum_circuit
    channel per tick — the algorithm's live output as it executes."""
    name = "circuit_readout"
    label = "Circuit Readout"
    exactness = "quantitative"

    def observe(self, sim) -> None:
        for cname, ch in sim.channels.items():
            if not isinstance(ch, QuantumCircuitChannel):
                continue
            o = ch.observables(sim.states[cname], sim.lattice)
            self.records.append({"tick": sim.tick, "channel": cname,
                                 "argmax": o["argmax"], "p_argmax": o["p_argmax"],
                                 "layer": o["layer"], "probabilities": o["probabilities"]})

    def summary(self) -> dict:
        if not self.records:
            return {}
        last = self.records[-1]
        return {"final_argmax": last["argmax"], "final_p": last["p_argmax"],
                "final_probabilities": last["probabilities"]}


def _SQ():
    """Lazy handle to the second-quantization kernel.

    Migrated at roadmap C5: `ca_second_quant` -> `casim.engine.particles
    .second_quant`. Imported by STRING, so the C3.4 shim checker cannot see it
    — the path is spelled out here deliberately rather than left to the shim.
    """
    import importlib
    return importlib.import_module("casim.engine.particles.second_quant")


@register
class FermionChainChannel(Channel):
    """A genuine second-quantized spin-½ fermion chain (Hubbard) — field-native
    entanglement (F217).

    Unlike ``entanglement_register`` (an effective spin model), this channel
    evolves the full fermionic Fock state e^{−iH·tick} with H the Hubbard
    Hamiltonian built from Jordan–Wigner operators: hopping t (from ca_dirac) +
    on-site U (mass gap).  Two-site spin entanglement and the super-exchange J
    EMERGE from the real hopping + Pauli exclusion; the effective exchange gate
    is recovered only in the large-U limit.

    Config: n_sites (default 2), m (default 0.5), init ("neel").
    """
    type_name = "fermion_chain"
    label = "Fermion Chain (2nd-quantized)"
    propagator = "per-branch"      # genuine fermions (matter sector, F91)
    topologies = ("cubic", "bcc")

    def __init__(self, name=None, **config):
        super().__init__(name=name, **config)
        self._fc = None            # cached FermionChain (rebuilt on resume)
        self._prop = None          # cached one-tick propagator e^{−iH}

    def _chain(self, n_sites, t, U):
        if (self._fc is None or self._fc.n_sites != n_sites
                or abs(self._fc.t - t) > 1e-15 or abs(self._fc.U - U) > 1e-15):
            SQ = _SQ()
            self._fc = SQ.FermionChain(n_sites, t, U)
            w, V = np.linalg.eigh(self._fc.H)
            self._prop = (V * np.exp(-1j * w)) @ V.conj().T   # e^{−iH·1}
        return self._fc

    def init_state(self, lattice, rng):
        SQ = _SQ()
        from casim.engine.interactions import qi_entanglement as E
        n_sites = int(self.config.get("n_sites", 2))
        m = float(self.config.get("m", 0.5))
        init = str(self.config.get("init", "neel"))
        t, U = E.hopping_amplitude(m), E.mass_gap(m)
        fc = self._chain(n_sites, t, U)
        if init == "neel":
            psi = fc.neel_two_site() if n_sites == 2 else \
                fc.fock_state([fc.orb(s, s % 2) for s in range(n_sites)])
        else:
            raise ValueError(f"fermion_chain: unknown init {init!r}")
        return {"psi": np.asarray(psi, complex),
                "n_sites": n_sites, "m": m, "t": float(t), "U": float(U)}

    def step(self, state, lattice, context=None, rng=None):
        self._chain(int(state["n_sites"]), float(state["t"]), float(state["U"]))
        out = dict(state)
        out["psi"] = self._prop @ state["psi"]
        return out

    def energy(self, state) -> float:
        return float(np.vdot(state["psi"], state["psi"]).real)   # norm² (≡1)

    def observables(self, state, lattice) -> dict:
        fc = self._chain(int(state["n_sites"]), float(state["t"]), float(state["U"]))
        psi = state["psi"]
        S, w = fc.spin_entanglement(psi, 0, 1)
        return {
            "spin_entanglement": float(S),
            "one_per_site_weight": float(w),
            "double_occ_site0": fc.double_occupancy(psi, 0),
            "spin_corr_01": fc.spin_correlation(psi, 0, 1),
            "norm": float(np.vdot(psi, psi).real),
        }

    def block_spin(self, state, lattice, b: int):
        return state

    def density_field(self, state):
        raise ValueError("fermion_chain has no spatial density field")


@register
class FermionAlgorithmChannel(Channel):
    """Run a quantum ALGORITHM live on the genuine second-quantized Fock sector
    (F220) — computation on real matter, not an abstract register.

    A logical qubit is the SPIN of a singly-occupied site.  Single-qubit gates
    are exact fermionic operators; the two-qubit entangler is the GENUINE
    Hubbard time-evolution whose emergent super-exchange (F214/F217) realises the
    exchange gate in the large-U limit.  One circuit layer is applied per tick to
    the full 2^{2·n_sites} Fock state; the readout projects onto the one-per-site
    sector and reports the logical-register probabilities plus the leakage weight.

    Config: n_sites (default 2), m (default 0.9, sets U/t), program (JSON layers).
    """
    type_name = "fermion_algorithm"
    label = "Fermion Algorithm (field-native)"
    propagator = "per-branch"          # genuine fermions (matter sector, F91)
    topologies = ("cubic", "bcc")

    def __init__(self, name=None, **config):
        super().__init__(name=name, **config)
        self._fc = None

    def _chain(self, n_sites, t, U):
        if (self._fc is None or self._fc.n_sites != n_sites
                or abs(self._fc.t - t) > 1e-15 or abs(self._fc.U - U) > 1e-15):
            self._fc = _SQ().FermionChain(n_sites, t, U)
        return self._fc

    def init_state(self, lattice, rng):
        from casim.engine.interactions import qi_entanglement as E
        n_sites = int(self.config.get("n_sites", 2))
        m = float(self.config.get("m", 0.9))
        program = self.config.get("program", [])
        t, U = E.hopping_amplitude(m), E.mass_gap(m)
        fc = self._chain(n_sites, t, U)
        psi = fc.neel_two_site() if n_sites == 2 else \
            fc.fock_state([fc.orb(s, s % 2) for s in range(n_sites)])
        return {"psi": np.asarray(psi, complex), "n_sites": n_sites, "m": m,
                "t": float(t), "U": float(U), "program": program, "layer": 0}

    def step(self, state, lattice, context=None, rng=None):
        fc = self._chain(int(state["n_sites"]), float(state["t"]), float(state["U"]))
        prog = state["program"]
        i = int(state["layer"])
        out = dict(state)
        if i < len(prog):
            out["psi"] = fc.apply_program_fock(state["psi"], [prog[i]])
            out["layer"] = i + 1
        return out

    def energy(self, state) -> float:
        return float(np.vdot(state["psi"], state["psi"]).real)

    def observables(self, state, lattice) -> dict:
        fc = self._chain(int(state["n_sites"]), float(state["t"]), float(state["U"]))
        amps, w = fc.spin_register(state["psi"])
        probs = np.abs(amps) ** 2
        top = int(np.argmax(probs))
        return {"probabilities": [float(p) for p in probs], "argmax": top,
                "p_argmax": float(probs[top]), "one_per_site_weight": float(w),
                "layer": int(state["layer"]), "n_layers": len(state["program"]),
                "norm": float(np.vdot(state["psi"], state["psi"]).real)}

    def block_spin(self, state, lattice, b: int):
        return state

    def density_field(self, state):
        raise ValueError("fermion_algorithm has no spatial density field")


@register_observer
class FermionAlgorithmObserver(Observer):
    """Record the live logical-register readout of every fermion_algorithm
    channel per tick — a quantum algorithm executing on genuine matter (F220)."""
    name = "fermion_algorithm_readout"
    label = "Fermion Algorithm Readout"
    exactness = "quantitative"

    def observe(self, sim) -> None:
        for cname, ch in sim.channels.items():
            if not isinstance(ch, FermionAlgorithmChannel):
                continue
            o = ch.observables(sim.states[cname], sim.lattice)
            self.records.append({"tick": sim.tick, "channel": cname,
                                 "argmax": o["argmax"], "p_argmax": o["p_argmax"],
                                 "one_per_site_weight": o["one_per_site_weight"],
                                 "layer": o["layer"], "probabilities": o["probabilities"]})

    def summary(self) -> dict:
        if not self.records:
            return {}
        last = self.records[-1]
        return {"final_argmax": last["argmax"], "final_p": last["p_argmax"],
                "final_weight": last["one_per_site_weight"],
                "final_probabilities": last["probabilities"]}


@register_observer
class FermionEntanglementObserver(Observer):
    """Record the live two-site SPIN entanglement generated by real fermion
    hopping (F217): from the Fock product |↑,↓⟩ the spin entanglement rises as
    the genuine second-quantized dynamics run."""
    name = "fermion_entanglement"
    label = "Fermion Spin Entanglement"
    exactness = "quantitative"

    def observe(self, sim) -> None:
        for cname, ch in sim.channels.items():
            if not isinstance(ch, FermionChainChannel):
                continue
            o = ch.observables(sim.states[cname], sim.lattice)
            self.records.append({"tick": sim.tick, "channel": cname, **o})

    def summary(self) -> dict:
        if not self.records:
            return {}
        S = [r["spin_entanglement"] for r in self.records]
        return {"S_initial": S[0], "S_final": S[-1], "S_max": max(S),
                "generated": bool(max(S) > S[0] + 1e-9), "ln2": float(np.log(2))}


def _QN():
    """Lazy handle to the ca_quantum_noise kernel (F221)."""
    import importlib
    # C6: engine path, not the bare `ca_quantum_noise` shim name — this loads by
    # string, so the import rewriter cannot see it and C9 would break it.
    return importlib.import_module("casim.engine.interactions.qi_noise")


@register
class ErrorCorrectionChannel(Channel):
    """A live quantum error-correction round through the engine (F221).

    Carries the full density matrix of an encoded logical qubit; each tick
    applies one round of a decoherence channel and (optionally) stabilizer
    recovery, reporting the logical fidelity.  Codes: bitflip (3q), phaseflip
    (3q), shor (9q).  All gates native (exchange-derived CNOT + rotors).

    Config: code ("bitflip"|"phaseflip"|"shor"), noise ("bitflip"|"phaseflip"|
    "depolarizing"), p (0.1), correct (True), a,b (logical amplitudes).
    """
    type_name = "error_correction"
    label = "Error Correction"
    propagator = "even"
    topologies = ("cubic", "bcc")

    def _encode(self, QN, code, a, b):
        if code == "bitflip":
            return QN.encode_bitflip(a, b), 3
        if code == "phaseflip":
            return QN.encode_phaseflip(a, b), 3
        if code == "shor":
            return QN.encode_shor(a, b), 9
        raise ValueError(f"unknown code {code!r}")

    def _kraus(self, QN, noise, p):
        return {"bitflip": QN.kraus_bitflip, "phaseflip": QN.kraus_phaseflip,
                "depolarizing": QN.kraus_depolarizing}[noise](p)

    def _recover(self, QN, code, rho):
        return {"bitflip": QN.recover_bitflip, "phaseflip": QN.recover_phaseflip,
                "shor": QN.recover_shor}[code](rho)

    def init_state(self, lattice, rng):
        QN = _QN()
        code = str(self.config.get("code", "bitflip"))
        a = float(self.config.get("a", np.cos(0.7)))
        b = float(self.config.get("b", np.sin(0.7)))
        psiL, n = self._encode(QN, code, a, b)
        return {"rho": QN.density(psiL), "psiL": np.asarray(psiL, complex),
                "n": n, "code": code,
                "noise": str(self.config.get("noise", "bitflip")),
                "p": float(self.config.get("p", 0.1)),
                "correct": bool(self.config.get("correct", True))}

    def step(self, state, lattice, context=None, rng=None):
        QN = _QN()
        n = int(state["n"])
        kraus = self._kraus(QN, state["noise"], float(state["p"]))
        rho = QN.apply_channel_all(state["rho"], kraus, n)
        if state["correct"]:
            rho = self._recover(QN, state["code"], rho)
        out = dict(state)
        out["rho"] = rho
        return out

    def energy(self, state) -> float:
        return float(np.real(np.trace(state["rho"])))    # ≡1

    def observables(self, state, lattice) -> dict:
        QN = _QN()
        F = QN.fidelity(state["rho"], state["psiL"])
        return {"fidelity": float(F), "trace": float(np.real(np.trace(state["rho"]))),
                "code": state["code"], "noise": state["noise"],
                "p": float(state["p"]), "corrected": bool(state["correct"])}

    def block_spin(self, state, lattice, b: int):
        return state

    def density_field(self, state):
        raise ValueError("error_correction has no spatial density field")


@register_observer
class ErrorCorrectionObserver(Observer):
    """Record the live logical fidelity of every error_correction channel per
    tick — the code holding a logical qubit against decoherence (F221)."""
    name = "error_correction_fidelity"
    label = "Error Correction Fidelity"
    exactness = "quantitative"

    def observe(self, sim) -> None:
        for cname, ch in sim.channels.items():
            if not isinstance(ch, ErrorCorrectionChannel):
                continue
            o = ch.observables(sim.states[cname], sim.lattice)
            self.records.append({"tick": sim.tick, "channel": cname, **o})

    def summary(self) -> dict:
        if not self.records:
            return {}
        F = [r["fidelity"] for r in self.records]
        return {"F_initial": F[0], "F_final": F[-1], "F_min": min(F),
                "code": self.records[-1]["code"], "corrected": self.records[-1]["corrected"]}


@register_observer
class EntanglementEntropyObserver(Observer):
    """Record the live entanglement entropy of every register channel per tick.

    This is the mechanised statement of F212/F214: from a PRODUCT initial state
    the recorded entropy rises from 0 toward ln2 (per maximally-entangled cut) as
    the derived exchange dynamics run — entanglement the substrate is not given.
    """
    name = "entanglement_entropy"
    label = "Entanglement Entropy"
    exactness = "quantitative"

    def observe(self, sim) -> None:
        for cname, ch in sim.channels.items():
            if not isinstance(ch, EntanglementRegisterChannel):
                continue
            obs = ch.observables(sim.states[cname], sim.lattice)
            self.records.append({
                "tick": sim.tick,
                "channel": cname,
                "entropy_cut": obs["entropy_cut"],
                "entropy_single": obs["entropy_single"],
                "purity_cut": obs["purity_cut"],
                "norm": obs["norm"],
            })

    def summary(self) -> dict:
        if not self.records:
            return {}
        S = [r["entropy_cut"] for r in self.records]
        return {
            "S_initial": S[0],
            "S_final": S[-1],
            "S_max": max(S),
            "generated": bool(S[-1] > S[0] + 1e-9),
            "ln2": float(np.log(2)),
        }
