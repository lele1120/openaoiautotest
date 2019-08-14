# -*- coding: utf-8 -*-
# @Time    : 2019/7/15 9:37 AM
# @Author  : XuChen
# @File    : test_smrz.py

from __future__ import absolute_import
from decimal import *
import json
import operator
import sys
import time
from os import path

import allure
import pytest
import requests

from Common import assert_module, Consts
from Common import request_module, mysql_module
from Params.Params import exp_results

test = assert_module.AssertModule()
req = request_module.RequestModule()

mysql_opt = mysql_module.MySqlModule()
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
Consts.MYSQL_ENVIRONMENT = 'bicai_member_id_auth_test4_enc'


@allure.feature('sm', "查询认证信息")
@allure.severity('blocker')
def test_real_name_status_01():
    """
    用户开户状态查询
    :param login: 预制登录信息 获取授权token:
    :return:
    """
    global login_token
    login_token = req.get_token(13911645993)
    # login_token = 'BC-a62ce02bb89946e9b6638c3a0ab74ca7'

    with pytest.allure.step("查询认证信息"):
        response_dicts = req.api_request("real_name_status",
                                         token=login_token)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("real_name_status")['code'], response_dicts['code'])
        # test.assert_text(
        #     exp_results("real_name_status")['code'],
        #     response_dicts['data']['hasLogin'], "是否需要登录银行 0：不需要登录 1：已登录 2：未登陆")

    Consts.RESULT_LIST.append('True')



