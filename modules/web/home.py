from selenium.webdriver.common.by import By
from conftest import bmc_client
from modules.web.nav import change_nav


def get_home_product_name(bmc_client):
    """获取服务器类型"""
    change_nav(bmc_client,"navHome")
    home_product_name = bmc_client.driver.find_element(By.ID, "homeProductName").text
    return home_product_name


