
import pytest

from modules.common import check_values
from modules.web.home import get_home_product_name
from modules.web.ibmc_manger import change_net_mode
from modules.web.nav import change_nav


def test_bmc_change_netmod(bmc_client, logger):
    """测试 BMC 登录并获取主机名"""
    bmc_client.start_driver()
    bmc_client.login()
    change_nav(bmc_client,"nav_manager")
    change_net_mode(bmc_client, "net_mode_auto")
