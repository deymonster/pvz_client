import pytest
from aioresponses import aioresponses
from pvz_client.api_auth import ApiAuth, HTTPException


@pytest.fixture
def api_auth():
    """Создание экземпляра ApiAuth для тестов."""
    return ApiAuth(
        auth_base_path="https://mock-auth.api",
        base_path="https://mock-api",
        verify=True,
        basic_token="mock_basic_token"
    )


@pytest.mark.asyncio
async def test_validate_success(api_auth):
    """Тест успешной валидации токена."""
    with aioresponses() as mock_response:
        mock_response.post(
            "https://mock-auth.api/api/v1/validate",
            payload={
                "access": {"token": "access_token", "ttl": 3600},
                "refresh": {"token": "refresh_token", "ttl": 7200},
                "ws_access": {"token": "ws_token", "ttl": 3600},
                "user_id": 123
            },
            status=200,
        )

        response = await api_auth.validate(code="1234", token="temp_token")

        # Проверяем результат
        assert response.access.token == "access_token"
        assert response.refresh.token == "refresh_token"
        assert response.ws_access.token == "ws_token"
        assert response.user_id == 123


@pytest.mark.asyncio
async def test_validate_error(api_auth):
    """Тест ошибки при валидации."""
    with aioresponses() as mock_response:
        mock_response.post(
            "https://mock-auth.api/api/v1/validate",
            payload={"error": "Invalid code"},
            status=400,
        )

        with pytest.raises(HTTPException) as excinfo:
            await api_auth.validate(code="1234", token="temp_token")

        # Проверяем, что выброшено правильное исключение
        assert excinfo.value.status_code == 400
        assert "Invalid code" in str(excinfo.value)


@pytest.mark.asyncio
async def test_request_content_type_error(api_auth):
    with aioresponses() as mock_response:
        mock_response.post(
            "https://mock-auth.api/api/v1/login",
            body="Invalid response",
            status=200,
            headers={"Content-Type": "text/html"},
        )
        with pytest.raises(HTTPException) as excinfo:
            await api_auth.login(phone="1234567890")
        assert "Invalid response from server" in str(excinfo.value)
