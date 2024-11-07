import telnetlib

class TelnetClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        self.client = telnetlib.Telnet(self.host, self.port)
        self.client.read_until(b"login: ")
        self.client.write(self.username.encode('ascii') + b"\n")
        self.client.read_until(b"Password: ")
        self.client.write(self.password.encode('ascii') + b"\n")

    def execute_command(self, command):
        self.client.write(command.encode('ascii') + b"\n")
        return self.client.read_all().decode('ascii')

    def close(self):
        if self.client:
            self.client.close()
