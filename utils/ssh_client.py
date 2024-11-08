import paramiko


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
            raise  # 如果连接失败，抛出异常

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

    def close(self):
        if self.client:
            print(f"Closing SSH connection to {self.host}")
            self.client.close()
