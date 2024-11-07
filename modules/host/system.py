# modules/host/ping.py

def ping_host(ssh_client, target_ip):
    """执行 ping 命令并返回结果"""
    command = f"ping -c 4 {target_ip}"
    response = ssh_client.execute_command(command)
    return response

