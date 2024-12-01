from pydantic import BaseModel
from typing import Optional, List


class PickpointUserModel(BaseModel):
    user_id: int
    name: str
    last_name: Optional[str] = ""
    phone: int
    is_deleted: bool


class PickpointModel(BaseModel):
    id: int
    name: str
    latitude: str
    longitude: str
    is_active: bool
    external_id: int
    rate: float
    users: List[PickpointUserModel]

