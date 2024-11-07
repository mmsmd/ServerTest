import re

import pytest

from modules.common import check_values
from modules.host.system import ping_host


def test_host_ping_latency(ssh_client, logger):
    logger.info("Starting test: test_host_ping_latency")

    response = ping_host(ssh_client, "192.168.8.1")
    logger.info(f"response: {response}")

    # 假设你需要提取延迟值
    pattern = r'time=(\d+.\d+) ms'
    match = re.search(pattern, response)

    if match:
        latency = float(match.group(1))

        # 检查延迟是否在预期范围内
        check_values(expected=100, actual=latency, check_type="less_than")
    else:
        pytest.fail("Latency not found in ping response")
