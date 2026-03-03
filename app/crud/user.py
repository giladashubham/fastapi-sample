from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import (
    get_password_hash,
    verify_password,
    create_verification_token,
)
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    verification_token = create_verification_token(user.email)

    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        verification_token=verification_token,
        is_active=True,
        is_verified=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: User, user_update: UserUpdate) -> User:
    update_data = user_update.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()


def verify_user(db: Session, user: User) -> User:
    user.is_verified = True
    user.verification_token = None
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def regenerate_verification_token(db: Session, user: User) -> User:
    verification_token = create_verification_token(user.email)
    user.verification_token = verification_token
    db.commit()
    db.refresh(user)
    return user
