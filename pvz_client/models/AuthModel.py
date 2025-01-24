from pydantic import BaseModel
from typing import Optional


class RequestCodeResponse(BaseModel):
    """Модель для ответа при запросе кода"""
    data: str
    code: str
    code_length: int


class AccessTokenData(BaseModel):
    """Модель для данных токена доступа"""
    token: str
    ttl: int


class TokenResponse(BaseModel):
    """Модель для ответа при подтверждении кода и получения токенов"""
    access: AccessTokenData
    refresh: AccessTokenData
    ws_access: AccessTokenData
    user_id: int

class SwitchTokenResponse(BaseModel):
    """Модель для ответа при обновлении токена"""
    access: AccessTokenData
    refresh: AccessTokenData




