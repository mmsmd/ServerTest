import pytest
import json
import os


def check_values(expected, actual, check_type="equal", tolerance=None):
    """
    检查预期值和实际值是否一致。

    :param expected: 预期的值
    :param actual: 实际得到的值
    :param check_type: 检查类型，默认为"equal"（值相等），也支持"greater_than"（大于），"less_than"（小于）
    :param tolerance: 对于浮动值的容忍度，默认为None，不考虑容忍度。
    :raises AssertionError: 如果检查失败
    """

    if check_type == "equal":
        if expected != actual:
            raise AssertionError(f"Expected value {expected}, but got {actual}.")

    elif check_type == "greater_than":
        if not (actual > expected):
            raise AssertionError(f"Expected value greater than {expected}, but got {actual}.")

    elif check_type == "less_than":
        if not (actual < expected):
            raise AssertionError(f"Expected value less than {expected}, but got {actual}.")

    elif check_type == "approx_equal" and tolerance is not None:
        # 对浮动值使用容忍度进行检查
        if abs(expected - actual) > tolerance:
            raise AssertionError(
                f"Expected value {expected} to be approximately equal to {actual} with tolerance {tolerance}, but the difference is too large.")

    else:
        raise ValueError(f"Unsupported check type: {check_type}")

    # 如果检查通过，不做任何操作
    print(f"Check passed: {expected} {check_type} {actual}")

def load_nav_map(config_file_path="../../config/element_map.json"):
    """加载导航名称到 ID 的映射"""
    # 确保路径正确，并读取 JSON 文件
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"Config file not found: {config_file_path}")

    with open(config_file_path, "r") as file:
        nav_map = json.load(file)
    return nav_map

