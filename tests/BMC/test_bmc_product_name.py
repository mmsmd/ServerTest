import pytest

from modules.common import check_values
from modules.web.home import get_home_product_name
from modules.web.nav import change_nav


def test_bmc_product_name(bmc_client, logger):
    """测试 BMC 登录并获取主机名"""
    bmc_client.start_driver()
    bmc_client.login()
    change_nav(bmc_client, "nav_home")
    product_name = get_home_product_name(bmc_client, "home_product_name")
    check_values("1288H V6", product_name, check_type="equal")
