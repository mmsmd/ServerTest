from modules.host.system import reboot


def test_host_reboot(ssh_client, logger):
    # 记录测试用例开始
    logger.info("Starting test: test_host_reboot")

    # 通过reboot来复位
    reboot(ssh_client,logger)
