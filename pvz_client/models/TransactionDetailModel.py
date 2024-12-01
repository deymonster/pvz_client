from pydantic import BaseModel
from typing import Optional


class TransactionDetailModel(BaseModel):
    rid: int
    shk: int
    price: float
    vendor: int
    model: int
    info: str  # Здесь информация в виде JSON-строки
    scanned_code: Optional[str] = None
    currency: str
    payment_type: str
    buyer_id: int
    pickpoint_id: int
    balance: float
    sell_summ: float
    created: str
    with_discount: bool
