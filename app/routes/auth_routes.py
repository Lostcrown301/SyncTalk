from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user import (
    UserCreate,
    UserResponse
)
from app.services.user_service import create_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(
        db=db,
        username=user.username,
        email=user.email,
        password=user.password
    )