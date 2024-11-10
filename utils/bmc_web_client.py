import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class BMCWebClient:
    def __init__(self, host, port , username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.driver = None

    def start_driver(self):
        """初始化 Chrome WebDriver"""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()  # 最大化窗口
        print("Starting ChromeDriver...")
        bmc_url = self.host
        self.driver.get(bmc_url)
        time.sleep(2)  # 等待页面加载

    def login(self):
        """登录到 BMC Web 界面"""
        # 查找用户名和密码输入框并输入数据
        WebDriverWait(self.driver, 10)
        username_field = self.driver.find_element(By.ID, "account")
        password_field = self.driver.find_element(By.ID, "loginPwd")

        username_field.send_keys(self.username)  # 输入用户名
        password_field.send_keys(self.password)  # 输入密码

        # 提交表单
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)  # 等待页面加载

        print("Logged in successfully.")

    def logout(self):
        """登出操作"""
        logout_button = self.driver.find_element(By.ID, "logout_button")  # 根据实际元素定位
        logout_button.click()
        print("Logged out successfully.")
        self.driver.quit()  # 关闭浏览器

    def perform_operation(self):
        """执行一系列操作，例如重启服务器"""
        self.start_driver()
        self.login()
        # self.logout()
