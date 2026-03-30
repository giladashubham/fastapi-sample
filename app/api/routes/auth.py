from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core import email as email_utils
from app.core.config import settings
from app.core.rate_limit import limiter
from app.core.security import verify_verification_token, create_access_token
from app.crud import user as user_crud
from app.schemas.user import MessageResponse, Token, UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@limiter.limit("5/minute")
@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)) -> Any:
    existing_email = user_crud.get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    existing_username = user_crud.get_user_by_username(db, user.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    db_user = user_crud.create_user(db, user)

    email_utils.send_verification_email(db_user.email, db_user.verification_token)

    return db_user


@limiter.limit("10/minute")
@router.post("/login", response_model=Token)
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Any:
    user = user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please check your email for verification link.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@limiter.limit("20/minute")
@router.get("/verify-email", response_model=MessageResponse)
def verify_email(
    request: Request,
    token: str = Query(..., description="Verification token from email"),
    db: Session = Depends(get_db),
) -> Any:
    email = verify_verification_token(token, max_age=3600)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token",
        )

    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user.is_verified:
        return {"message": "Email already verified"}

    user_crud.verify_user(db, user)

    return {"message": "Email verified successfully"}


@limiter.limit("3/minute")
@router.post("/resend-verification", response_model=MessageResponse)
def resend_verification(
    request: Request,
    email: str = Query(..., description="Email address to resend verification"),
    db: Session = Depends(get_db),
) -> Any:
    user = user_crud.get_user_by_email(db, email)
    if not user:
        return {"message": "If this email exists, a verification email has been sent"}

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already verified"
        )

    user_crud.regenerate_verification_token(db, user)
    email_utils.send_verification_email(user.email, user.verification_token)

    return {"message": "Verification email sent. Please check your inbox."}
