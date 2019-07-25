# -*- coding: utf-8 -*-
# @Time    : 2019/7/15 1:22 PM
# @Author  : XuChen
# @File    : conftest.py
import time
import pytest

from Common import Consts, request_module
from Common import mysql_module

mysql_opt = mysql_module.MySqlModule()
req = request_module.RequestModule()


@pytest.fixture(scope="function", autouse=True)
def func_header(request):
    """
    统计运行case数
    :param request:
    :return:
    """
    Consts.TEST_LIST.append('Test')
    print('\n-----------------')
    print('function    : %s' % request.function.__name__)
    print('time        : %s' % time.asctime())
    print('-----------------')
