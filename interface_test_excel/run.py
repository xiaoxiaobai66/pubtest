import os

import pytest

if __name__ == '__main__':
    pytest.main(['-sv','./pytest_case/','--alluredir', './report/life'])
    os.system('allure generate --clean ./report/life -o ./report/report')
