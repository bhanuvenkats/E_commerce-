from fastapi import APIRouter, HTTPException, status, Request, Body, Path
from typing import List
from api.utils import get_db_pool
from api.carts.schemas import CartItemAdd, CartItemUpdate, CartItemResponse
import logging

router = APIRouter(prefix="/api/v1/cart", tags=["Cart"])
logging.basicConfig(level=logging.INFO)

# --- Schemas ---

# --- Helper to get user_id from JWT (assumes JWT middleware sets request.state.jwt_payload) ---
def get_user_id_from_jwt(request: Request) -> int:
    payload = getattr(request.state, "jwt_payload", None)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return int(payload["sub"])

# --- Endpoints ---

@router.get("/", response_model=List[CartItemResponse])
async def get_cart_items(request: Request):
    """
    Get all items in the user's active cart.
    """
    user_id = get_user_id_from_jwt(request)
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        cart = await conn.fetchrow(
            "SELECT id FROM siri.carts WHERE user_id = $1 AND status = 'active'",
            user_id
        )
        if not cart:
            raise HTTPException(status_code=404, detail="Active cart not found")
        rows = await conn.fetch(
            """
            SELECT * FROM siri.cart_items
            WHERE cart_id = $1
            ORDER BY created_at DESC
            """,
            cart["id"]
        )
        return [dict(row) for row in rows]

@router.post("/add", response_model=CartItemResponse, status_code=201)
async def add_to_cart(request: Request, item: CartItemAdd = Body(...)):
    """
    Add a product to the user's active cart.
    """
    user_id = get_user_id_from_jwt(request)
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        cart = await conn.fetchrow(
            "SELECT id FROM siri.carts WHERE user_id = $1 AND status = 'active'",
            user_id
        )
        if not cart:
            # Create a new active cart for the user
            cart = await conn.fetchrow(
                """
                INSERT INTO siri.carts (user_id, status)
                VALUES ($1, 'active')
                RETURNING id
                """,
                user_id
            )
        # Get product price
        product = await conn.fetchrow(
            "SELECT net_price FROM siri.products WHERE id = $1",
            item.product_id
        )
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        # Check if item already in cart
        existing = await conn.fetchrow(
            "SELECT * FROM siri.cart_items WHERE cart_id = $1 AND product_id = $2",
            cart["id"], item.product_id
        )
        if existing:
            raise HTTPException(status_code=409, detail="Product already in cart. Use update endpoint to change quantity.")
        row = await conn.fetchrow(
            """
            INSERT INTO siri.cart_items (cart_id, product_id, quantity, price_at_add)
            VALUES ($1, $2, $3, $4)
            RETURNING *
            """,
            cart["id"], item.product_id, item.quantity, float(product["net_price"])
        )
        return dict(row)

@router.patch("/update/{cart_item_id}", response_model=CartItemResponse)
async def update_cart_item(
    request: Request,
    cart_item_id: int = Path(..., gt=0),
    item: CartItemUpdate = Body(...)
):
    """
    Update quantity of a cart item.
    """
    user_id = get_user_id_from_jwt(request)
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        # Ensure the cart item belongs to the user's active cart
        cart = await conn.fetchrow(
            "SELECT id FROM siri.carts WHERE user_id = $1 AND status = 'active'",
            user_id
        )
        if not cart:
            raise HTTPException(status_code=404, detail="Active cart not found")
        cart_item = await conn.fetchrow(
            "SELECT * FROM siri.cart_items WHERE id = $1 AND cart_id = $2",
            cart_item_id, cart["id"]
        )
        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        row = await conn.fetchrow(
            """
            UPDATE siri.cart_items
            SET quantity = $1, updated_at = NOW()
            WHERE id = $2
            RETURNING *
            """,
            item.quantity, cart_item_id
        )
        return dict(row)

@router.delete("/remove/{cart_item_id}", status_code=204)
async def remove_cart_item(
    request: Request,
    cart_item_id: int = Path(..., gt=0)
):
    """
    Remove a product from the user's active cart.
    """
    user_id = get_user_id_from_jwt(request)
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        cart = await conn.fetchrow(
            "SELECT id FROM siri.carts WHERE user_id = $1 AND status = 'active'",
            user_id
        )
        if not cart:
            raise HTTPException(status_code=404, detail="Active cart not found")
        result = await conn.execute(
            "DELETE FROM siri.cart_items WHERE id = $1 AND cart_id = $2",
            cart_item_id, cart["id"]
        )
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Cart item not found")
        return

@router.delete("/clear", status_code=204)
async def clear_cart(request: Request):
    """
    Remove all items from the user's active cart.
    """
    user_id = get_user_id_from_jwt(request)
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        cart = await conn.fetchrow(
            "SELECT id FROM siri.carts WHERE user_id = $1 AND status = 'active'",
            user_id
        )
        if not cart:
            raise HTTPException(status_code=404, detail="Active cart not found")
        await conn.execute(
            "DELETE FROM siri.cart_items WHERE cart_id = $1",
            cart["id"]
        )
        return
