from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud import user as user_crud
from app.models.user import User
from app.schemas.user import MessageResponse, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)) -> Any:
    return current_user


@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    if user_update.email and user_update.email != current_user.email:
        existing = user_crud.get_user_by_email(db, user_update.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use"
            )

    if user_update.username and user_update.username != current_user.username:
        existing = user_crud.get_user_by_username(db, user_update.username)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
            )

    user = user_crud.update_user(db, current_user, user_update)
    return user


@router.delete("/me", response_model=MessageResponse)
def delete_current_user(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> Any:
    user_crud.delete_user(db, current_user)
    return {"message": "User deleted successfully"}
