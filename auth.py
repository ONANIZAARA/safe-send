import hashlib
import hmac
import secrets
import json
import base64
import time

SECRET_KEY = "safesend-secret-key-2024"

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{hashed}"

def verify_password(plain: str, hashed: str) -> bool:
    try:
        salt, hash_val = hashed.split(":")
        return hashlib.sha256((salt + plain).encode()).hexdigest() == hash_val
    except Exception:
        return False

def create_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = int(time.time()) + 86400
    payload_json = json.dumps(payload)
    payload_b64 = base64.b64encode(payload_json.encode()).decode()
    sig = hashlib.sha256((payload_b64 + SECRET_KEY).encode()).hexdigest()
    return f"{payload_b64}.{sig}"

def decode_token(token: str):
    try:
        payload_b64, sig = token.split(".")
        expected_sig = hashlib.sha256((payload_b64 + SECRET_KEY).encode()).hexdigest()
        if sig != expected_sig:
            return None
        payload = json.loads(base64.b64decode(payload_b64).decode())
        if payload.get("exp", 0) < int(time.time()):
            return None
        return payload.get("sub")
    except Exception:
        return None

def get_current_user(token: str = None):
    if not token:
        return None
    return decode_token(token)
# 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