from fastapi import APIRouter, status, HTTPException, UploadFile, File, Form
from api.product.shemas import ProductImageResponse
from api.utils import get_db_pool
import logging
import uuid
from api.product.blob_utils import upload_to_azure_blob

router = APIRouter(prefix="/api/v1/product-image", tags=["ProductImage"])
logging.basicConfig(level=logging.INFO)

# Schemas are now imported from api.product.shemas

# Schemas are now imported from api.product.shemas

@router.post("/", response_model=ProductImageResponse)
async def add_product_image(
    product_id: int = Form(...),
    image: UploadFile = File(...)
):
    pool = await get_db_pool()
    image_url = await upload_to_azure_blob(image)
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO siri.product_images (product_id, image_url)
            VALUES ($1, $2)
            RETURNING id, product_id, image_url
            """,
            product_id, image_url
        )
        if not row:
            raise HTTPException(status_code=500, detail="Failed to add product image")
        return ProductImageResponse(**row)

@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_image(image_id: int):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM siri.product_images WHERE id = $1",
            image_id
        )
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Product image not found")
        return

@router.get("/product/{product_id}", response_model=list[ProductImageResponse])
async def list_product_images(product_id: int):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id, product_id, image_url FROM siri.product_images WHERE product_id = $1 ORDER BY id",
            product_id
        )
        return [ProductImageResponse(**row) for row in rows]
