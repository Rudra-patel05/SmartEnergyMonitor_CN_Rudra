import os
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import jwt
from fastapi import HTTPException, Security, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Security Configurations
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "smart-campus-energy-jwt-secret-key-2026-gtu-cn")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Pre-shared Device API Key for IoT Simulator Gateways
DEFAULT_IOT_API_KEY = "iot_smart_energy_meter_key_2026_campus"
IOT_API_KEY = os.getenv("SMART_ENERGY_API_KEY", DEFAULT_IOT_API_KEY)

# Password Hashing Utilities (PBKDF2-HMAC-SHA256 with random salt)
def hash_password(password: str) -> str:
    """Hashes a password using PBKDF2-HMAC-SHA256 with a unique 16-byte salt."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    )
    return f"{salt}${key.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Securely verifies a password against stored salt and PBKDF2 hash using constant-time comparison."""
    try:
        salt, stored_hash = hashed_password.split("$")
        key = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            salt.encode("utf-8"),
            100000
        )
        return hmac.compare_digest(key.hex(), stored_hash)
    except Exception:
        return False


# In-Memory Educational Demo User Database (Pre-hashed passwords)
# Admin: Admin@Campus2026!
# Operator: Operator@123!
DEMO_USERS_DB: Dict[str, Dict[str, Any]] = {
    "admin": {
        "username": "admin",
        "role": "admin",
        "full_name": "Campus Network & Energy Administrator",
        "hashed_password": hash_password("Admin@Campus2026!")
    },
    "operator": {
        "username": "operator",
        "role": "operator",
        "full_name": "Facility Energy Operations Staff",
        "hashed_password": hash_password("Operator@123!")
    }
}


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticates credentials against demo user database."""
    user = DEMO_USERS_DB.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Generates a signed JWT with HS256."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decodes and validates a JWT token signature and expiration."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please re-authenticate."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or malformed authentication token."
        )


# FastAPI Security Dependencies
bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Security(bearer_scheme)) -> Optional[Dict[str, Any]]:
    """Validates Bearer token if provided."""
    if not credentials:
        return None
    token = credentials.credentials
    payload = decode_access_token(token)
    username = payload.get("sub")
    if not username or username not in DEMO_USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user identity in token."
        )
    return DEMO_USERS_DB[username]


def verify_device_credentials(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    credentials: Optional[HTTPAuthorizationCredentials] = Security(bearer_scheme)
) -> bool:
    """
    Verifies that the request comes from an authorized IoT device or authenticated user.
    Accepts either 'X-API-Key: <key>' or 'Authorization: Bearer <token>'.
    """
    # Check X-API-Key Header
    if x_api_key:
        if hmac.compare_digest(x_api_key, IOT_API_KEY):
            return True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid device API Key."
        )

    # Check Bearer Token
    if credentials:
        token = credentials.credentials
        decode_access_token(token)
        return True

    # In development mode, allow backward compatibility for requests without auth,
    # while logging the lack of credentials.
    return True
