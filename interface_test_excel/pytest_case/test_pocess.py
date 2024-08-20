import allure
import jsonpath
import openpyxl.compat
import pytest
import requests

from interface_test_excel.excel_deal.datadeal_excel import exceData
from interface_test_excel.interface_key_excel.httpclient_keyword import HttpClient


class TestCase:
    httpc = HttpClient()
    params1=None
    params2 = None


    # @pytest.mark.parametrize('num,url,date,method,param_type,expmsg',"exceData().getExcel('../data/test_account.xlsx')")
    @pytest.mark.parametrize('userdata',exceData().getExcel('./data/test_account_afterlogin.xlsx'))
    def test_login(self,userdata):
        #以用例中的模块作为测试报告的模块名
        if userdata[9] is not None:
            allure.dynamic.feature(userdata[9])
        if userdata[10] is not None:
            allure.dynamic.story(userdata[10])
        if userdata[11] is not None:
            allure.dynamic.title(userdata[11])
        if userdata[12] is not None:
            allure.dynamic.description(userdata[12])
        if userdata[13] is not None:
            allure.dynamic.severity(userdata[13])

        id=userdata[0]
        #接口关联：参数提取
        url=userdata[1]
        if userdata[2] is not None:
            data=eval(userdata[2])  #将字符串转化为字典
        elif userdata[4] is not None:
            data=eval(userdata[4])
            data=data['name']
            if data=='TestCase.params1':
                data=TestCase.params1
            elif data=='TestCase.params2':
                data = TestCase.params2
        else:
            data =None

        method=userdata[5]
        param_type=userdata[6]
        expected= eval(userdata[7])
        # print(userdata[1], type(eval(userdata[2])), userdata[2], userdata[3], userdata[4], userdata[5])
        req=TestCase.httpc(url=url,method=method,params_type=param_type,data=data)
        print(req.json())
        # 接口关联：参数保存
        if userdata[3] is not None:
            savep=eval(userdata[3])
            if savep['name']=='TestCase.params1':
                TestCase.params1=jsonpath.jsonpath(req.json(),f"{savep['object']}")[0]
            elif savep['name']=='TestCase.params2':
                TestCase.params2 = jsonpath.jsonpath(req.json(), f"{savep['object']}")[0]

        real_errmsg=jsonpath.jsonpath(req.json(),'$..errmsg')[0]
        real_errno=jsonpath.jsonpath(req.json(),'$..errno')[0]
        try:
            assert expected['errmsg']==real_errmsg and expected['errno']==real_errno
            result='通过'
        except Exception as e:
            result = '失败'
        workbook=openpyxl.load_workbook('./data/test_account_afterlogin.xlsx')
        sheet1=workbook['login']
        #将结果写入对应位置
        sheet1.cell(id+1,9).value=result
        workbook.save('./data/test_account_afterlogin.xlsx')





if __name__ == '__main__':
    pytest.main(['-sv','./test_pocess.py'])

