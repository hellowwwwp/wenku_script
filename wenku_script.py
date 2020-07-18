from utils import *
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

# 指定要爬取的百度文库链接
WENKU_URL = "https://wenku.baidu.com/view/38a170fda800b52acfc789eb172ded630b1c98f8.html?fr=search"

# 开始加载页面的超时时间,一般不建议修改. 如果总是获取不到数据可以尝试把事件给大一点.因为百度文库的页面是懒加载形式
PAGE_LOAD_TIMEOUT = 8
# 正常寻找页面元素等待的最大超时时间, 一般不建议修改
NORMAL_FIND_ELEMENT_TIMEOUT = 30
# 生成文件的文件名
WENKU_FILE = "result.txt"

# 继续阅读按钮的class, 如果发现页面明明有[继续阅读]按钮但是脚本抓不到,就将新的class添加到这里
MORE_BUTTON_CLASS = ["moreBtn", "read-all"]


def search_webku(driver: WebDriver):
    print("开始加载网页..")
    try:
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        driver.set_script_timeout(PAGE_LOAD_TIMEOUT)
        driver.get(WENKU_URL)
        driver.set_page_load_timeout(NORMAL_FIND_ELEMENT_TIMEOUT)
        driver.set_script_timeout(NORMAL_FIND_ELEMENT_TIMEOUT)
    except:
        # 不要停止加载网页, 因为子page的内容需要懒加载
        # driver.execute_script("window.stop()")
        pass

    # 点击继续阅读加载所有子页面
    print("页面加载成功,尝试寻找[继续阅读]按钮")
    find_more_butto_and_click(driver)

    text = ""
    page_div_list: List[WebElement] = driver.find_elements_by_class_name("reader-page")
    print(f"共找到{len(page_div_list)}页, 开始循环解析..")
    for index in range(0, len(page_div_list)):
        page_div = page_div_list[index]
        # 滚动网页到指定page
        driver.execute_script("arguments[0].scrollIntoView();", page_div)
        # 懒加载page中的内容
        wait_until_found_p_element(driver)
        # 获取当前page的内容
        text += get_page_text(page_div)
        print(f"第{index + 1}页数据解析成功")

    # 消除多余的换行符
    text = remove_needless_newline(text)

    print("所有页面解析完成, 准备写入文件")
    print(f"\n---------start--------\n{text}\n---------end--------")

    with open(WENKU_FILE, "w") as wf:
        wf.write(text)
    print(f"所有页面数据已写入 [{WENKU_FILE}] 中")


def remove_needless_newline(text: str) -> str:
    """
    消除指定字符串中多余的换行符
    :param text:
    :return: str
    """
    text = text.replace("（\n）", "（）") \
        .replace("(\n)", "()") \
        .replace("[\n]", "[]") \
        .replace("{\n}", "{}") \
        .replace("<\n>", "<>") \
        .replace("《\n》", "《》") \
        .replace("【\n】", "【】")
    return text


def find_more_butto_and_click(driver: WebDriver):
    more_button = None
    for more_btn_class in MORE_BUTTON_CLASS:
        try:
            more_button = driver.find_element_by_class_name(more_btn_class)
        except:
            pass
        if more_button is not None:
            print("点击[继续阅读]按钮,加载所有子页面")
            driver.execute_script("arguments[0].click();", more_button)
            time.sleep(2)
            return
    print("没有找到[继续阅读]按钮")


def wait_until_found_p_element(driver: WebDriver, timeout=8, init_delay=1, interval_delay=0.5):
    time.sleep(init_delay)
    start_time = time.time()
    while True:
        # 判断p标签是否加载完成, 然后退出循环
        try:
            p_element: WebDriver = driver.find_elements_by_class_name("reader-word-layer")
            if p_element is not None:
                return
        except:
            pass
        # 判断是否超时
        if time.time() - start_time >= timeout:
            return None
        # 继续等待加载
        time.sleep(interval_delay)


def get_page_text(page_div: WebElement) -> str:
    p_list: List[WebElement] = page_div.find_elements_by_tag_name("p")
    count = len(p_list)
    text = ""
    for i in range(0, count):
        p_text: str = p_list[i].text.strip()
        if i == 0 or i == count - 1:
            text += p_text
        else:
            if p_text.strip() == "":
                next_text = p_list[i + 1].text.strip()
                if next_text == "":
                    text += ""
                else:
                    text += "\n"
            else:
                text += p_text.strip()
    return text


def main():
    # 启动一个google浏览器进程
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    # driver = webdriver.Chrome()
    try:
        search_webku(driver)
    finally:
        driver.close()


if __name__ == "__main__":
    main()
