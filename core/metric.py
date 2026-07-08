# ============================================================
# Constitutional Metric Space (Definition II.3)
# Weighted Euclidean Metric ||·||_v in WAD Arithmetic
# ============================================================

from core.wad import (
    wad_encode,
    wad_decode,
    wad_add,
    wad_sub,
    wad_mul,
    wad_abs,
    W
)

# ------------------------------------------------------------
# Weighted principal-component metric
# ||Ya - Yb||_v = sqrt( Σ wj * (vj(Ya) - vj(Yb))^2 )
# All arithmetic performed in WAD integer space.
# ------------------------------------------------------------

class ConstitutionalMetric:
    def __init__(self, weights):
        """
        weights: list of floats -> encoded into WAD integers
        Must satisfy Σ wj = 1 and wj > 0.
        """
        self.weights = [wad_encode(w) for w in weights]

    def distance(self, a, b):
        """
        Compute ||a - b||_v in WAD arithmetic.
        a, b: lists of WAD-encoded principal components.
        """
        total = 0

        for w, va, vb in zip(self.weights, a, b):
            diff = wad_sub(va, vb)          # (va - vb)
            sq = wad_mul(diff, diff)        # (va - vb)^2
            weighted = wad_mul(w, sq)       # wj * (va - vb)^2
            total = wad_add(total, weighted)

        # sqrt(total / W) — but sqrt must remain deterministic.
        # We use integer Newton iteration for WAD-safe sqrt.
        return self._wad_sqrt(total)

    # --------------------------------------------------------
    # Deterministic integer sqrt (Newton iteration)
    # --------------------------------------------------------
    def _wad_sqrt(self, n):
        """
        Compute sqrt(n / W) in WAD integer space.
        Returns WAD-encoded sqrt.
        """
        if n == 0:
            return 0

        # Initial guess (encoded)
        x = n

        # Newton iteration (deterministic)
        for _ in range(12):  # fixed number of iterations
            # x_next = (x + n/x) / 2
            div = n // x
            x_next = (x + div) // 2
            x = x_next

        # Encode sqrt(n/W) = sqrt(n) / sqrt(W)
        # sqrt(W) = 10^9
        SQRT_W = 10**9
        return x // SQRT_W

# ------------------------------------------------------------
# Example metric instance (3 principal components)
# ------------------------------------------------------------

default_metric = ConstitutionalMetric(weights=[0.33, 0.33, 0.34])

def metric_self_test():
    """
    Deterministic self-test for build-in-public verification.
    """
    a = [wad_encode(0.1), wad_encode(0.2), wad_encode(0.3)]
    b = [wad_encode(0.15), wad_encode(0.25), wad_encode(0.35)]

    d = default_metric.distance(a, b)

    return {
        "a": a,
        "b": b,
        "distance_raw": d,
        "distance_decoded": wad_decode(d)
    }
