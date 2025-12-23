from fastapi import APIRouter, status, HTTPException, Body, Request
from api.product.shemas import CategoryCreate, CategoryUpdate, CategoryResponse
from api.utils import get_db_pool
import logging

router = APIRouter(prefix="/api/v1/category", tags=["Category"])
logging.basicConfig(level=logging.INFO)

# Schemas are now imported from api.product.shemas

@router.post("/", response_model=CategoryResponse)
async def create_category(payload: CategoryCreate = Body(...)):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        try:
            row = await conn.fetchrow(
                "INSERT INTO siri.categories (name) VALUES ($1) RETURNING id, name",
                payload.name
            )
            if not row:
                raise HTTPException(status_code=500, detail="Failed to create category")
            return CategoryResponse(id=row["id"], name=row["name"])
        except Exception as e:
            logging.error(f"Error creating category: {e}")
            raise HTTPException(status_code=400, detail="Category already exists or invalid data")

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, payload: CategoryUpdate = Body(...)):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            "UPDATE siri.categories SET name = $1 WHERE id = $2",
            payload.name, category_id
        )
        if result == "UPDATE 0":
            raise HTTPException(status_code=404, detail="Category not found")
        row = await conn.fetchrow(
            "SELECT id, name FROM siri.categories WHERE id = $1",
            category_id
        )
        return CategoryResponse(id=row["id"], name=row["name"])

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM siri.categories WHERE id = $1",
            category_id
        )
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Category not found")
        return

@router.get("/", response_model=list[CategoryResponse])
async def list_categories():
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, name FROM siri.categories ORDER BY name")
        return [CategoryResponse(id=row["id"], name=row["name"]) for row in rows]
