from pvz_client.models.AuthModel import RequestCodeResponse

def test_request_code_response_initialization():
    """Тест инициализации модели RequestCodeResponse"""
    data = {
        "data": "mock_data",
        "code": "12345",
        "code_length": 5
    }
    model = RequestCodeResponse(**data)
    assert model.data == "mock_data"
    assert model.code == "12345"
    assert model.code_length == 5
