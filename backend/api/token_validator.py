import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
import os
from api.utils import get_db_pool, DB_SCHEMA
from dotenv import load_dotenv

# Load environment variables from project root .env
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

PUBLIC_PATHS = [
    "/docs",
    "/docs/",
    "/openapi.json",
    "/redoc",
    "/redoc/",
    "/favicon.ico",
    "/health",
    "/api/v1/login",
    "/api/v1/signup",
    "/api/v1/forgot-password/request",
    "/api/v1/forgot-password/verify",
]

async def validate_token(token: str):
    try:
        jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return True, "Valid"
    except jwt.ExpiredSignatureError:
        return False, "Token expired"
    except jwt.InvalidTokenError:
        return False, "Invalid token"
    except Exception as e:
        return False, f"Error: {str(e)}"

class TokenValidatorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow OPTIONS requests to pass through for CORS preflight
        if request.method == "OPTIONS":
            return await call_next(request)
        
        # Check if path matches any public path pattern
        request_path = request.url.path
        is_public = any(request_path == path or request_path.startswith(path) for path in PUBLIC_PATHS)
        if is_public:
            return await call_next(request)
        auth = request.headers.get("Authorization")
        request_id = request.headers.get("X-Request-ID", "N/A")
        if not auth or not auth.startswith("Bearer "):
            logging.info(f"Request_ID={request_id} Token_ID=N/A Valid=Invalid Reason=Missing token")
            return JSONResponse(status_code=403, content={"detail": "Forbidden: Missing or invalid token"})
        token = auth.split(" ", 1)[1]
        valid, reason = await validate_token(token)
        token_id = "N/A"
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], options={"verify_exp": False})
            token_id = payload.get("sub", "N/A")
            request.state.jwt_payload = payload  # <-- FIX: Set payload for downstream use
        except Exception:
            payload = None
        logging.info(f"Request_ID={request_id} Token_ID={token_id} Valid={'Valid' if valid else 'Invalid'} Reason={reason}")
        if not valid:
            msg = "Another session was initiated by the same user in another device" if reason == "Session not active" else f"Forbidden: {reason}"
            return JSONResponse(status_code=403, content={"detail": msg})
        return await call_next(request)
