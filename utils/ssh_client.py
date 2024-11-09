import time
from logging import raiseExceptions

import paramiko
from paramiko.ssh_exception import NoValidConnectionsError


class SSHClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        if self.client is not None:
            return  # 如果已经连接，就不再重复连接

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            print(f"Connecting to {self.host}:{self.port} with username {self.username}")
            self.client.connect(self.host, port=self.port, username=self.username, password=self.password)
            print("SSH connection established successfully!")
        except Exception as e:
            print(f"Failed to connect to {self.host}:{self.port} - {e}")
            self.client = None
            raise  # 如果连接失败，抛出异常

    def reconnect(self, wait_time):
        # 重新尝试连接直到服务器恢复

        for _ in range(wait_time // 10):
            try:
                self.connect()  # 尝试重新连接
                print("Server rebooted and SSH connection restored.")
                return True
            except (NoValidConnectionsError, TimeoutError, paramiko.SSHException) as e:
                print(f"Server still rebooting... waiting for 3 seconds. Error: {e}")
                time.sleep(5)
        print("Failed to reconnect after waiting for reboot.")
        return False

    def execute_command_all(self, command):
        if not self.client:
            raise Exception("SSH client is not connected")

        stdin, stdout, stderr = self.client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        return stdout.read().decode(), stderr.read().decode()

    def execute_command(self, command):
        if not self.client:
            raise Exception("SSH client is not connected")

        stdin, stdout, stderr = self.client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        return stdout.read().decode()

    def execute_command_only(self, command):
        if not self.client:
            raise Exception("SSH client is not connected")
        self.client.exec_command(command)

    def close(self):
        if self.client:
            print(f"Closing SSH connection to {self.host}")
            self.client.close()
            self.client=None


