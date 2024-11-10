import time
import paramiko
from paramiko.ssh_exception import NoValidConnectionsError
import logging


class SSHClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        self.logger = logging.getLogger(__name__)

    def connect(self):
        if self.client is not None:
            return  # If already connected, do nothing

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self.logger.info(f"Connecting to {self.host}:{self.port} with username {self.username}")
            self.client.connect(self.host, port=self.port, username=self.username, password=self.password)
            self.logger.info("SSH connection established successfully!")
        except Exception as e:
            self.logger.error(f"Failed to connect to {self.host}:{self.port} - {e}")
            self.client = None
            raise  # Re-raise the exception if the connection fails

    def reconnect(self, wait_time, max_attempts=10):
        # Retry connecting until the server recovers or max attempts are reached
        attempt = 0
        while attempt < max_attempts:
            try:
                self.connect()  # Try to reconnect
                self.logger.info("Server rebooted and SSH connection restored.")
                return True
            except (NoValidConnectionsError, TimeoutError, paramiko.SSHException) as e:
                attempt += 1
                self.logger.warning(f"Server still rebooting... waiting for {2 ** attempt} seconds. Attempt {attempt}/{max_attempts}. Error: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
        self.logger.error("Failed to reconnect after maximum attempts.")
        return False

    def execute_command_all(self, command):
        self._check_connection()

        stdin, stdout, stderr = self.client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        return stdout.read().decode(), stderr.read().decode()

    def execute_command(self, command):
        self._check_connection()

        stdin, stdout, stderr = self.client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        return stdout.read().decode()

    def execute_command_only(self, command):
        self._check_connection()
        self.client.exec_command(command)

    def close(self):
        if self.client:
            self.logger.info(f"Closing SSH connection to {self.host}")
            self.client.close()
            self.client = None

    def _check_connection(self):
        if not self.client:
            raise Exception("SSH client is not connected")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()