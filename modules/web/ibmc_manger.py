import json

from selenium.webdriver.common.by import By
from conftest import bmc_client
from modules.common import load_nav_map

def change_net_mode(bmc_client, net_mode):
    """
    修改网络模式

    :param net_mode: 固定设置 "net_mode_manual" 自动设置 "net_mode_auto"
    """
    element_id = load_nav_map().get(net_mode.lower())
    bmc_client.driver.find_element(By.ID, element_id).click()
    bmc_client.driver.find_element(By.ID, "modeButton").click()


