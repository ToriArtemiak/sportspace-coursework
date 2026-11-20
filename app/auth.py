
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserRead


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

password_hasher = PasswordHash.recommended()


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    # Нормалізуємо email
    email = str(user_data.email).strip().lower()

    # Перевіряємо, чи користувач уже існує
    existing_user = db.scalar(
        select(User).where(User.email == email)
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    # Хешуємо пароль
    hashed_password = password_hasher.hash(
        user_data.password
    )

    # Створюємо користувача
    new_user = User(
        full_name=user_data.full_name.strip(),
        email=email,
        password_hash=hashed_password,
        role="client"
    )

    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        ) from None

    db.refresh(new_user)

    return new_user
