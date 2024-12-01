from pydantic import BaseModel
from typing import Optional

class OwnerInfoModel(BaseModel):
    """Model for owner information response

    Attributes:
        wb_user_id (int): Wildberries user ID
        phone (int): Phone number
        name (str): Full name of the owner
        org_name (str): Organization name
    """
    wb_user_id: int
    phone: int
    name: str
    org_name: str
