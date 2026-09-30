"""
NB-121 (p.97) -- "neutrino as the missing magnetic monopole" analogy.
NB-122 (p.97) -- quark confinement likened to orbital-angular-momentum
quantization forcing intrinsic (spin-like) charges to stay hidden.

Neither is a closed algebraic claim; this script does the one concrete,
checkable piece of each -- whether the STRUCTURAL premise each analogy
leans on is itself accurate -- and leaves the analogy itself (which the
notebook offers only as a speculative "might be examined") unscored beyond
that.
"""
import json

# NB-121: is it actually true, structurally, that (a) the right-handed weak
# current is absent from the SM and (b) magnetic monopoles are absent from
# Maxwell's equations, in a way that is a comparable "missing state" to the
# missing/neutral (non-interacting) Weyl components identified in NB-120?
nb121_premises = {
    "SM_has_no_observed_right_handed_charged_current": True,  # standard, well-established (V-A theory, confirmed to high precision)
    "Maxwell_equations_as_formulated_have_no_magnetic_source_term": True,  # standard (div B = 0 is a postulate, not derived)
    "both_are_literally_the_same_kind_of_absence": False,  # one is a dynamical/chirality selection rule (could in principle be violated by new physics at some scale), the other is a topological/structural feature of the U(1) gauge group (a monopole requires a DIFFERENT U(1) bundle topology, not a violated selection rule)
}

# NB-122: is orbital angular momentum actually restricted to integer values
# (0,1,2,...) while spin can be half-integer, and is this really an accurate
# structural parallel to fractional (1/3 e) quark charge confinement?
nb122_premises = {
    "orbital_angular_momentum_quantum_number_is_always_a_nonnegative_integer": True,  # standard QM (single-valuedness of Y_l^m on the sphere)
    "spin_can_be_half_integer_with_no_such_restriction": True,  # standard QM (spinor double-valuedness allowed since spin is not a function on physical space)
    "quark_charge_confinement_mechanism_is_actually_analogous": False,  # confinement is a strong-coupling/flux-tube (linear potential) dynamical effect of SU(3) color, not a representation-theory selection rule like integer-vs-half-integer angular momentum; the notebook's own phrasing ("perhaps... some fundamental principle") correctly flags this as speculative, not a derived equivalence
}

output = {
    "NB-121": {
        "kind": "mechanism/speculation",
        "premises_checked": nb121_premises,
        "assessment": (
            "Both named facts (no right-handed weak current observed; no "
            "magnetic monopole observed) are individually correct. The "
            "analogy between them -- both are the 'missing' member of an "
            "otherwise-populated multiplet -- is an apt verbal observation "
            "but not a structural equivalence: the absence of a "
            "right-handed W-coupling is a dynamical/representation choice "
            "(nothing prevents writing a right-handed current on paper; the "
            "SM simply doesn't gauge it), whereas the absence of a magnetic "
            "monopole in ordinary Maxwell theory is a topological fact "
            "about the trivial U(1) bundle (a monopole requires a "
            "nontrivial fiber bundle / Dirac string, a qualitatively "
            "different kind of 'missing'). The notebook does not claim more "
            "than an analogy, and is explicit that it is speculative."
        ),
        "verdict": "NOT-TESTABLE",
    },
    "NB-122": {
        "kind": "mechanism/speculation",
        "premises_checked": nb122_premises,
        "assessment": (
            "The stated facts about orbital vs. spin angular momentum "
            "quantization are standard and correct. The proposed parallel "
            "to quark-charge confinement is explicitly speculative in the "
            "notebook's own words ('perhaps... under a Heisenberg-like "
            "arrangement') and is not actually structurally analogous: "
            "confinement is a strong-coupling dynamical statement (the "
            "linearly-rising QCD flux-tube potential), not a "
            "representation-theoretic selection rule forbidding certain "
            "quantum numbers from appearing in isolation. The analogy is "
            "evocative but not a mechanism with the same mathematical "
            "content as the L vs. S quantization example it's compared to."
        ),
        "verdict": "NOT-TESTABLE",
    },
}

path = "test-results/notebook-recon/NB-121_122_monopole_confinement_analogies.json"
with open(path, "w") as f:
    json.dump(output, f, indent=2)

print(json.dumps(output, indent=2))
