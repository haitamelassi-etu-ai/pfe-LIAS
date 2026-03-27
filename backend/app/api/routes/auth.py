from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db
from app.models.user import MemberProfile, User, UserRole
from app.schemas.auth import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
)
from app.schemas.user import MemberOut

router = APIRouter(prefix="/auth", tags=["auth"])


def _create_reset_token(user_id: int) -> str:
    return create_access_token(str(user_id), expires_delta=timedelta(minutes=30))


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    existing = db.scalar(select(User).where(User.email == payload.email))
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    role = payload.role if payload.role in {"member", "doctorant", "admin"} else "member"
    user = User(email=payload.email, password_hash=hash_password(payload.password), role=UserRole(role))
    db.add(user)
    db.flush()

    profile = MemberProfile(
        user_id=user.id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        professional_email=payload.email,
    )
    db.add(profile)
    db.commit()

    token = create_access_token(str(user.id), expires_delta=timedelta(days=1))
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == form_data.username))
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token)


@router.get("/me", response_model=MemberOut)
def me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> MemberOut:
    profile = db.scalar(select(MemberProfile).where(MemberProfile.user_id == current_user.id))
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)) -> dict[str, str]:
    user = db.scalar(select(User).where(User.email == payload.email))
    if not user:
        return {"message": "If this email exists, a reset token has been issued."}

    # In production this token should be emailed; returned here for PFE demo flow.
    reset_token = _create_reset_token(user.id)
    return {
        "message": "Password reset token generated. In production, send by email.",
        "reset_token": reset_token,
    }


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)) -> dict[str, bool]:
    try:
        decoded = jwt.decode(payload.token, settings.secret_key, algorithms=["HS256"])
        user_id = int(decoded.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password_hash = hash_password(payload.new_password)
    db.add(user)
    db.commit()
    return {"updated": True}


@router.post("/change-password")
def change_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, bool]:
    if not verify_password(payload.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    current_user.password_hash = hash_password(payload.new_password)
    db.add(current_user)
    db.commit()
    return {"updated": True}
