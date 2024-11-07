import requests

class BMCWebClient:
    def __init__(self, bmc_url, username, password):
        self.bmc_url = bmc_url
        self.username = username
        self.password = password

    def login(self):
        # 模拟登录 BMC Web 端，这里仅供参考，具体根据 BMC 的 API 调用
        response = requests.post(f"{self.bmc_url}/login", data={"username": self.username, "password": self.password})
        if response.status_code == 200:
            self.token = response.json().get("token")
        else:
            raise Exception("Failed to login to BMC")

    def perform_action(self, action):
        # 根据需要在 BMC Web 端执行特定操作
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{self.bmc_url}/actions/{action}", headers=headers)
        return response.status_code
