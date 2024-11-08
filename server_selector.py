import json
import os
from pathlib import Path


def get_project_root() -> Path:
    # 获取当前脚本文件的路径，然后返回项目根目录
    return Path(__file__).parent


def load_selected_server(config_file_path="config/server_config.json"):
    # 获取项目根目录
    project_root = get_project_root()

    # 拼接 config 路径
    config_path = project_root / config_file_path

    # 检查 config 文件是否存在
    if not config_path.exists():
        raise FileNotFoundError(f"配置文件未找到: {config_path}")

    with open(config_path, 'r') as f:
        config = json.load(f)

    selected_server_name = config.get("selected_server", "")
    if not selected_server_name:
        raise ValueError("未选择要测试的服务器")

    # 加载所有服务器配置
    servers = load_servers_from_json(project_root / "config/servers.json")

    # 查找选中的服务器配置
    selected_server = None
    for server in servers:
        if server["name"] == selected_server_name:
            selected_server = server
            break

    if not selected_server:
        raise ValueError(f"未找到名为 {selected_server_name} 的服务器")

    return selected_server


def load_servers_from_json(file_path):
    # 加载所有服务器配置
    with open(file_path, 'r') as f:
        return json.load(f)["servers"]
