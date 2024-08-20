'''
        Chrome浏览器的配置项
'''

from selenium import webdriver
import time


def options(localcookies=False,withoutrepasswd=False,weblocal=False,websize=False,withouttips=False,useterminal=False,ysmode=False,headless=False,**kwargs):
    # 创建chrome 浏览器配置项
    options = webdriver.ChromeOptions()
    # #添加试验性质的配置项
    # options.add_experimental_option()
    # #添加常规设定
    # options.add_argument()

    # 使selenium执行完后不会自动关闭
    options.add_experimental_option('detach', True)
    # 浏览器最大化
    # options.add_argument('start-maximized')
    # 页面加载策略
    options.page_load_strategy = 'eager'

    if localcookies:
        # 读取本地缓存 webdriver启动时默认是不会加载本地缓存的，
        # 有时候想要绕过验证码或者登录流程可以使用读取本地缓存
        options.add_argument(r'--user-data-dir=C:\Users\Sunny\AppData\Local\Google\Chrome\User Data')

    if withoutrepasswd:
        #去掉账号密码弹出框  （一些页面登录后，浏览器会弹框询问是否要记录密码）
        prefs=dict()
        prefs['credentials_enable_service']=False
        prefs['profile.password_manager_enable']=False
        # 缺少了一行代码，用于调用这个字典
        options.add_experimental_option('prefs', prefs)

    if weblocal:
        # #指定位置启动浏览器
        options.add_argument(f'window-position={wlx},{wly}')
    if websize:
        # #设置窗体的启动大小
        options.add_argument(f'window-size={wsx},{wsy}')

    if withouttips:
        # #去掉浏览器提示自动化黄条：没有什么用处，只是为了好看而已
        options.add_experimental_option('excludeSwitches',['enable-automation'])
        # #下--只支持与2.7版本的selenium，目前已经被弃用了
        # options.add_experimental_option('disable-infobars')


    if headless:
        #无头模式--浏览器不展示出来，在后台静默运行;偶尔场景会有一场但很少。作用：减少电脑资源耗费
        options.add_argument('--headless')

    if useterminal:
        #去掉控制台多余信息--用于控制台中运行，在pycharm中直接run会报错，可以与上面去掉浏览器自动化提示配置 合并
        options.add_experimental_option('excludeSwitches', ['enable-automation','enable-logging'])
        # options.add_experimental_option('excludeSwitches',['enable-logging'])
        # 去掉控制台多余信息手段二，可以作为保险的存在。（当你发现还有多余信息的时候）
        options.add_argument('--log_level=3')
        options.add_argument('--disable-gpu')
        options.add_argument('--ignorecertificate-errors')

    if ysmode:
        #隐身模式
        options.add_argument('incognito')

    return options

if __name__ == '__main__':

    #创建driver对象
    driver= webdriver.Chrome(options=options())
    driver.get('https://www.baidu.com')
    # driver.find_element('id','kw').send_keys('水星')
    # driver.find_element('id','su').click()
    time.sleep(5)
    print(driver.title)


