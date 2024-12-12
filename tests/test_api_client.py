import pytest
from aioresponses import aioresponses
from pvz_client.api_client import ApiClient, HTTPException
import re

@pytest.fixture
def api_client():
    """Фикстура для создания экземпляра ApiClient"""
    return ApiClient(access_token="mock_access_token")


@pytest.mark.asyncio
async def test_get_pickpoint_list_invalid_data(api_client):
    """Тест получения списка pickpoint с некорректными данными."""
    with aioresponses() as mock_response:
        mock_response.get(
            "https://mock-discovery.api/api/v2/pickpoint/list",
            payload={"data": "invalid_data"},
            status=200,
        )

        with pytest.raises(ValueError) as excinfo:
            await api_client.get_pickpoint_list()

        assert "Expected 'data' to be a list of dictionaries" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_owner_info_missing_data(api_client):
    """Тест получения информации о владельце с отсутствующими данными."""
    with aioresponses() as mock_response:
        mock_response.get(
            "https://mock-s-point.api/api/v3/pickpoint/owner/info",
            payload={"data": []},
            status=200,
        )

        with pytest.raises(ValueError) as excinfo:
            await api_client.get_owner_info(pickpoint_id=1, external_id=100)

        assert "Expected response_data to be a dictionary with a 'data' list containing at least one item" in str(excinfo.value)


@pytest.mark.asyncio
async def test_request_unauthorized(api_client):
    """Тест обработки ошибки 401."""
    with aioresponses() as mock_response:
        mock_response.get(
            "https://mock-discovery.api/api/v2/pickpoint/list",
            payload={"error": "Unauthorized"},
            status=401,
        )

        with pytest.raises(HTTPException) as excinfo:
            await api_client.get_pickpoint_list()

        assert excinfo.value.status_code == 401
        assert "Unauthorized" in str(excinfo.value)


@pytest.mark.asyncio
async def test_request_server_error(api_client):
    """Тест обработки ошибки 500."""
    with aioresponses() as mock_response:
        mock_response.get(
            "https://mock-discovery.api/api/v2/pickpoint/list",
            payload={"error": "Internal Server Error"},
            status=500,
        )

        with pytest.raises(HTTPException) as excinfo:
            await api_client.get_pickpoint_list()

        assert excinfo.value.status_code == 500
        assert "Internal Server Error" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_pickpoint_rating_success(api_client):
    """Тест успешного получения рейтинга pickpoint."""
    with aioresponses() as mock_response:
        mock_response.post(
            "https://mock-point-rating.api/external/api/pickpoint/rates/avg30",
            payload={"avg_rate": 4.973},
            status=200,
        )

        response = await api_client.get_pickpoint_rating(office_id=141685)
        assert response == 4.973


@pytest.mark.asyncio
async def test_get_pickpoint_rating_missing_key(api_client):
    """Тест получения рейтинга с отсутствующим ключом 'avg_rate'."""
    with aioresponses() as mock_response:
        mock_response.post(
            "https://mock-point-rating.api/external/api/pickpoint/rates/avg30",
            payload={},
            status=200,
        )

        with pytest.raises(ValueError) as excinfo:
            await api_client.get_pickpoint_rating(office_id=141685)

        assert "Expected response_data to be a dictionary with key 'avg_rate'" in str(excinfo.value)



@pytest.mark.asyncio
async def test_parallel_get_operations():
    """Тест метода parallel_get_operations."""
    token = "test_token"
    api_client = ApiClient(access_token=token)

    # Указываем параметры теста
    date_from = "2024-11-30"
    date_to = "2024-11-30"
    base_url = "https://mock-point-rating.api/s4"
    path = "/api/v1/balance/owner/transactions"
    total_rows = 250
    limit = 100

    # Подготавливаем фейковые ответы для всех запросов
    fake_data = [
        {
            "operation_id": 2102505171 + i,
            "operation_type": "Продажа",
            "pickpoint_id": 12345,
            "employee_id": 67890,
            "summ": 100.0 + i,
            "rids": "[]",
            "created": f"2024-11-30T10:{i:02d}:00",
            "currency": "₽",
            "description": "",
            "summ_pickpoint": 0.0,
        }
        for i in range(total_rows)
    ]
    chunks = [fake_data[i:i + limit] for i in range(0, total_rows, limit)]

    with aioresponses() as mock_response:
        # Добавляем фейковые ответы для каждого запроса
        for i, chunk in enumerate(chunks):
            offset = i * limit
            pattern = re.compile(
                rf'^{base_url}{path}\?country=RU&filter\.date_from={date_from}'
                rf'&filter\.date_to={date_to}&filter\.limit={limit}'
                rf'&filter\.offset={offset}$'
            )
            mock_response.get(
                pattern,
                payload={
                    "data": chunk,
                    "total_rows": total_rows,
                    "total_summ": sum(op["summ"] for op in chunk),
                },
                repeat=True,
            )

        # Запускаем метод
        operations = await api_client.parallel_get_operations(
            date_from=date_from,
            date_to=date_to,
        )

        # Проверяем количество собранных операций
        assert len(operations) == total_rows

        # Проверяем содержимое операций
        for op, fake_op in zip(operations, fake_data):
            assert op.operation_id == fake_op["operation_id"]
            assert op.operation_type == fake_op["operation_type"]
            assert op.pickpoint_id == fake_op["pickpoint_id"]
            assert op.employee_id == fake_op["employee_id"]
            assert op.summ == fake_op["summ"]
            assert op.created == fake_op["created"]