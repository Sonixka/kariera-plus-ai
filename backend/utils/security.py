
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import JWTError, jwt


# Načtení .env z hlavní složky projektu
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=ENV_FILE)

# Tajný klíč pro zabezpečení JWT tokenů
secret_key = os.getenv("SECRET_KEY")

if secret_key is None:
    raise RuntimeError(
        "SECRET_KEY není nastaven. Zkontroluj soubor .env."
    )

if len(secret_key) < 32:
    raise RuntimeError(
        "SECRET_KEY je příliš krátký. Zkontroluj soubor .env."
    )

SECRET_KEY: str = secret_key

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        return payload

    except JWTError:
        raise ValueError("Neplatný nebo prošlý přístupový token.")
