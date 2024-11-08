import os

import pytest
import yaml

from server_selector import load_selected_server
from utils.logger import create_logger
from utils.ssh_client import SSHClient
from utils.telnet_client import TelnetClient
from utils.redfish_client import RedfishClient
from utils.bmc_web_client import BMCWebClient

@pytest.fixture(scope="session")
def selected_server():
    # 获取选中的服务器
    server = load_selected_server()
    print("选中的服务器：", server)
    return server

@pytest.fixture(scope="session")
def ssh_client(selected_server):
    # 使用选中的服务器配置创建 SSH 客户端
    client = SSHClient(
        host=selected_server["host"],
        username=selected_server["username"],
        password=selected_server["password"],
        port=selected_server["port"]
    )
    return client

@pytest.fixture(scope="session")
def telnet_client(selected_server):
    # 使用选中的服务器配置创建 Telnet 客户端
    client = TelnetClient(
        host=selected_server["telnet"]["host"],
        port=selected_server["telnet"]["port"],
        username=selected_server["telnet"]["username"],
        password=selected_server["telnet"]["password"]
    )
    return client

@pytest.fixture(scope="session")
def bmc_client(selected_server):
    # 使用选中的服务器配置创建 BMC 客户端
    client = BMCWebClient(
        host=selected_server["bmc_web"]["host"],
        port=selected_server["bmc_web"]["port"],
        username=selected_server["bmc_web"]["username"],
        password=selected_server["bmc_web"]["password"]
    )
    return client

# 使用 request 获取当前用例名，并为每个用例创建独立的 logger
@pytest.fixture(scope="function", autouse=True)
def logger(request):
    test_name = request.node.name  # 获取当前测试用例的名称
    logger = create_logger(test_name)
    return logger

@pytest.fixture(scope="function", autouse=True)
def clear_and_check_dmesg(ssh_client, logger):
    # 确保 SSH 客户端已连接
    if not ssh_client.client:
        logger.info("SSH client not connected, attempting to connect.")
        ssh_client.connect()

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
