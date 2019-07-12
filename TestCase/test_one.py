# -*- coding: utf-8 -*-
# @Time    : 2019/7/12 2:54 PM
# @Author  : XuChen
# @File    : test_one.py

from __future__ import absolute_import

import operator
import sys
import time
from os import path

import pytest

from Common import assert_module, Consts
from Common import request_module, mysql_module
from Params.Params import exp_results

test = assert_module.AssertModule()
req = request_module.RequestModule()
mysql_opt = mysql_module.MySqlModule()
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
Consts.MYSQL_ENVIRONMENT = 'bicai_admin'


@pytest.allure.feature('Admin_User', "获取用户权限列表")
@pytest.allure.severity('blocker')
def test_get_admin_user_info_01():
    """
    获取用户权限列表
    :param login: 预制登录信息 获取授权authorization:
    :return:
    """
    with pytest.allure.step("取用户权限列表"):
        response_dicts = req.start_request("get_admin_user_info")
    with pytest.allure.step("断言success对比"):
        test.assert_text(
            exp_results('get_admin_user_info')['success'],
            response_dicts['success'])
    Consts.RESULT_LIST.append('True')
