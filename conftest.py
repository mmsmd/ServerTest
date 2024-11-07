import os

import pytest
import yaml

from utils.logger import create_logger
from utils.ssh_client import SSHClient
from utils.telnet_client import TelnetClient
from utils.redfish_client import RedfishClient

# CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config/telnet_config.yaml")


@pytest.fixture(scope="module")
def ssh_client():
    with open("E:/AutoServer/ServerTest/config/ssh_config.yaml") as f:
        config = yaml.safe_load(f)
    client = SSHClient(config['host'], config['port'], config['username'], config['password'])
    client.connect()
    yield client
    client.close()

@pytest.fixture(scope="module")
def telnet_client():
    with open("E:/AutoServer/ServerTest/config/telnet_config.yaml") as f:
        config = yaml.safe_load(f)
    client = TelnetClient(config['host'], config['port'], config['username'], config['password'])
    client.connect()
    yield client
    client.close()

@pytest.fixture(scope="module")
def redfish_client():
    with open("config/bmc_credentials.yaml") as f:
        config = yaml.safe_load(f)
    client = RedfishClient(config['bmc_url'], config['username'], config['password'])
    return client

# 使用 request 获取当前用例名，并为每个用例创建独立的 logger
@pytest.fixture(scope="function", autouse=True)
def logger(request):
    test_name = request.node.name  # 获取当前测试用例的名称
    logger = create_logger(test_name)
    return logger

@pytest.fixture(scope="function", autouse=True)
def clear_and_check_dmesg(ssh_client, logger):
    # 清除 dmesg 日志
    logger.info("Clearing dmesg logs before test execution.")
    logger.info("==================================================================================")
    ssh_client.execute_command("dmesg -C")  # 清除 dmesg 缓存

    # 执行测试前，确保清除 dmesg 后没有错误
    yield

    # 测试结束后，检查 dmesg 中是否有错误信息
    logger.info("==================================================================================")
    logger.info("Checking dmesg for errors after test execution.")
    dmesg_output = ssh_client.execute_command("dmesg")
    if "error" in dmesg_output.lower() or "warn" in dmesg_output.lower():
        logger.error("Found errors or warnings in dmesg logs:")
        logger.error(dmesg_output)
        pytest.fail(f"dmesg log contains errors or warnings: {dmesg_output}")
    else:
        logger.info("No errors or warnings found in dmesg logs.")
