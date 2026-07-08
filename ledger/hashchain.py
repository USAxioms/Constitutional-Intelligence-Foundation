# ============================================================
# Constitutional Hash-Chain Ledger (SHA3-256)
# Tamper-Evident, Deterministic, WAD-Compatible
# Implements Definition VIII.1 and VIII.2
# ============================================================

import hashlib
from core.wad import wad_encode, wad_decode, W

# ------------------------------------------------------------
# SHA3-256 Hash Function (NIST FIPS 202)
# ------------------------------------------------------------

def sha3_256_bytes(data: bytes) -> str:
    """
    Compute SHA3-256 hash of raw bytes.
    Returns hex string.
    Deterministic, cryptographically secure.
    """
    return hashlib.sha3_256(data).hexdigest()


def sha3_256_state(state):
    """
    Compute SHA3-256 hash of a WAD-encoded state vector.
    State is a list of integers.
    """
    raw = b"".join(int(x).to_bytes(32, "big") for x in state)
    return sha3_256_bytes(raw)


# ------------------------------------------------------------
# Ledger Entry Structure (Definition VIII.1)
# ------------------------------------------------------------

def make_ledger_entry(raw_hash, k, mhplc, sstate, m_class):
    """
    Construct a ledger entry dictionary.
    All fields deterministic.
    """
    return {
        "raw_hash": raw_hash,      # H(Praw)
        "k": k,                    # iteration depth
        "mhplc": mhplc,            # immutable HPLC-MS metadata hash
        "sstate": sstate,          # binary validation state (0 or 1)
        "m_class": m_class         # constitutional classification M(s)
    }


# ------------------------------------------------------------
# Hash-Chain Construction (Definition VIII.2)
# H(Tk) = SHA3-256( Tk | H(Tk-1) )
# ------------------------------------------------------------

def chain_hash(entry, prev_hash):
    """
    Compute chained hash for ledger entry.
    Concatenate entry fields + previous hash.
    """
    payload = (
        str(entry["raw_hash"]).encode() +
        str(entry["k"]).encode() +
        str(entry["mhplc"]).encode() +
        str(entry["sstate"]).encode() +
        str(entry["m_class"]).encode() +
        str(prev_hash).encode()
    )

    return sha3_256_bytes(payload)


# ------------------------------------------------------------
# Ledger Class
# ------------------------------------------------------------

class ConstitutionalLedger:
    def __init__(self, genesis="0" * 64):
        """
        Initialize ledger with genesis hash.
        """
        self.entries = []
        self.hashes = [genesis]

    def append(self, entry):
        """
        Append a new ledger entry and compute chained hash.
        """
        prev_hash = self.hashes[-1]
        new_hash = chain_hash(entry, prev_hash)

        self.entries.append(entry)
        self.hashes.append(new_hash)

        return new_hash

    def verify(self):
        """
        Verify entire hash-chain for tamper-evidence.
        Returns True if valid, False if mismatch detected.
        """
        for i in range(1, len(self.entries) + 1):
            entry = self.entries[i - 1]
            prev_hash = self.hashes[i - 1]
            expected = chain_hash(entry, prev_hash)

            if expected != self.hashes[i]:
                return False

        return True


# ------------------------------------------------------------
# Self-Test for Build-In-Public Verification
# ------------------------------------------------------------

def ledger_self_test():
    ledger = ConstitutionalLedger()

    # Example WAD-encoded state
    state = [wad_encode(0.1), wad_encode(0.2), wad_encode(0.3)]
    raw_hash = sha3_256_state(state)

    entry1 = make_ledger_entry(
        raw_hash=raw_hash,
        k=1,
        mhplc="abc123",
        sstate=1,
        m_class="F27"
    )

    h1 = ledger.append(entry1)

    entry2 = make_ledger_entry(
        raw_hash=raw_hash,
        k=2,
        mhplc="abc123",
        sstate=1,
        m_class="F27"
    )

    h2 = ledger.append(entry2)

    return {
        "hash_1": h1,
        "hash_2": h2,
        "verified": ledger.verify()
    }
