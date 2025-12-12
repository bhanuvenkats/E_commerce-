from pydantic import BaseModel

# Category Schemas
class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str

# Product Schemas
class ProductCreate(BaseModel):
    name: str
    description: str = ""
    category_id: int
    total_price: float
    offer_percentage: float = 0
    quantity: int

class ProductUpdate(BaseModel):
    name: str
    description: str = ""
    category_id: int
    total_price: float
    offer_percentage: float = 0
    quantity: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    category_id: int
    total_price: float
    offer_percentage: float
    net_price: float
    quantity: int
    image_url: str | None

# Product Image Schemas
class ProductImageResponse(BaseModel):
    id: int
    product_id: int
    image_url: str
