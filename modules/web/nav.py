from selenium.webdriver.common.by import By
from conftest import bmc_client
import time

from modules.common import load_nav_map


def change_nav(bmc_client, nav_name):
    """
    切换nav

    :param nav_name: 要切换的nav名称, "nav_home"(首页) "nav_manager"(管理)
    """
    element_id = load_nav_map().get(nav_name.lower())
    nav_button = bmc_client.driver.find_element(By.ID, element_id)
    nav_button.click()
    print(f"Enter the {nav_name} interface...")
    time.sleep(3)



