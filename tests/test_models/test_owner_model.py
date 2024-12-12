from pvz_client.models.OwnerModel import OwnerInfoModel

def test_owner_info_model_initialization():
    """Тест инициализации модели OwnerInfoModel"""
    data = {
        "wb_user_id": 1,
        "phone": 1234567890,
        "name": "Owner Name",
        "org_name": "Test Org"
    }
    model = OwnerInfoModel(**data)
    assert model.wb_user_id == 1
    assert model.phone == 1234567890
    assert model.name == "Owner Name"
    assert model.org_name == "Test Org"
