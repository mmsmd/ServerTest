from modules.redfish.system import get_system_info

def test_redfish_system_info(redfish_client):
    # 通过 Redfish 检查系统信息
    response = get_system_info(redfish_client)
    assert "Members" in response, "Redfish system information is missing"
