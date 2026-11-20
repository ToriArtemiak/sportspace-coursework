
import os

from datetime import datetime, timedelta, timezone

import jwt

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserRead, TokenResponse


# Завантаження налаштувань із .env
load_dotenv()

SECRET_KEY = os.getenv("SPORTSPACE_JWT_SECRET")

if not SECRET_KEY:
    raise RuntimeError(
        "SPORTSPACE_JWT_SECRET is not configured"
    )

ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)

password_hasher = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)


# 1. Реєстрація нового користувача
@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    email = str(user_data.email).strip().lower()

    existing_user = db.scalar(
        select(User).where(User.email == email)
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    hashed_password = password_hasher.hash(
        user_data.password
    )

    new_user = User(
        full_name=user_data.full_name.strip(),
        email=email,
        password_hash=hashed_password,
        role="client",
    )

    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        ) from None

    db.refresh(new_user)

    return new_user


# 2. Вхід користувача
@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    email = form_data.username.strip().lower()

    user = db.scalar(
        select(User).where(User.email == email)
    )

    # Перевірка email і пароля
    if (
        user is None
        or not password_hasher.verify(
            form_data.password,
            user.password_hash,
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Час завершення дії токена
    expires_at = datetime.now(
        timezone.utc
    ) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

    # Створення JWT
    token = jwt.encode(
        {
            "sub": str(user.id),
            "exp": expires_at,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
    )


# 3. Отримання поточного користувача
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_error = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if not isinstance(user_id, str):
            raise credentials_error

        if not user_id.isdigit():
            raise credentials_error

    except InvalidTokenError:
        raise credentials_error from None

    user = db.get(User, int(user_id))

    if user is None:
        raise credentials_error

    return user


# 4. Захищений маршрут профілю
@router.get(
    "/me",
    response_model=UserRead,
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user
