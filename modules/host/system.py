import time

from conftest import ssh_client, logger


def ping_host(ssh_client, target_ip):
    """执行 ping 命令并返回结果"""
    command = f"ping -c 4 {target_ip}"
    response = ssh_client.execute_command(command)
    return response

def reboot(ssh_client, logger, wait_time=300):
    """通过reboot命令复位，并等待复位完成"""
    command = "reboot"
    logger.info("Rebooting server...")
    ssh_client.execute_command_only(command)
    # 等待服务器重启并恢复 SSH 连接
    print(f"Waiting for server to reboot... (up to {wait_time} seconds)")
    # 断开当前的 SSH 连接，等待服务器恢复
    ssh_client.close()
    time.sleep(3)  # 稍微等待一下，给服务器一些时间开始重启
    ssh_client.reconnect(wait_time)
