from pydantic import BaseModel,  Field
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


class TransactionDetailsResponse(BaseModel):
    data: Optional[list[TransactionDetailModel]] = Field(
        None, description="Детализация операций, может быть пустым"
    )