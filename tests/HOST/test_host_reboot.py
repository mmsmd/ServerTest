import re

import pytest

from modules.common import check_values
from modules.host.system import ping_host


def test_host_reboot(ssh_client, logger):
    # 记录测试用例开始
    logger.info("Starting test: test_host_reboot")

    # 使用 SSH 测试主机可访问性
    result = ping_host("192.168.8.1")
    logger.info(f"result:{result}")

    # 使用正则表达式匹配
    pattern = r'(\d+) packets transmitted, (\d+) received'
    match = re.search(pattern, result)

    # 检查匹配的结果
    if match:
        packets_transmitted = int(match.group(1))
        packets_received = int(match.group(2))
        check_values(packets_transmitted, packets_received, check_type="equal")
    else:
        pytest.fail("Ping statistics not found in response")