import hashlib
import os
import uuid
import re
import asyncpg
import ssl
from dotenv import load_dotenv

# Load environment variables from project root .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SCHEMA = os.getenv("DB_SCHEMA", "siri")
DB_SSLMODE = os.getenv("DB_SSLMODE", "require").lower()

# Fail fast if any required DB env variable is missing
_missing = [k for k, v in [
    ("DB_HOST", DB_HOST),
    ("DB_PORT", DB_PORT),
    ("DB_NAME", DB_NAME),
    ("DB_USER", DB_USER),
    ("DB_PASSWORD", DB_PASSWORD),
] if not v]
if _missing:
    raise RuntimeError(f"Missing required DB environment variables: {', '.join(_missing)}")

# Password hashing with SHA-512 (no salt)
def hash_password(password: str) -> str:
    hash_obj = hashlib.sha512()
    hash_obj.update(password.encode('utf-8'))
    return hash_obj.hexdigest()

# Password strength validation (at least 8 chars, upper, lower, digit, special)
def is_password_strong(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def generate_uuid() -> str:
    return str(uuid.uuid4())

def passwords_match(password1: str, password2: str) -> bool:
    """
    Returns True if both passwords are exactly the same, False otherwise.
    """
    return password1 == password2

async def get_db_pool():
    print(f"[DB DEBUG] DB_HOST={DB_HOST} DB_PORT={DB_PORT} DB_NAME={DB_NAME} DB_USER={DB_USER} DB_SCHEMA={DB_SCHEMA}")
    if not hasattr(get_db_pool, "pool"):
        ssl_context = None
        if DB_SSLMODE != "disable":
            ssl_context = ssl.create_default_context()
        get_db_pool.pool = await asyncpg.create_pool(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            command_timeout=60,
            ssl=ssl_context,
        )
    return get_db_pool.pool
