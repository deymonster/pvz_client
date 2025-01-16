from pydantic import BaseModel
from typing import List, Optional


class Category(BaseModel):
    description: Optional[str] = None
    id: int
    name: str
    operations: List[int]

class Operation(BaseModel):
    base_name: str
    description: Optional[str] = None
    id: int
    minus_description: Optional[str] = None
    minus_name: str
    name: str

class CategoriesOperationsResponse(BaseModel):
    categories: List[Category]
    operations: List[Operation]