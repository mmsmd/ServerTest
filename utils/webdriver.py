import time

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

class HighlightedWebDriver(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        super(HighlightedWebDriver, self).__init__(*args, **kwargs)

    def find_element(self, *args, **kwargs):
        """重写 find_element，返回自定义的 HighlightedWebElement"""
        element = super(HighlightedWebDriver, self).find_element(*args, **kwargs)
        return HighlightedWebElement(element, self)

    def find_elements(self, *args, **kwargs):
        """重写 find_elements，返回自定义的 HighlightedWebElement 列表"""
        elements = super(HighlightedWebDriver, self).find_elements(*args, **kwargs)
        return [HighlightedWebElement(e, self) for e in elements]

class HighlightedWebElement(WebElement):
    def __init__(self, element, driver):
        super(HighlightedWebElement, self).__init__(driver, element._id)
        self._element = element
        self._driver = driver

    def highlight(self, duration=0.5):
        """高亮元素"""
        # 获取原始样式，调用父类的 get_attribute 以避免递归
        original_style = super(HighlightedWebElement, self).get_attribute('style')

        # 使用 JavaScript 设置高亮样式
        self._driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            self, "border: 3px solid red; background-color: yellow;"
        )

        # 等待指定的时间来显示高亮效果
        time.sleep(duration)

        # 恢复原始样式
        self._driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            self, original_style
        )

    def click(self, *args, **kwargs):
        """重写 click 方法，添加高亮效果"""
        self.highlight()  # 先高亮
        super(HighlightedWebElement, self).click(*args, **kwargs)  # 然后点击

    def send_keys(self, *args, **kwargs):
        """重写 send_keys 方法，添加高亮效果"""
        self.highlight()  # 先高亮
        super(HighlightedWebElement, self).send_keys(*args, **kwargs)  # 然后发送按键

    def clear(self):
        """重写 clear 方法，添加高亮效果"""
        self.highlight()  # 先高亮
        super(HighlightedWebElement, self).clear()  # 然后清除输入框内容

    def get_attribute(self, name):
        """重写 get_attribute 方法，但不进行高亮以避免递归"""
        # 直接调用父类的方法来获取属性，避免调用重写的 get_attribute() 自身
        return super(HighlightedWebElement, self).get_attribute(name)

    @property
    def text(self):
        """重写 text 属性，添加高亮效果"""
        self.highlight()  # 先高亮
        return super(HighlightedWebElement, self).text
