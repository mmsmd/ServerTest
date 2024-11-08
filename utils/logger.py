import logging
import os
import time

from tornado.template import Template


# 获取当前时间戳，用于生成日志文件名
def get_timestamp():
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())


# 配置日志
def create_logger(test_name):
    # 生成测试用例名对应的文件夹路径
    parent_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    test_log_dir = os.path.join(parent_dir, "logs", test_name)

    # 如果文件夹不存在，则创建它
    if not os.path.exists(test_log_dir):
        os.makedirs(test_log_dir)

    # 获取当前时间戳，作为日志文件名的一部分
    timestamp = get_timestamp()

    # 设置日志文件路径
    log_file = os.path.join(test_log_dir, f"{test_name}_{timestamp}.log")

    # 配置日志
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.INFO)  # 记录所有级别的日志

    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 创建文件处理器，保存日志到文件
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # 同时输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
