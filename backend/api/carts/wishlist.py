from fastapi import APIRouter, HTTPException, status, Request, Body, Path
from typing import List
from api.utils import get_db_pool
from api.carts.schemas import WishlistItemAdd, WishlistItemResponse
import logging

router = APIRouter(prefix="/api/v1/wishlist", tags=["Wishlist"])
logging.basicConfig(level=logging.INFO)

# --- Schemas ---

# --- Helper to get user_id from JWT (assumes JWT middleware sets request.state.jwt_payload) ---
def get_user_id_from_jwt(request: Request) -> int:
    payload = getattr(request.state, "jwt_payload", None)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return int(payload["sub"])

# --- Endpoints ---

@router.get("/", response_model=List[WishlistItemResponse])
async def get_wishlist_items(request: Request):
    """
    Get all items in the user's wishlist.
    """
    user_id = get_user_id_from_jwt(request)
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT * FROM siri.wishlist_items
            WHERE user_id = $1
            ORDER BY added_at DESC
            """,
            user_id
        )
        return [dict(row) for row in rows]

@router.post("/add", response_model=WishlistItemResponse, status_code=201)
async def add_to_wishlist(request: Request, item: WishlistItemAdd = Body(...)):
    """
    Add a product to the user's wishlist.
    """
    user_id = get_user_id_from_jwt(request)
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        # Check if product already in wishlist
        existing = await conn.fetchrow(
            "SELECT * FROM siri.wishlist_items WHERE user_id = $1 AND product_id = $2",
            user_id, item.product_id
        )
        if existing:
            raise HTTPException(status_code=409, detail="Product already in wishlist.")
        # Check if product exists
        product = await conn.fetchrow(
            "SELECT id FROM siri.products WHERE id = $1",
            item.product_id
        )
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        row = await conn.fetchrow(
            """
            INSERT INTO siri.wishlist_items (user_id, product_id)
            VALUES ($1, $2)
            RETURNING *
            """,
            user_id, item.product_id
        )
        return dict(row)

@router.delete("/remove/{wishlist_item_id}", status_code=204)
async def remove_wishlist_item(
    request: Request,
    wishlist_item_id: int = Path(..., gt=0)
):
    """
    Remove a product from the user's wishlist.
    """
    user_id = get_user_id_from_jwt(request)
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM siri.wishlist_items WHERE id = $1 AND user_id = $2",
            wishlist_item_id, user_id
        )
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Wishlist item not found")
        return

@router.post("/move-to-cart/{wishlist_item_id}", status_code=201)
async def move_wishlist_item_to_cart(
    request: Request,
    wishlist_item_id: int = Path(..., gt=0)
):
    """
    Move a product from wishlist to the user's active cart.
    """
    user_id = get_user_id_from_jwt(request)
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        # Get wishlist item
        wishlist_item = await conn.fetchrow(
            "SELECT * FROM siri.wishlist_items WHERE id = $1 AND user_id = $2",
            wishlist_item_id, user_id
        )
        if not wishlist_item:
            raise HTTPException(status_code=404, detail="Wishlist item not found")
        # Get active cart
        cart = await conn.fetchrow(
            "SELECT id FROM siri.carts WHERE user_id = $1 AND status = 'active'",
            user_id
        )
        if not cart:
            raise HTTPException(status_code=404, detail="Active cart not found")
        # Get product price
        product = await conn.fetchrow(
            "SELECT net_price FROM siri.products WHERE id = $1",
            wishlist_item["product_id"]
        )
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        # Check if already in cart
        existing = await conn.fetchrow(
            "SELECT * FROM siri.cart_items WHERE cart_id = $1 AND product_id = $2",
            cart["id"], wishlist_item["product_id"]
        )
        if existing:
            raise HTTPException(status_code=409, detail="Product already in cart.")
        # Add to cart
        await conn.fetchrow(
            """
            INSERT INTO siri.cart_items (cart_id, product_id, quantity, price_at_add)
            VALUES ($1, $2, $3, $4)
            """,
            cart["id"], wishlist_item["product_id"], 1, float(product["net_price"])
        )
        # Remove from wishlist
        await conn.execute(
            "DELETE FROM siri.wishlist_items WHERE id = $1 AND user_id = $2",
            wishlist_item_id, user_id
        )
        return {"detail": "Product moved from wishlist to cart."}

@router.delete("/clear", status_code=204)
async def clear_wishlist(request: Request):
    """
    Remove all items from the user's wishlist.
    """
    user_id = get_user_id_from_jwt(request)
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "DELETE FROM siri.wishlist_items WHERE user_id = $1",
            user_id
        )
        return
