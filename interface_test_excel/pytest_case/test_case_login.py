import sys

import allure
import jsonpath
import openpyxl.compat
import pytest
import requests

sys.path.append('D:\pyf\LFd1')
from interface_test_excel.excel_deal.datadeal_excel import exceData
from interface_test_excel.interface_key_excel.httpclient_keyword import HttpClient


class TestCase:
    httpc = HttpClient()

    # @pytest.mark.parametrize('num,url,date,method,param_type,expmsg',"exceData().getExcel('../data/test_account.xlsx')")
    @pytest.mark.parametrize('userdata',exceData().getExcel('./data/test_account.xlsx'))
    def test_alone(self,userdata):
        #以用例中的模块作为测试报告的模块名
        if userdata[7] is not None:
            allure.dynamic.feature(userdata[7])
        if userdata[8] is not None:
            allure.dynamic.story(userdata[8])
        if userdata[9] is not None:
            allure.dynamic.title(userdata[7])
        if userdata[10] is not None:
            allure.dynamic.description(userdata[10])
        if userdata[11] is not None:
            allure.dynamic.severity(userdata[11])

        id=userdata[0]
        print(userdata[1],type(eval(userdata[2])),userdata[2],userdata[3],userdata[4],userdata[5])
        url=userdata[1]
        data=eval(userdata[2])  #将字符串转化为字典
        method=userdata[3]
        param_type=userdata[4]
        expected= eval(userdata[5])
        req=TestCase.httpc(url=url,method=method,params_type=param_type,data=data)
        print(req.json())
        real_errmsg=jsonpath.jsonpath(req.json(),'$..errmsg')[0]
        real_errno=jsonpath.jsonpath(req.json(),'$..errno')[0]
        try:
            assert expected['errmsg']==real_errmsg and expected['errno']==real_errno
            result='通过'
        except Exception as e:
            result = '失败'
        workbook=openpyxl.load_workbook('./data/test_account.xlsx')
        sheet1=workbook['login']
        #将结果写入对应位置
        sheet1.cell(id+1,7).value=result
        workbook.save('./data/test_account.xlsx')


if __name__ == '__main__':
    pytest.main(['-sv','./test_case_login.py'])

