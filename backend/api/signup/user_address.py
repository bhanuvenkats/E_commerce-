from fastapi import APIRouter, HTTPException, Request, Body, Path
from fastapi.responses import JSONResponse
from typing import Optional
from api.utils import get_db_pool, DB_SCHEMA
import logging
from api.signup.schemas import AddressCreate, AddressUpdate, AddressResponse

router = APIRouter(prefix="/api/v1", tags=["UserAddress"])

logging.basicConfig(level=logging.INFO)

def get_user_id_from_jwt(request: Request):
    """
    Extract user_id from JWT payload set by TokenValidatorMiddleware.
    Ensures all address operations are scoped to the authenticated user.
    """
    payload = getattr(request.state, "jwt_payload", None)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return int(payload["sub"])

@router.get("/user-address", response_model=list[AddressResponse])
async def list_addresses(request: Request):
    user_id = get_user_id_from_jwt(request)
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            f"SELECT * FROM {DB_SCHEMA}.user_addresses WHERE user_id = $1 ORDER BY is_default DESC, id ASC",
            user_id
        )
        return [dict(row) for row in rows]

@router.post("/user-address", response_model=AddressResponse, status_code=201)
async def add_address(
    request: Request,
    address: AddressCreate = Body(...),
):
    user_id = get_user_id_from_jwt(request)
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        try:
            row = await conn.fetchrow(
                f"""
                INSERT INTO {DB_SCHEMA}.user_addresses
                (user_id, address_line1, city, postal_code, country, address_type, is_default, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, NOW(), NOW())
                RETURNING *
                """,
                user_id, address.address_line1, address.city, address.postal_code, address.country, address.address_type, address.is_default
            )
            return dict(row)
        except Exception as e:
            logging.error(f"Error adding address: {e}")
            raise HTTPException(status_code=503, detail="Could not add address")

@router.put("/user-address/{address_id}", response_model=AddressResponse)
async def update_address(
    request: Request,
    address_id: int = Path(..., gt=0),
    address: AddressUpdate = Body(...),
):
    user_id = get_user_id_from_jwt(request)
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        # Build dynamic update statement
        fields = []
        values = []
        for field, value in address.dict(exclude_unset=True).items():
            fields.append(f"{field} = ${len(values)+2}")
            values.append(value)
        if not fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        values = [address_id] + values
        try:
            row = await conn.fetchrow(
                f"""
                UPDATE {DB_SCHEMA}.user_addresses
                SET {', '.join(fields)}, updated_at = NOW()
                WHERE id = $1 AND user_id = {user_id}
                RETURNING *
                """,
                *values
            )
            if not row:
                raise HTTPException(status_code=404, detail="Address not found")
            return dict(row)
        except Exception as e:
            logging.error(f"Error updating address: {e}")
            raise HTTPException(status_code=503, detail="Could not update address")

@router.delete("/user-address/{address_id}", status_code=204)
async def delete_address(
    request: Request,
    address_id: int = Path(..., gt=0),
):
    user_id = get_user_id_from_jwt(request)
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        try:
            result = await conn.execute(
                f"DELETE FROM {DB_SCHEMA}.user_addresses WHERE id = $1 AND user_id = {user_id}",
                address_id
            )
            if result == "DELETE 0":
                raise HTTPException(status_code=404, detail="Address not found")
            return JSONResponse(status_code=204, content=None)
        except Exception as e:
            logging.error(f"Error deleting address: {e}")
            raise HTTPException(status_code=503, detail="Could not delete address")
