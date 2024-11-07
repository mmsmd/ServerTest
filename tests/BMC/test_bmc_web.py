def test_bmc_web_login(ssh_client):
    # Example of running a command via SSH to verify a BMC web status
    stdout, stderr = ssh_client.execute_command("curl -s http://localhost:8080/status")
    assert "running" in stdout, "BMC Web service is not running"
