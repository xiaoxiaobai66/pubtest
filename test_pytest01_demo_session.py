from time import sleep

import jsonpath
import pytest
import requests


class TestCase:
    cookhg=None
    cookhg2=None
    #创建session对象
    session1=requests.session()
    header=None
    other=None
    def test_login(self):
        url='https://litemall.hogwarts.ceshiren.com/admin/auth/login'
        json={'username':'hogwarts','password':'test12345'}
        rep=TestCase.session1.post(url,json=json)
        # rep=requests.post(url,json=json)
        print(type(rep.json()),rep.json())
        print(rep.headers)
        # TestCase.cookhg=rep.headers['Set-Cookie']
        #提取返回信息中的token值
        TestCase.cookhg2=jsonpath.jsonpath(rep.json(),'$..token')[0]
        # cookhg = jsonpath.jsonpath(rep.json(), '$..token')[0]
        cookhg = rep.headers['Set-Cookie']
        print(TestCase.cookhg2)
        #把这个token放在session的headers里面  给头部里面设置属性，用update
        TestCase.session1.headers.update({'cookie':cookhg})
        ass_key=jsonpath.jsonpath(rep.json(),'$..errmsg')[0]
        assert ass_key=='成功'




    def test_get_cityinfo(self):
        url='https://litemall.hogwarts.ceshiren.com/admin/region/list'
        #session 头部里面已经有了cookie
        # TestCase.header={'JSESSIONID':TestCase.cookhg2,'X-Litemall-Admin-Token':TestCase.cookhg2}
        # rep = requests.get(url, params=TestCase.header) #使用cookies=TestCase.header、headers=TestCase.header都可以
        rep=TestCase.session1.get(url)
        ass_key=rep.json()['errno']
        ass_ot=jsonpath.jsonpath(rep.json(),'$..list')[0]
        print(len(ass_ot))
        print(rep.headers)
        assert ass_key==0 and len(ass_ot)==31
    #
    def test_get_marketlist(self):
        url='https://litemall.hogwarts.ceshiren.com/admin/brand/list'
        #?page=1&limit=20&sort=add_time&order=desc
        data={'page':1,'limit':20,'sort':'add_time','order':'desc'}
        # rep = requests.get(url, cookies=TestCase.header,data=data)
        rep = TestCase.session1.get(url,data=data)
        print(rep.url)
        print(rep.headers)
        print(type(rep.json()),rep.json())
        ass_key = rep.json()['errno']
        ass_ot = jsonpath.jsonpath(rep.json(), '$..errmsg')[0]
        assert ass_key == 0 and ass_ot == '成功'

    def test_create_marketlist(self):
        url='https://litemall.hogwarts.ceshiren.com/admin/brand/create'
        data={"name":"测试二商","desc":"添加商品","floorPrice":"32","picUrl":"https://litemall.hogwarts.ceshiren.com/wx/storage/fetch/ue9vehya1y6h8a17brpk.jpg"}
        # rep=requests.post(url,json=data,cookies=TestCase.header)
        rep = TestCase.session1.post(url, json=data)
        ass_key = rep.json()['errno']
        ass_ot = jsonpath.jsonpath(rep.json(), '$..errmsg')[0]
        ass_ot2= jsonpath.jsonpath(rep.json(), '$..name')[0]
        # TestCase.other=jsonpath.jsonpath(rep.json(), '$..id')[0]
        TestCase.other = jsonpath.jsonpath(rep.json(), '$..data')[0] #接口关联：类变量方法
        create_info=jsonpath.jsonpath(rep.json(), '$..data')[0] #接口关联：return方法
        print(TestCase.other)
        assert ass_key == 0 and ass_ot == '成功' and ass_ot2=='测试二商'
        # return create_info #接口关联：return方法

    def test_update_marketlist(self):
        sleep(1)
        url='https://litemall.hogwarts.ceshiren.com/admin/brand/update'
        # data={"id": TestCase.other,"name":"测试二商","desc":"12355",
        #       "picUrl":"https://litemall.hogwarts.ceshiren.com/wx/storage/fetch/z0768g2bumgknikegm0c.jpg",
        #       "floorPrice":20,"addTime":"2024-08-10 17:39:37","updateTime":"2024-08-10 17:39:37",
        #       "preview":["https://litemall.hogwarts.ceshiren.com/wx/storage/fetch/ue9vehya1y6h8a17brpk.jpg"]}
        TestCase.other['desc']='商品描述修改'
        # rep = requests.post(url, json=TestCase.other, cookies=TestCase.header)  #接口关联：类变量方法
        # rep = requests.post(url, json=TestCase().test_create_marketlist(), cookies=TestCase.header) #接口关联：return方法
        rep = TestCase.session1.post(url, json=TestCase.other)  #接口关联：session方法
        print(TestCase.other, rep.json())
        ass_key = rep.json()['errno']
        ass_ot = jsonpath.jsonpath(rep.json(), '$..errmsg')[0]
        assert ass_key == 0 and ass_ot == '成功'


    def test_del_marketlist(self):
        sleep(1)
        url = 'https://litemall.hogwarts.ceshiren.com/admin/brand/delete'
        # rep = requests.post(url, json=TestCase.other, cookies=TestCase.header)  #接口关联：类变量方法
        # rep = requests.post(url, json=TestCase().test_create_marketlist(), cookies=TestCase.header)  #接口关联：return方法
        rep = TestCase.session1.post(url, json=TestCase.other)  # 接口关联：session方法
        print(rep.json())
        ass_key = rep.json()['errno']
        ass_ot = jsonpath.jsonpath(rep.json(), '$..errmsg')[0]
        assert ass_key == 0 and ass_ot == '成功'



if __name__ == '__main__':
    pytest.main(['-sv','test_pytest01_demo_session.py'])
