"""
Personal Assistant Bot — Utilities
Self-contained 2FA/TOTP code generator and validator.
"""

import re
import base64
import struct
import time
import hmac
import hashlib

def validate_totp_secret(secret: str) -> tuple[bool, str]:
    """Validate a TOTP secret key (base32 encoded).
    Returns (is_valid, cleaned_secret_or_error_message).
    """
    if not secret:
        return False, "Secret key cannot be empty."

    # Clean: remove spaces, dashes, convert to uppercase
    cleaned = secret.strip().replace(" ", "").replace("-", "").upper()

    if len(cleaned) < 16:
        return False, "Secret key is too short. It should be at least 16 characters."

    if len(cleaned) > 64:
        return False, "Secret key is too long."

    # Check valid base32 characters (A-Z, 2-7, =)
    if not re.match(r'^[A-Z2-7=]+$', cleaned):
        return False, "Invalid characters in secret key. It should only contain letters A-Z and digits 2-7."

    # Try to decode
    try:
        base64.b32decode(cleaned, casefold=True)
    except Exception:
        return False, "Invalid secret key format."

    return True, cleaned


def generate_totp(secret_base32: str, digits: int = 6, interval: int = 30) -> str:
    """Generate a TOTP code from a base32-encoded secret (RFC 6238).
    Uses only Python stdlib — no external dependencies needed.
    """
    # Decode the base32 secret
    key = base64.b32decode(secret_base32.upper(), casefold=True)

    # Current time step
    time_step = int(time.time()) // interval

    # Pack as big-endian unsigned 64-bit int
    msg = struct.pack('>Q', time_step)

    # HMAC-SHA1
    h = hmac.new(key, msg, hashlib.sha1).digest()

    # Dynamic truncation (RFC 4226 §5.4)
    offset = h[-1] & 0x0F
    code_int = struct.unpack('>I', h[offset:offset + 4])[0]
    code_int = code_int & 0x7FFFFFFF
    code_int = code_int % (10 ** digits)

    return str(code_int).zfill(digits)


def get_totp_remaining_seconds(interval: int = 30) -> int:
    """Get remaining seconds before the current TOTP code expires."""
    return interval - (int(time.time()) % interval)
