'''
   关键字驱动类
   一般再常态化中，考虑封装各类操作行为，作为关键字驱动的核心底层结构
   以工具类的形态，便于其他的类来进行调用
   常用的操作行为：
        1、访问url
        2、创建driver对象
        3、元素定位
        4、三类等待
        5、输入、点击
        6、切换iframe和句柄
    。。。
    封装的概念上，我们优先靠考虑自己用的上的内容，进行封装

'''
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
# from optins_webui_pg06 import options
from optins_webui_key import options
# from Day10check_shortof.optins_webui_pg06 import options
# from Day10check_shortof.logmoudle04_2 import test_log2
# from logmoudle04_2 import test_log2
from logmoudle import test_log2

#日志实例化


log2=test_log2()# loggeer组件封装实例化

#构造浏览器对象，基于type_参数，构造对应的浏览器对象
def open_browser(type_):
    '''
        getattr是python内置的四大函数之一，反射机制，用于获取指定对象的成员属性或者函数
        driver= getattr(webdriver,type_)()意思就是--driver=webdriver.type_()
        if type_=='Chrome':
            driver=webdriver.Chrome()
        elif type_=='Edge':
            driver=webdriver.Edge()
        elif...
        因为反射本身是用来获取指定对象属性的，如果要获取的是函数，则需要在反射后面加()
        例如：getattr(webdriver,type_)  表示获取webdriver的type_属性
        getattr(webdriver,type_)()  表示获取webdriver的type_函数
    '''
    # 方式一：反射：必须严格要求用户的输入规范
    try:
        if type_=='Chrome':
            driver= webdriver.Chrome(options=options())
        else:
            driver= getattr(webdriver,type_)()
    except:
        # #可以考虑通过三方工具(测码？)safedriver来实现chrome浏览器对象的生成(没有安装源)
        # driver=SafeDriver.driver.driver()
        driver=webdriver.Chrome()

    return driver

    # #方式二： 这种写法更好的满足用户调用需求
    # browser={"chrome":"['Chrome','chrome','cc','谷歌']","ie":"['ie','IE','Ie','iE']"}
    # # chrome=['Chrome','chrome','cc','谷歌']
    # # ie=['ie','IE','Ie','iE']
    # if type_ in browser["chrome"]:
    #     driver = webdriver.Chrome(options=options())
    # elif type_ in browser['ie']:
    #     drover=webdriver.Ie()
    # else:
    #     driver=webdriver.Chrome()
    #
    # return driver


class WebUiKeys():
    #driver对象
    # driver = webdriver.Chrome()
    def __init__(self,type_):
        self.driver=open_browser(type_)
        self.driver.implicitly_wait(5)
        #防反爬
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator,'webdriver', {
                    get: () => false
                })
            """
        })

    #url访问
    def open(self,url):
        self.driver.get(url)
        #日志信息由 web_data_excel.py 中调用日志模块输出。try except是否使用，后续再看，先一并注释
        # try:
        #     self.driver.get(url)
        #     log2.info(f"成功访问{url}")
        # except Exception as a:
        #     log2.error(f"访问{url}失败，详情：{a}")

    #元素定位  这里一定要加return 因为元素的查找后必定伴随操作（点击、输入等），如果没有return，元素可以寻找但无法进行操作
    def locator(self,by,value):
        self.driver.find_element(by, value)
        return self.driver.find_element(by, value)
        # try:
        #     self.driver.find_element(by, value)
        #     log2.info(f"通过{by}方式的对应值{value}")
        #     return self.driver.find_element(by, value)
        # except Exception as a:
        #     log2.error(f"找不到名为{value}的{by}元素，具体：{a}")

    #获取元素文本
    def get_text(self,by,value):
        return self.locator(by,value).text

    #输入  不使用driver.find_element，而用封装好的方法---提高复用性
    def input(self,by,value,txt):
        self.locator(by, value).send_keys(txt)
        # try:
        #     self.locator(by,value).send_keys(txt)
        #     log2.info(f"成功输入{txt}")
        # except Exception as a:
        #     log2.error(f"输入失败{txt}，具体：{a}")

    #点击
    def click(self,by,value):
        self.locator(by,value).click()

    #鼠标悬停
    def mousestop(self,by,value):
        ActionChains(self.driver).move_to_element(self.locator(by,value)).perform()

    #选择框
    def selector(self,by,value,type_,type_value):
        select=Select(self.locator(by,value))
        getattr(select,type_)(type_value)

    #切换iframe
    def change_iframe(self,value,by=None):
        if by is None:
            self.driver.switch_to.frame(value)
        else:
            self.driver.switch_to.frame(self.locator(by,value))

    #浏览器的完全关闭
    def quit(self):
        self.driver.quit()

    # 浏览器的关闭窗口
    def close(self):
        self.driver.close()

    #文本断言完全相等
    def assert_text(self,by,value,expected):
        try:
            reality=self.locator(by,value).text
            assert expected == reality,f"{expected}与{reality}不相等，不符合预期"
            log2.info(f"{expected}与{reality}相等，符合预期")
            return True
        except Exception as e:
            # print(f"断言失败，详情：{e}")
            log2.error(f"断言失败，详情：{e}")
            return False

    #文本断言包含
    def assert_intext(self,by,value,expected):
        try:
            reality=self.locator(by,value).text
            assert expected in reality,f"{reality}中没有包含{expected}，不符合预期"
            log2.info(f"{reality}中包含{expected}，符合预期")
            return True
        except Exception as e:
            # print(f"断言失败，详情：{e}")
            log2.error(f"断言失败，详情：{e}")
            return False

    #强制等待
    def must_wait(self,timeto):
        time.sleep(timeto)

    #显示等待
    def smart_wait(self,by,value):
        return WebDriverWait(self.driver,10,0.5).until(lambda el: self.locator(by,value), message='显式等待失败')

if __name__ == '__main__':
    test=WebUiKeys("谷歌")
    test.open("https://www.baidu.com")