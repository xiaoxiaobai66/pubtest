# 安装：pip install zmail

import zmail

def sendmail(file):
    # subject 标题
    # Content_text：邮件文本内容
    # Content_html:发送html格式内容
    # Attachments:附件

    # 发送人
    sender={'username':'yrjwrj@163.com','password':'13609612291show'}
    # 登录邮箱
    server=zmail.server(sender['username'],sender['password'])

    # 邮件内容
    mail_content={
        'subject':'我是标题',
        'Content_text':'测试报告',
        # 'Content_html':'<a href="http://www.baidu.com">嗨，你好</a>',
        'Attachments':f'{file}'  #../../unittestfile/report/report.html
    }

    # 收件人
    receive=['405798503@qq.com','yrjwrj@2980.com']
    # 发送邮件
    server.send_mail(receive,mail_content,cc=['yrjwrj@163.com'])

    # 注意：
    # Content_text和Content_html只能选择一个使用