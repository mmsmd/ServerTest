import requests
from requests.auth import HTTPBasicAuth

class RedfishClient:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.base_url = f"https://{host}/redfish/v1"

    def make_request(self, method, endpoint, data=None):
        """通用请求方法"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.request(
                method, url, auth=HTTPBasicAuth(self.username, self.password),
                json=data, verify=False  # 如果使用 https，可能需要设置 verify=False
            )
            response.raise_for_status()  # 如果响应状态码是 4xx 或 5xx，会抛出异常
            return response.json()  # 返回 JSON 格式的响应
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
