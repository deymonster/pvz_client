from pydantic import BaseModel
from typing import Optional
from typing import List, Dict
from datetime import datetime


class PickPointHandlingReport(BaseModel):
    add_shk_count: int
    add_shk_sum: int
    address: str
    currency: str
    expired_shk_count: int
    expired_shk_sum: int
    expiring_shk_count: int
    expiring_shk_sum: int
    hold_shk_count: int
    hold_shk_sum: int
    not_accepted_shk_count: int
    not_accepted_shk_sum: int


class TotalHandlingReport(BaseModel):
    add_shk_count: int
    add_shk_sum: int
    currency: str
    expired_shk_count: int
    expired_shk_sum: int
    expiring_shk_count: int
    expiring_shk_sum: int
    hold_shk_count: int
    hold_shk_sum: int
    not_accepted_shk_count: int
    not_accepted_shk_sum: int
    payments_suspended: bool
    pickpoints: List[PickPointHandlingReport]


class GoodsOperation(BaseModel):
    """Модель для операции удержания/доплачивания"""
    id: int
    scanned_code: str
    cell: int
    sum: int
    currency: str
    days: int
    type: str
    transferbox_id: int
    box_accepted_date: Optional[datetime] = None
    add_date: Optional[datetime] = None 
    hold_date: Optional[datetime] = None
    on_hold_date: Optional[datetime] = None
    reason: str
    accept_transferbox_id: int
    ticket_id: int
    rid: int
    shk: int
    buyer_wb_id: int
    is_pickpoint_user: bool


class HandlingReport2Model(BaseModel):
    """Модель для операции удержания/доплачивания"""
    box: List
    goods: List[GoodsOperation]


class ByuerInfo(BaseModel):
    Country: str
    name: str
    phone: int
    user_id: int

class Info(BaseModel):
    name: str
    color: str
    brand: str
    goods_size: str
    no_return: bool
    pics_cnt: int
    adult: bool
    parent_id: int
    subject_name: str
    skus: Optional[dict] = None

class Employee(BaseModel):
    id: int
    phone: int
    country: str
    first_name: str
    last_name: str
    middle_name: str



class GoodOperationDetail(BaseModel):
    """Детализация операции удержания/доплачивания"""
    id: int
    buyer: ByuerInfo
    cell: int
    shk: int
    sticker: int
    scanned_code: str
    price: int
    currency: str
    vendor_code: int
    status: int
    status_description: str
    status_updated: datetime
    info: Info
    type: str
    days: int
    description: str
    employee: Employee
    comment: str
    ticket_id: int
    lostreason_id: int
