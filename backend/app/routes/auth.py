from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from datetime import timedelta

from ..schemas import LoginRequest, TokenResponse, AuthStatusResponse
from ..auth import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, DEMO_USERS_DB
from ..logger import log_auth_success, log_auth_failure

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@router.post("/token", response_model=TokenResponse)
def login_for_access_token(payload: LoginRequest, request: Request):
    """
    Authenticates a campus user and issues a signed JWT access token.
    """
    ip = request.client.host if request.client else "unknown"
    user = authenticate_user(payload.username, payload.password)
    if not user:
        log_auth_failure(payload.username, ip, "Incorrect password or username")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    
    log_auth_success(user["username"], user["role"], ip)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        role=user["role"],
        username=user["username"]
    )

@router.post("/verify")
def verify_token(current_user: dict = Depends(get_current_user)):
    """
    Verifies that the provided JWT is valid and active.
    """
    return {
        "valid": True,
        "username": current_user["username"],
        "role": current_user["role"],
        "full_name": current_user["full_name"]
    }

@router.get("/status", response_model=AuthStatusResponse)
def get_auth_status():
    """
    Retrieves the system security status.
    """
    return AuthStatusResponse(
        status="SECURED",
        auth_mode="JWT + PBKDF2-HMAC-SHA256 / Device API-Key Header",
        jwt_algorithm="HS256",
        device_auth_enabled=True,
        active_users=list(DEMO_USERS_DB.keys())
    )
