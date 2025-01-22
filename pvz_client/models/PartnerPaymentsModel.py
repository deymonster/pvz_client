from pydantic import BaseModel
from typing import Optional
from typing import List, Dict

class Operation(BaseModel):  # Операция
    id: int
    sum: float
    count: int
    

class Transaction(BaseModel): # Содержит список операций в рамках одной категории.
    id: int
    operations: List[Operation]
    


class PickpointPayment(BaseModel): # Определяет выплаты для каждого отдельного филиала.
    pickpoint_id: int
    address: str
    categories: List[Transaction]
    turnover: Dict[str, float]
    total: float
    base_accrued: float
    expensive_accrued: float
    other_accrued: float


class WeeklyTransaction(BaseModel):   #  определяет сумму выплат за неделю.
    date_from: str
    date_to: str
    owner_id: int
    currency: str
    total_transactions: List[Transaction]  # Используем модель `Transaction`
    total_turnover: Dict[str, float]
    total: float
    base_accrued: float
    expensive_accrued: float
    other_accrued: float
    pickpoint_payments: List[PickpointPayment]

class WeeklyPaymentsResponse(BaseModel):
    payments: List[WeeklyTransaction]
    total_weeks: int




