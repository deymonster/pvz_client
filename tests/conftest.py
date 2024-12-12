import os
import pytest

@pytest.fixture(scope="session", autouse=True)
def set_env_variables():
    """Устанавливает переменные окружения для тестов"""
    os.environ["DISCOVERY_URL"] = "https://mock-discovery.api"
    os.environ["S_POINT_URL"] = "https://mock-s-point.api"