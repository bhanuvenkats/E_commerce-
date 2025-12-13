from fastapi import APIRouter, status, HTTPException, Body, UploadFile, File, Form
from api.product.shemas import ProductCreate, ProductUpdate, ProductResponse
from api.utils import get_db_pool
import logging
import uuid
from api.product.blob_utils import upload_to_azure_blob

router = APIRouter(prefix="/api/v1/product", tags=["Product"])
logging.basicConfig(level=logging.INFO)

@router.post("/", response_model=ProductResponse)
async def create_product(
    name: str = Form(...),
    description: str = Form(""),
    category_id: int = Form(...),
    total_price: float = Form(...),
    offer_percentage: float = Form(0),
    quantity: int = Form(...),
    image: UploadFile = File(...)
):
    pool = await get_db_pool()
    image_url = await upload_to_azure_blob(image)
    async with pool.acquire() as conn:
        # Check if category exists
        category = await conn.fetchrow(
            "SELECT id FROM siri.categories WHERE id = $1",
            category_id
        )
        if not category:
            raise HTTPException(
                status_code=400,
                detail="Category not found. Please create the category first."
            )
        row = await conn.fetchrow(
            """
            INSERT INTO siri.products
            (name, description, category_id, total_price, offer_percentage, quantity, image_url)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id, name, description, category_id, total_price, offer_percentage, net_price, quantity, image_url
            """,
            name, description, category_id, total_price, offer_percentage, quantity, image_url
        )
        if not row:
            raise HTTPException(status_code=500, detail="Failed to create product")
        # Also insert into product_images table
        await conn.execute(
            """
            INSERT INTO siri.product_images (product_id, image_url)
            VALUES ($1, $2)
            """,
            row["id"], row["image_url"]
        )
        return ProductResponse(**row)

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, payload: ProductUpdate = Body(...)):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        # Check if category exists
        category = await conn.fetchrow(
            "SELECT id FROM siri.categories WHERE id = $1",
            payload.category_id
        )
        if not category:
            raise HTTPException(
                status_code=400,
                detail="Category not found. Please create the category first."
            )
        result = await conn.execute(
            """
            UPDATE siri.products
            SET name = $1, description = $2, category_id = $3, total_price = $4, offer_percentage = $5, quantity = $6, updated_at = NOW()
            WHERE id = $7
            """,
            payload.name, payload.description, payload.category_id, payload.total_price, payload.offer_percentage, payload.quantity, product_id
        )
        if result == "UPDATE 0":
            raise HTTPException(status_code=404, detail="Product not found")
        row = await conn.fetchrow(
            "SELECT * FROM siri.products WHERE id = $1",
            product_id
        )
        return ProductResponse(**row)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM siri.products WHERE id = $1",
            product_id
        )
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Product not found")
        return

@router.get("/", response_model=list[ProductResponse])
async def list_products():
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM siri.products ORDER BY created_at DESC")
        return [ProductResponse(**row) for row in rows]

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM siri.products WHERE id = $1", product_id)
        if not row:
            raise HTTPException(status_code=404, detail="Product not found")
        return ProductResponse(**row)
