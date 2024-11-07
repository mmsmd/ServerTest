import paramiko

class SSHClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, port=self.port, username=self.username, password=self.password)

    #获取所有输出，包括标准输出stdout和标准错误stderr
    def execute_command_all(self, command):
        if not self.client:
            raise Exception("SSH client is not connected")
        stdin, stdout, stderr = self.client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        return stdout.read().decode(), stderr.read().decode()

    # 获取所有输出，只包括标准输出stdout
    def execute_command(self, command):
        if not self.client:
            raise Exception("SSH client is not connected")
        stdin, stdout, _ = self.client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        return stdout.read().decode()

    def close(self):
        if self.client:
            self.client.close()
