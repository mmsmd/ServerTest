def test_redfish_system_info(redfish_client):
    # 通过 Redfish 检查系统信息
    response = redfish_client.get_system_info()
    assert "Members" in response, "Redfish system information is missing"
