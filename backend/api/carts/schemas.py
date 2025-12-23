from pydantic import BaseModel, PositiveInt
from typing import Optional

# --- Cart Schemas ---

class CartItemAdd(BaseModel):
    product_id: int
    quantity: PositiveInt

class CartItemUpdate(BaseModel):
    quantity: PositiveInt

from datetime import datetime

class CartItemResponse(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int
    price_at_add: float
    total_amount: float
    created_at: datetime
    updated_at: datetime

# --- Wishlist Schemas ---

class WishlistItemAdd(BaseModel):
    product_id: int

class WishlistItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    added_at: datetime
