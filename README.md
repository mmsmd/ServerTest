# 服务器自动化测试框架

这个自动化测试框架基于 `pytest`，用于通过 SSH 和 Telnet 连接远程服务器进行自动化测试。框架支持多个测试用例，包括 BMC WEB端功能测试、HOST侧接口测试以及 Redfish 测试。测试过程中的日志会被记录并保存在本地，便于随时查看。

## 主要功能

- **SSH/Telnet 远程控制**：可以通过 SSH 或 Telnet 连接到远程服务器执行命令，获取测试数据。
- **自动清理 `dmesg` 日志**：在每个测试开始前清除 `dmesg` 日志，确保测试环境干净。
- **自动检查 `dmesg` 错误**：每个测试用例结束后，自动检查 `dmesg` 日志，判断是否有错误信息。
- **日志记录**：每个测试用例执行过程中生成详细的日志文件，日志文件名以测试用例名和时间戳为命名规则。
- **控制台输出和日志文件双重记录**：支持将日志同时输出到控制台和保存到日志文件中。

## 环境要求

- Python 3.x
- pytest
- paramiko (用于 SSH 连接)
- telnetlib (用于 Telnet 连接)
- 其他依赖：请参考 `requirements.txt` 文件

## 安装与依赖

1. 克隆此仓库：

   ```bash
   git clone <repository_url>
   ```

2. 安装所需依赖：

   ```bash
   cd <your_project_directory>
   pip install -r requirements.txt
   ```

3. 确保你的机器上已安装 `pytest`，如果没有安装，请通过以下命令安装：

   ```bash
   pip install pytest
   ```

## 项目结构

```plaintext
<ServerTest>/
├── conftest.py                # Pytest 配置文件，包含 Fixture 和其他初始化操作
├── tests/                     # 测试用例目录
│   ├── test_example.py        # 示例测试用例
│   └── ...                    # 其他测试用例
├── utils/                     # 工具类，包括日志、SSH/Telnet 客户端等
│   ├── logger.py              # 日志处理模块
│   └── ssh_client.py          # SSH 客户端模块
├── config/                    # 环境配置目录
│   ├── bmc_credentials.yaml   # BMC信息配置文件
│   ├── ssh_config.yaml        # SSH信息配置文件
│   └── telnet_config.yaml     # Telnet信息配置文件
├── modules/                   # 模块代码目录
├── logs/                      # 日志目录
├── requirements.txt           # 项目依赖包
└── README.md                  # 本文档
```

### `conftest.py`

`conftest.py` 文件包含全局配置，主要用于定义 `pytest` 的 fixture，例如创建 SSH 客户端、Telnet 客户端以及配置日志记录器。每个测试用例都会通过 fixture 注入所需的资源。

### `tests/` 文件夹

在 `tests/` 文件夹下，每个 Python 文件代表一个测试用例模块。每个测试用例都会通过 SSH 或 Telnet 连接远程服务器，执行相应的操作，并根据结果判断是否通过。

### `utils/` 文件夹

该文件夹包含了工具类，如 `logger.py` 负责日志处理，`ssh_client.py` 提供 SSH 连接和命令执行的功能。你可以根据需要添加其他工具模块。

## 使用方法

### 运行单个测试用例

你可以使用 `pytest` 运行指定的测试用例，命令如下：

```bash
pytest tests/test_example.py
```

### 运行所有测试用例

你也可以运行整个测试文件夹下的所有测试用例：

```bash
pytest tests/
```

### 查看日志

- 每个测试用例执行时，会在 `logs/` 目录下生成一个以测试用例名为文件夹名的日志文件夹。
- 每个日志文件的文件名包含测试用例名和时间戳，例如 `test_example_20231102_130305.log`。

## 测试过程示例

### 1. 清除 `dmesg` 日志

在每个测试用例开始前，会自动清除远程服务器上的 `dmesg` 日志，确保测试开始时环境干净。

### 2. 执行测试

每个测试用例会通过 SSH 或 Telnet 执行命令并进行相应的验证。例如，对于 `ping` 测试，测试用例会检查主机的可达性。

```python
def test_host_ping(ssh_client, logger, clear_and_check_dmesg):
    # 使用 SSH 测试主机可访问性
    response = ssh_client.execute_command("ping -c 4 192.168.8.1")
    logger.info(f"Response: {response}")
    # 使用正则表达式匹配
    pattern = r'(\d+) packets transmitted, (\d+) received'
    match = re.search(pattern, response)
    # 断言丢包情况
    if match:
        packets_transmitted = int(match.group(1))
        packets_received = int(match.group(2))
        assert packets_transmitted == packets_received, "Packet loss detected"
```

### 3. 检查 `dmesg` 日志

每个测试用例结束后，会自动查询 `dmesg` 日志，查找是否有错误信息。如果存在错误，测试将会失败。

### 示例日志输出

#### 控制台输出

```bash
Starting test: test_host_ping
Response: PING 192.168.8.1 (192.168.8.1) 56(84) bytes of data.
64 bytes from 192.168.8.1: icmp_seq=1 ttl=64 time=1.17 ms
...
Finished test: test_host_ping
```

#### 日志文件

```plaintext
20231102_130305.log
--------------------------------------------------------
2023-11-02 13:03:05,123 - test_host_ping - INFO - Starting test: test_host_ping
2023-11-02 13:03:06,456 - test_host_ping - INFO - Response: PING 192.168.8.1 (192.168.8.1) 56(84) bytes of data.
2023-11-02 13:03:06,789 - test_host_ping - INFO - Finished test: test_host_ping
```

## 常见问题

### 1. 测试用例执行失败，提示 `dmesg` 中有错误信息

- 请检查 `dmesg` 日志是否包含与硬件或系统相关的错误信息。如果存在错误，可以根据日志内容定位问题。

### 2. 如何修改日志输出路径？

- 如果你需要修改日志的保存路径，可以在 `logger.py` 中修改日志文件路径配置。

### 3. 如何添加新的测试用例？

- 你可以在 `tests/` 文件夹下创建新的 Python 文件，编写新的测试用例，并使用 SSH 或 Telnet 执行相应命令进行验证。确保每个测试用例的日志记录和 `dmesg` 检查都符合规范。

## 贡献

欢迎提交问题和 PR！如果你发现任何 bug 或有改进建议，欢迎提 issue 或 PR。

## 许可证

此项目使用 MIT 许可证，详细信息请查看 [LICENSE](LICENSE) 文件。

```

### 说明：
1. **项目概述**：简要介绍了框架的功能和目标，帮助用户快速了解这个框架的主要用途。
2. **环境要求**：列出了该框架所需的 Python 环境和依赖库。
3. **安装与依赖**：介绍了如何安装和配置项目环境。
4. **使用方法**：包含了如何运行测试用例，如何查看日志以及如何运行所有测试用例。
5. **日志说明**：说明了日志的输出格式，以及如何修改日志的路径。
6. **常见问题**：列出了可能遇到的一些问题和解决方法。
7. **贡献指南**：鼓励用户参与到项目中，提出问题或贡献代码。

希望这个 `README.md` 能帮助你和其他开发人员快速理解和使用这个框架。如果有其他需求或修改，随时告诉我！
