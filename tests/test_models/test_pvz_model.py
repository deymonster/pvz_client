from pvz_client.models.Pvzmodel import PickpointModel

def test_pickpoint_model_initialization():
    """Тест инициализации модели PickpointModel"""
    data = {
        "id": 1,
        "name": "Test Location",
        "latitude": "55.7558",
        "longitude": "37.6173",
        "is_active": True,
        "external_id": 1001,
        "rate": 4.5,
        "users": [
            {
                "user_id": 1,
                "name": "John",
                "last_name": "Doe",
                "phone": 1234567890,
                "is_deleted": False
            }
        ]
    }
    model = PickpointModel(**data)

    # Проверяем поля модели
    assert model.id == 1
    assert model.name == "Test Location"
    assert model.latitude == "55.7558"
    assert model.longitude == "37.6173"
    assert model.is_active is True
    assert model.external_id == 1001
    assert model.rate == 4.5
    assert len(model.users) == 1
    assert model.users[0].user_id == 1
    assert model.users[0].name == "John"
    assert model.users[0].last_name == "Doe"
    assert model.users[0].phone == 1234567890
    assert model.users[0].is_deleted is False
