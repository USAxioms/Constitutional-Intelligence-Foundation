# ============================================================
# WAD Arithmetic Core (Fixed-Point Constitutional Mathematics)
# Precision: W = 10^18
# Deterministic, Bit-Exact, Cross-Platform Safe
# ============================================================

W = 10**18  # Fixed-point precision constant

def wad_encode(x: float) -> int:
    """
    Encode a real number x into WAD fixed-point integer form.
    Constitutional Definition II.5:
    Represent x as floor(x * W).
    """
    return int(x * W)

def wad_decode(n: int) -> float:
    """
    Decode a WAD integer back into a real number.
    This is only for human readability; internal ops stay integer.
    """
    return n / W

def wad_add(a: int, b: int) -> int:
    """
    WAD addition: integer-safe, deterministic.
    """
    return a + b

def wad_sub(a: int, b: int) -> int:
    """
    WAD subtraction: integer-safe, deterministic.
    """
    return a - b

def wad_mul(a: int, b: int) -> int:
    """
    WAD multiplication:
    Constitutional Definition II.5:
    a ⊗ b := floor(a * b / W)
    """
    return (a * b) // W

def wad_lt(a: int, b: int) -> bool:
    """
    WAD less-than comparison.
    Deterministic, O(1).
    """
    return a < b

def wad_gt(a: int, b: int) -> bool:
    """
    WAD greater-than comparison.
    Deterministic, O(1).
    """
    return a > b

def wad_abs(a: int) -> int:
    """
    Absolute value in WAD integer space.
    """
    return abs(a)

# ============================================================
# Compton-Class Safety Threshold
# εc = 2.5 × 10^-15 encoded in WAD
# ============================================================

EC = wad_encode(2.5e-15)

# ============================================================
# Diagnostic: verify deterministic behavior
# ============================================================

def wad_self_test():
    """
    Quick deterministic self-test for build-in-public verification.
    """
    x = wad_encode(1.234567890123456)
    y = wad_encode(0.000000000000001)

    return {
        "x_raw": x,
        "y_raw": y,
        "add": wad_add(x, y),
        "sub": wad_sub(x, y),
        "mul": wad_mul(x, y),
        "lt": wad_lt(x, y),
        "gt": wad_gt(x, y),
        "abs": wad_abs(-x),
        "EC": EC
    }
