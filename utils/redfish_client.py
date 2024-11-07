import requests

class RedfishClient:
    def __init__(self, bmc_url, username, password):
        self.bmc_url = bmc_url
        self.username = username
        self.password = password

    def get_system_info(self):
        url = f"{self.bmc_url}/redfish/v1/Systems"
        response = requests.get(url, auth=(self.username, self.password), verify=False)
        return response.json()
