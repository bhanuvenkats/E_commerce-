from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import sys

# Add parent directory to path BEFORE imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.token_validator import TokenValidatorMiddleware

load_dotenv()

import logging
import multiprocessing

logging.basicConfig(level=logging.INFO)

from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer

app = FastAPI(title="SIRI APP", version="1.0.0")

# Add middleware in correct order (they execute in reverse order)
# First add TokenValidator, then CORS - so CORS runs before TokenValidator
app.add_middleware(TokenValidatorMiddleware)

# Add CORS middleware AFTER TokenValidator so it runs FIRST
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",  # Regex to match all origins
    allow_credentials=True,  # Allow credentials
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
)

# Add BearerAuth to OpenAPI docs for global JWT authorization
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Import signup and login routers

from api.signup.signup import router as signup_router
from api.signup.login import router as login_router
from api.signup.user_address import router as user_address_router
from api.signup.forgot_password import router as forgot_password_router
from api.product.category import router as category_router
from api.product.product import router as product_router
from api.product.product_image import router as product_image_router

if signup_router:
    app.include_router(signup_router)
if login_router:
    app.include_router(login_router)
if user_address_router:
    app.include_router(user_address_router)
if forgot_password_router:
    app.include_router(forgot_password_router)
if category_router:
    app.include_router(category_router)
if product_router:
    app.include_router(product_router)
if product_image_router:
    app.include_router(product_image_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Production runner with uvicorn
if __name__ == "__main__":
    import uvicorn

    # Get number of workers - defaults to CPU count
    workers = int(os.getenv("WORKERS", multiprocessing.cpu_count()))

    # Get host and port from environment or use defaults
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))

    # Production configuration
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        workers=workers,
        loop="asyncio",  # Use default asyncio event loop
        access_log=True,
        log_level="info"
    )
