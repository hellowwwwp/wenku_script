import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def is_none_or_null(s) -> bool:
    return s is None or len(str(s)) == 0


def is_not_null(s) -> bool:
    return s is not None and len(str(s)) > 0


def find_element_by_xpath(driver: WebDriver, xpath: str):
    try:
        return driver.find_element_by_xpath(xpath)
    except:
        return None


def find_element_by_xpath2(element: WebElement, xpath: str):
    try:
        return element.find_element_by_xpath(xpath)
    except:
        return None


def get_ftime() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
