import aiohttp
from typing import Optional, Dict, Any
from .models import *
import json

from .api_config import HTTPException
from .config import settings
from .api_auth import ApiAuth

from asyncio import gather
import asyncio
from pydantic import ValidationError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApiClient:
    """API Client for pvz wb

    :param access_token: access token for requests

    """

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = self._build_headers(access_token)

    def _build_url(self, base_url_name: str, path: str) -> str:
        """Build full URL from settings and path

        :param base_url_name: The key of the base URL ('discovery' or 's_point')
        :param path: API endpoint path
        :return: Full URL as a string
        """
        base_url = getattr(settings, f"{base_url_name.upper()}_URL", None)
        if not base_url:
            raise ValueError(f"Base URL '{base_url_name}' not configured in settings")
        return f"{base_url.rstrip('/')}/{path.lstrip('/')}"


    def _build_headers(self, access_token: str) -> Dict[str, str]:
        """Build headers with current access token

        :param access_token: access token for requests
        :return: headers dictionary
        """
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Content-Type": "application/json",
            "Origin": "https://pvz.wb.ru",
            "Referer": "https://pvz.wb.ru/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "x-app-type": "prod",
            "x-app-version": "v9.7.254",
            "x-token": access_token
        }

    async def _request(self,
                       base_url_name: str,
                       path: str,
                       method: str,
                       params: Optional[Dict[str, Any]] = None,
                       data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Common method to get response from API
        
        :param base_url_name: The key of the base URL ('discovery' or 's_point')
        :param path: API endpoint path
        :param method: HTTP method
        :param params: Optional parameters for GET request
        :param data: Optional JSON data for POST request
        :return: JSON response data
        """
        url = self._build_url(base_url_name, path)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, params=params, json=data, headers=self.headers) as response:
                    if response.status == 401:
                        raise HTTPException(response.status, "Unauthorized - Access token may have expired.")
                    elif response.status in {400, 403, 429, 500}:
                        raise HTTPException(response.status, f"Error: {await response.text()}")

                    try:
                        return await response.json()
                    except aiohttp.ContentTypeError:
                        response_text = await response.text()
                        content_type = response.headers.get("Content-Type", '')
                        raise HTTPException(response.status,
                                            f"Error (ContentTypeError): {response_text} (Content-Type: {content_type})")
        except Exception as e:
            logger.error(f"Unexpected error in _request: {e}")
            raise

    async def get_pickpoint_list(self) -> List[PickpointModel]:
        """Retrieve the list of pickpoints with users"""

        
        response_data = await self._request(
            base_url_name="discovery",
            path="/api/v2/pickpoint/list",
            method="GET")

        # Проверка, что response_data — это словарь и содержит ключ 'data'
        if isinstance(response_data, dict) and "data" in response_data:
            pickpoint_data = response_data["data"]

            # Убедимся, что pickpoint_data — это список словарей
            if isinstance(pickpoint_data, list):
                pickpoints = [PickpointModel(**pp) for pp in pickpoint_data]
                return pickpoints
            else:
                raise ValueError("Expected 'data' to be a list of dictionaries")

        else:
            raise ValueError("Expected response_data to be a dictionary with a 'data' key")


    async def get_owner_info(self) -> OwnerInfoModel:
        """Get information about the pickpoint owner

        :param pickpoint_id: Internal pickpoint ID
        :param external_id: External pickpoint ID
        :return: OwnerInfoModel
        """
        
        response_data = await self._request(
            base_url_name="s_point",
            path="/api/v3/pickpoint/owner/info",
            method="GET"
        )
        
        # Проверка, что response_data — это словарь и содержит ключ 'data'
        if isinstance(response_data, dict) and "data" in response_data and isinstance(response_data["data"], list) and len(response_data["data"]) > 0:
            owner_data = response_data["data"][0]
            return OwnerInfoModel(**owner_data)
        else:
            raise ValueError("Expected response_data to be a dictionary with a 'data' list containing at least one item")


    async def get_pickpoint_rating(self, office_id: int):
        """Get information about pickpoint rating

        :param office_id: Office ID
        :return 

        """
        data = {"office_id": office_id}
        response_data = await self._request(
            base_url_name="point_rating",
            path="/api/pickpoint/rates/avg30",
            method="POST",
            data=data
        )
        # Проверяем, что ответ содержит ключ 'avg_rate'
        if isinstance(response_data, dict) and "avg_rate" in response_data:
            return float(response_data["avg_rate"])
        else:
            raise ValueError("Expected response_data to be a dictionary with key 'avg_rate'")

    async def get_operations(self, date_from: str, date_to: str,  offset: int = 0, limit: int = 100) -> OperationResponse:
        """Get all operations with  period for a specific offset and limit
        Вкладка - Баланс
        :param date_from: Начальная дата (в формате YYYY-MM-DD).
        :param date_to: Конечная дата (в формате YYYY-MM-DD).
        :param offset: Смещение.
        :param limit: Лимит.
        :return: Список операций.
        """

        base_url_name = "point_balance"
        path = "/api/v1/balance/owner/transactions" 
        
       
        params = {
            "country": "RU",
            "filter.limit": limit,
            "filter.offset": offset,
            "filter.date_from": date_from,
            "filter.date_to": date_to,
        }
        logger.info(f"Fetching data with params: {params}")
        response_data = await self._request(
            base_url_name=base_url_name,
            path=path,
            method="GET",
            params=params,
        )
        
        
        if isinstance(response_data, dict) and "data" in response_data:
            return OperationResponse(**response_data)
        else:
            raise ValueError("Unexpected response format")
       


    # async def parallel_get_operations(self, date_from: str, date_to: str) -> List[OperationModel]:
    #     """Get all operations for period with pagination, using parallel requests.

    #     :param date_from: Начальная дата (в формате YYYY-MM-DD).
    #     :param date_to: Конечная дата (в формате YYYY-MM-DD).
    #     :return: Список операций.
    #     """
        
    #     base_url_name = "point_balance"
    #     path = "/api/v1/balance/owner/transactions"
    #     limit = 20
    #     all_operations = []

    #     params = {
    #     "country": "RU",
    #     "filter.limit": limit,
    #     "filter.offset": 0,
    #     "filter.date_from": date_from,
    #     "filter.date_to": date_to,
    #     }
        
    #     response_data = await self._request(
    #         base_url_name=base_url_name,
    #         path=path,
    #         method="GET",
    #         params=params,
    #     )
        
    #     if not isinstance(response_data, dict) or "data" not in response_data:
    #         raise ValueError("Unexpected response format")
        
    #     response = OperationResponse(**response_data)
    #     all_operations.extend(response.data)

    #     total_rows = response.total_rows
    #     semaphore = asyncio.Semaphore(max_concurrent_tasks)

    #     async def fetch_with_semaphore(offset: int):
    #         async with semaphore:
    #             params = {
    #                 "country": "RU",
    #                 "filter.limit": limit,
    #                 "filter.offset": offset,
    #                 "filter.date_from": date_from,
    #                 "filter.date_to": date_to,
    #             }
    #             print(f"Fetching offset {offset}")
    #             return await self._request(
    #                 base_url_name=base_url_name,
    #                 path=path,
    #                 method="GET",
    #                 params=params,
    #             )

    #     tasks = [
    #         fetch_with_semaphore(offset)
    #         for offset in range(limit, total_rows, limit)
    #     ]
        
    #     responses = await gather(*tasks)

    #     for resp in responses:
    #         if isinstance(resp, dict) and "data" in resp:
    #             response = OperationResponse(**resp)
    #             all_operations.extend(response.data)
    #         else:
    #             raise ValueError("Unexpected response format in one of the responses")

    #     return all_operations

    async def get_transaction_details(self, transaction_id: int) -> TransactionDetailsResponse:
        """Get detail information about transaction

        :param transaction_id: ID операции.
        :return: Список детальной информации по операции
        """

        base_url_name = "point_balance"
        path = f"/api/v1/balance/transaction/{transaction_id}/goods_list"
        params = {"country": "RU"}

        response_data = await self._request(
            base_url_name=base_url_name,
            path=path,
            method="GET",
            params=params,
        )

        if isinstance(response_data, dict) and "data" in response_data:
            transaction_details = response_data["data"]

            # Проверяем, что data содержит ровно один элемент
            if isinstance(transaction_details, list):
                return [TransactionDetailModel(**detail) for detail in transaction_details]
            else:
                raise ValueError(
                    f"Expected 'data' to be a list with exactly one item, got {len(transaction_details)} items"
                )
        else:
            raise ValueError("Expected response_data to be a dictionary with a 'data' key")

    async def get_operations_name(self) -> CategoriesOperationsResponse:
        """"Get categories and names of operations"""

        base_url_name = "point_balance"
        path = "/api/v1/get-operations"

        response_data = await self._request(
            base_url_name=base_url_name,
            path=path,
            method="GET"
        )

        if isinstance(response_data, dict) and "categories" and "operations" in response_data:
            try:
                return CategoriesOperationsResponse(**response_data)
            except Exception as e:
                raise ValueError(f"Invalid response data structure: {e}")
        else:
            raise ValueError("Expected response_data to be a dictionary with 'categories' and 'operations' keys")
 


    async def get_partner_payments(self, pickpoint_id: int, limit: int = 10, offset: int = 0) -> WeeklyPaymentsResponse:
        """Get partner payments by week
        
        :param pickpoint_id: Pickpoint ID
        :param limit: Limit
        :param offset: Offset
        """

        base_url_name = "point_balance"  # Базовый URL для платежей
        path = "/api/v2/partner-payments"

        params = {
            "limit": limit,
            "offset": offset,
            "pickpoint_id": pickpoint_id
        }   
        response_data = await self._request(
            base_url_name=base_url_name,
            path=path,
            method="GET",
            params=params,
        )
        if isinstance(response_data, dict) and "payments" in response_data:
            payments = response_data["payments"]

            if isinstance(payments, list):
                return [WeeklyTransaction(**week) for week in payments]
            else:
                raise ValueError(
                    f"Expected 'payments' to be a list with exactly one item, got {len(payments)} items"
                )
        else:
            raise ValueError("Expected response_data to be a dictionary with a 'payments' key")

    
    async def get_handling_report(self) ->TotalHandlingReport:
        """Get handling report"""

        response_data = await self._request(
            base_url_name="s_point",
            path="/api/v2/handing-report-2/pickpoint/list",
            method="GET"
        )
        if isinstance(response_data, dict) and "data" in response_data:
            try:
                handling_report = TotalHandlingReport.model_validate(response_data["data"])
                return handling_report
            except ValidationError as e:
                raise ValueError(f"Validation error: {e}")
        else:
            raise ValueError("Expected response_data to be a dictionary with a 'data' key")

            
    async def get_handling_report_by_pickpoint(self, pickpoint_id: int) ->HandlingReport2Model:
        """Отчет по офису удержано/доплачено
        
        :param pickpoint_id: Pickpoint ID
        :return: HandlingReport2Model
        """
        base_url_name = "s_point"  
        path = "/api/v2/handing-report-2/box-goods/list"

        params = {
            "pickpoint_id": pickpoint_id
        }
        response_data = await self._request(
            base_url_name=base_url_name,
            path=path,
            method="GET",
            params=params,
        )
        if isinstance(response_data, dict) and "data" in response_data:
            try:
                handling_report = HandlingReport2Model.model_validate(response_data["data"])
                return handling_report
            except ValidationError as e:
                raise ValueError(f"Validation error: {e}")
        else:
            raise ValueError("Expected response_data to be a dictionary with a 'data' key")

    async def get_detail_good_hadling(self, pickpoint_id: int, goods_id: int) ->GoodOperationDetail:
        """Получения детализации по товару в удержании/доплате
        
        :param pickpoint_id: Pickpoint ID
        :param goods_id: Goods ID
        :return
        """
        base_url_name = "s_point"  
        path = "/api/v2/handing-report-2/goods"

        params = {
            "pickpoint_id": pickpoint_id,
            "goods_id": goods_id
        }
        response_data = await self._request(
            base_url_name=base_url_name,
            path=path,
            method="GET",
            params=params,
        )
        if isinstance(response_data, dict) and "data" in response_data:
            try:
                goods_detail = GoodOperationDetail.model_validate(response_data["data"])
                return goods_detail
            except ValidationError as e:
                raise ValueError(f"Validation error: {e}")
        else:
            raise ValueError("Expected response_data to be a dictionary with a 'data' key")




        


    