from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.models.user import User
from app.auth.password import hash_password


def create_user(
    db: Session,
    username: str,
    email: str,
    password: str
):
    existing_email = db.query(User).filter(
        User.email == email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    existing_username = db.query(User).filter(
        User.username == username
    ).first()

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    hashed_pw = hash_password(password)

    user = User(
        username=username,
        email=email,
        hashed_password=hashed_pw
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user