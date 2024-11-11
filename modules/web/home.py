from selenium.webdriver.common.by import By
from conftest import bmc_client
from modules.common import load_nav_map
from modules.web.nav import change_nav


def get_home_product_name(bmc_client, nav_name):
    """获取服务器类型"""
    element_id = load_nav_map().get(nav_name.lower())
    home_product_name = bmc_client.driver.find_element(By.ID, element_id).text
    return home_product_name


