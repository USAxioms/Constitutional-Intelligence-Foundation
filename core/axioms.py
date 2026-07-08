# ============================================================
# Seven Constitutional Axioms (WAD Arithmetic)
# Deterministic, O(1), WAD-Decidable (Theorem VII.1)
# ============================================================

from core.wad import (
    wad_encode,
    wad_mul,
    wad_lt,
    wad_gt,
    wad_abs,
    W
)

# ------------------------------------------------------------
# Thresholds (encoded in WAD)
# ------------------------------------------------------------

THRESHOLD_95 = wad_encode(0.95)     # Vi(s) > 0.95
PURITY_LIMIT = wad_encode(0.001)    # 0.10% impurity = 0.001 fraction
LEDGER_EXEC_MIN = wad_encode(0.975) # 98.2% ± 0.7% → lower bound
LEDGER_EXEC_MAX = wad_encode(0.989) # upper bound


# ------------------------------------------------------------
# Axiom I — Reproducibility ⇒ Determinism
# Bit-identical outputs on identical WAD inputs
# ------------------------------------------------------------

def axiom_I(prev_output, new_output):
    return wad_encode(1) if prev_output == new_output else wad_encode(0)


# ------------------------------------------------------------
# Axiom II — Determinism ⇒ Fixed Point
# |R3(s) - s| < εc (Compton-class safety)
# ------------------------------------------------------------

def axiom_II(distance_raw, EC):
    return wad_encode(1) if wad_lt(distance_raw, EC) else wad_encode(0)


# ------------------------------------------------------------
# Axiom III — Fixed Point ⇒ Full Verification
# Vi(s) > 0.95 for all 27 components
# ------------------------------------------------------------

def axiom_III(verification_list):
    for v in verification_list:
        if wad_lt(v, THRESHOLD_95):
            return wad_encode(0)
    return wad_encode(1)


# ------------------------------------------------------------
# Axiom IV — Verification ⇒ Machine Audit
# audit ∈ ledger
# ------------------------------------------------------------

def axiom_IV(audit_present):
    return wad_encode(1) if audit_present else wad_encode(0)


# ------------------------------------------------------------
# Axiom V — Audit ⇒ Ledger Anchor
# SHA3-256(state) == on_chain_hash
# ------------------------------------------------------------

def axiom_V(hash_match):
    return wad_encode(1) if hash_match else wad_encode(0)


# ------------------------------------------------------------
# Axiom VI — Purity Gate
# impurity < 0.10%
# ------------------------------------------------------------

def axiom_VI(impurity_fraction):
    return wad_encode(1) if wad_lt(impurity_fraction, PURITY_LIMIT) else wad_encode(0)


# ------------------------------------------------------------
# Axiom VII — Ledger Execution Convergence
# Gk ∈ [98.2% ± 0.7%]
# ------------------------------------------------------------

def axiom_VII(exec_cost):
    if wad_lt(exec_cost, LEDGER_EXEC_MIN):
        return wad_encode(0)
    if wad_gt(exec_cost, LEDGER_EXEC_MAX):
        return wad_encode(0)
    return wad_encode(1)


# ------------------------------------------------------------
# Constitutional Satisfaction Functional Γ(s)
# Γ(s) = Σ Ai(s), Ai ∈ {0,1}
# ------------------------------------------------------------

def constitutional_satisfaction(
    prev_output,
    new_output,
    distance_raw,
    EC,
    verification_list,
    audit_present,
    hash_match,
    impurity_fraction,
    exec_cost
):
    A1 = axiom_I(prev_output, new_output)
    A2 = axiom_II(distance_raw, EC)
    A3 = axiom_III(verification_list)
    A4 = axiom_IV(audit_present)
    A5 = axiom_V(hash_match)
    A6 = axiom_VI(impurity_fraction)
    A7 = axiom_VII(exec_cost)

    # Sum all seven axioms (WAD integer addition)
    return A1 + A2 + A3 + A4 + A5 + A6 + A7


# ------------------------------------------------------------
# Self-Test for Build-In-Public Verification
# ------------------------------------------------------------

def axioms_self_test():
    prev_output = [wad_encode(0.1)]
    new_output = [wad_encode(0.1)]
    distance_raw = wad_encode(1e-16)
    verification_list = [wad_encode(0.99)] * 27
    audit_present = True
    hash_match = True
    impurity_fraction = wad_encode(0.0005)
    exec_cost = wad_encode(0.982)

    gamma = constitutional_satisfaction(
        prev_output,
        new_output,
        distance_raw,
        EC,
        verification_list,
        audit_present,
        hash_match,
        impurity_fraction,
        exec_cost
    )

    return {
        "Γ(s)_raw": gamma,
        "Γ(s)_decoded": gamma / W
    }
