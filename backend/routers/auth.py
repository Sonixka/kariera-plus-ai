from fastapi import APIRouter, HTTPException
from datetime import datetime

from backend.models.user import UserCreate, UserLogin
from backend.database.database import get_connection
from backend.services.auth_service import hash_password
from backend.services.auth_service import verify_password
from backend.utils.security import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register")
def register_user(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()

    # Kontrola, zda už účet s tímto e-mailem existuje
    cursor.execute(
        "SELECT id FROM users WHERE email = ?",
        (user.email,),
    )

    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()

        raise HTTPException(
            status_code=400,
            detail="Uživatel s tímto e-mailem již existuje.",
        )

    # Zahashování hesla
    password_hash = hash_password(user.password)

    # Vytvoření uživatele
    cursor.execute(
        """
        INSERT INTO users (
            name,
            email,
            password_hash,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user.name,
            user.email,
            password_hash,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    conn.commit()
    conn.close()

    return {
        "message": "Registrace proběhla úspěšně.",
        "name": user.name,
        "email": user.email,
    }


@router.post("/login")
def login_user(user: UserLogin):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, email, password_hash
        FROM users
        WHERE email = ?
        """,
        (user.email,),
    )

    existing_user = cursor.fetchone()

    conn.close()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Nesprávný e-mail nebo heslo.",
        )

    user_id, name, email, password_hash = existing_user

    if not verify_password(user.password, password_hash):
        raise HTTPException(
            status_code=401,
            detail="Nesprávný e-mail nebo heslo.",
        )

    access_token = create_access_token(
        {
            "sub": str(user_id),
            "name": name,
            "email": email,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "name": name,
            "email": email,
        },
    }