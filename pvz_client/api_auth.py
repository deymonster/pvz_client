import aiohttp
from typing import Optional, Dict, Any, Union
from .api_config import HTTPException
from .models import TokenResponse, RequestCodeResponse, SwitchTokenResponse


class ApiAuth:
    """Auth client for pvz wb"""

    def __init__(self,
                 auth_base_path: str,
                 base_path: str,
                 verify: bool = True,
                 basic_token: Optional[str] = None):

        self.auth_base_path = auth_base_path
        self.base_path = base_path
        self.verify = verify
        self.basic_token = basic_token
        self.app_version = "v9.7.270"  # TODO: get from config
        self.device_uuid = "ba72b509f8d2417a882699ffdcac4f22"



    @property
    def get_headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Content-Type": "application/json",
            "Origin": "https://pvz.wb.ru",
            "Referer": "https://pvz.wb.ru/",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
            "x-app-type": "prod",
            "x-app-version": self.app_version
        }

    async def _request(self,
                       method: str,
                       path: str,
                       base_url: Optional[str] = None,
                       params: Optional[Dict[str, Any]] = None,
                       data: Optional[Dict[str, Any]] = None,
                       headers: Optional[Dict[str, str]] = None,
                       return_status: bool = False) -> Dict[str, Any] | int:
        """Common request method

        :param method: HTTP method
        :param path: API path
        :param params: Optional parameters
        :param data: Optional data
        :param return_status: Return HTTP status code
        :return: Response
        """
        base_url = base_url or self.auth_base_path
        if not path.startswith("/"):
            path = f"/{path}"
        url = base_url + path
        request_headers = self.get_headers.copy()
        if headers:
            request_headers.update(headers)
        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method,
                    url,
                    params=params,
                    json=data,
                    headers=request_headers,
            ) as response:
                if return_status:
                    return response.status
                try:
                    response_data = await response.json()
                except aiohttp.ContentTypeError:
                    response_text = await response.text()
                    raise HTTPException(response.status, f"Invalid response from server: {response_text}")
                if response.status in {400, 401, 403, 429, 500}:
                    raise HTTPException(response.status, f"{response_data}")
                return response_data

    async def login(self, phone: str) -> RequestCodeResponse:
        """Request code for auth

        :param phone: phone number
        :return RequestCodeResponse
        """
        path = "/api/v1/login"
        data = {
            "phone": phone,
            "resend": False,
            "device_uuid": self.device_uuid
        }
        response_data = await self._request("POST", path, data=data)
        if isinstance(response_data, dict):
            return RequestCodeResponse(**response_data)
        else:
            raise HTTPException(response_data, "Unexpected response format")

    async def validate(self, code: str, token: str) -> TokenResponse:
        """Connect with code and get access token or use refresh token

        :param username: username (phone number)
        :param password: password (code from lk)
        :param refresh_token: current refresh token
        :return TokenResponse
        """
        path = "/api/v1/validate"
        data = {
            "code": code,
            "token": token,
            "device_type": "DEVICE_WEB",
            "app_version": self.app_version,
            "device_name": "macOS 12.6.3"
        }
        

        response_data = await self._request("POST", path, data=data)
        if isinstance(response_data, dict):
            return TokenResponse(**response_data)
        else:
            raise HTTPException(response_data, "Unexpected response format")
        
    async def switch_token(self, token: str, pickpoint_id: str, external_id: str) -> SwitchTokenResponse:
        """Update token with pid and xpid
        
        :param token: current token
        :return SwitchTokenResponse
        """
        base_url = "https://s-point.wb.ru/s20"
        path = f"/api/v2/pickpoint/{pickpoint_id}/switch"

        headers = {
            "x-pickpoint-id": pickpoint_id,
            "x-pickpoint-external-id": external_id,
            "x-token": token,  # Добавляем токен в заголовки
        }
        response_data = await self._request(
            method="GET",
            path=path,
            base_url=base_url,
            headers=headers
        )
        if isinstance(response_data, dict):
            return SwitchTokenResponse(**response_data)
        else:
            raise HTTPException(response_data, "Unexpected response format")









async def main():
    auth_base_path = "https://r-point.wb.ru"
    api_auth = ApiAuth(auth_base_path=auth_base_path, base_path=auth_base_path)
    phone = "79282951709"
    try:
        code_response = await api_auth.login(phone=phone)
        print("Code requested successfully:", code_response)
    except HTTPException as e:
        print(f"Error requesting code: {e}")
        return

    code = input("Enter code received via SMS: ")
    temp_token = code_response.data

    try:
        token_response = await api_auth.validate(code=code, token=temp_token)
        print("Connected successfully, tokens received:")
        print(token_response)
    except HTTPException as e:
        print(f"Error validating code: {e}")
        return

    pickpoint_id = "65717"
    external_id = "141685"

    try:
        modified_token = await api_auth.switch_token(
            token=token_response.access.token,
            pickpoint_id=pickpoint_id,
            external_id=external_id,
        )
        print(f"Modified token: {modified_token}")
    except HTTPException as e:
        print(f"Error switching token: {e}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())



