from pydantic import BaseModel
from typing import List, Optional

class OperationModel(BaseModel):
    operation_id: int
    operation_type: str
    pickpoint_id: int
    employee_id: int
    summ: float
    rids: Optional[str] = ""
    created: str  
    currency: str
    description: Optional[str] = ""
    summ_pickpoint: float

class OperationResponse(BaseModel):
    data: List[OperationModel]
    total_rows: int
    total_summ: float
