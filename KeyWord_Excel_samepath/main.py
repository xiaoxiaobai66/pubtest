import os
import pathlib

from excel_data_deal import excel_read

if __name__ == '__main__':
    #通过读取’数据驱动‘文件夹下是否有测试用例，有则执行；没有后就不执行
    #测试用例集合
    cases=list()
    #读取路径下的测试用例 ../数据驱动/   D:\pyf\LFd1\web_automation\数据驱动
    for path,dir,files in os.walk('./excel_data/'): #此方法可以返回 1文件路径 2路径下的文件夹 3路径下的文件
        for file in files:
            #获取文件的后缀名
            # file_type =file.split('.')
            file_type = os.path.splitext(file)[1]
            # print(file_type)
            if file_type =='.xlsx':
                failcount=excel_read(path+file)  #文件路径+文件名 运行了excel_read()后，会返回失败结果
                #failcount为失败用例字典集，key为文件路径+文件名，value是sheet页
                if failcount == {}:
                    pass
                else:
                    #遍历需要重跑的文件名、sheet页
                    for refile, resheet in failcount.items():
                        excel_read(refile, replay=True, replay_case=resheet)
            else:
                print(f'{file}非excel文件，无法执行')


