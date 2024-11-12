from conftest import redfish_client, logger


def get_system_info(redfish_client):
    """获取系统信息"""
    return redfish_client.make_request('GET', 'Systems')


def get_health_status(redfish_client):
    """获取健康状态"""
    return redfish_client.make_request('GET', 'Systems/System.Embedded.1/Status')


def reboot_system(redfish_client):
    """重启服务器"""
    reboot_url = f"{redfish_client.base_url}/Systems/System.Embedded.1/Actions/ComputerSystem.Reset"
    payload = {"ResetType": "ForceRestart"}
    return redfish_client.make_request('POST', 'Systems/System.Embedded.1/Actions/ComputerSystem.Reset', data=payload)


def get_firmware_version(redfish_client):
    """获取固件版本"""
    return redfish_client.make_request('GET', 'Managers/1')
