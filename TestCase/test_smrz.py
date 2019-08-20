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
global login_token
login_token = req.get_token(13911645993)


@allure.feature('sm', "查询认证信息")
@allure.severity('blocker')
def test_real_name_status_01():
    """
    查询认证信息(已开户已绑卡用户)
    :param login: 预制登录信息 获取授权token:
    :return:
    """
    global login_token
    login_token = req.get_token(13911645993)
    # login_token = 'BC-a62ce02bb89946e9b6638c3a0ab74ca7'

    with pytest.allure.step("查询认证信息"):
        response_dicts = req.api_request("real_name_status", token=login_token)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("real_name_status")['code'], response_dicts['code'])
        # test.assert_text(
        #     exp_results("real_name_status")['memberAuthComplete'],
        #     response_dicts['data']['memberAuthComplete'],
        #     "实名认证状态(true:完成 false:未完成)")
        # test.assert_text(
        #     exp_results("real_name_status")['idCardAuthComplete'],
        #     response_dicts['data']['idCardAuthComplete'],
        #     "身份证认证状态(true:完成 false:未完成)")
        # test.assert_text(
        #     exp_results("real_name_status")['userVerifyFlag'],
        #     response_dicts['data']['userVerifyFlag'], "用户是否通过短信校验(0：未通过 1：通过)")

    Consts.RESULT_LIST.append('True')


@allure.feature('sm', "查询认证信息_清除认证信息后")
@allure.severity('blocker')
def test_real_name_status_change_02():
    """
    查询认证信息_清除认证信息后(未开户未绑卡用户)
    :param login: 预制登录信息 获取授权token:
    :return:
    """
    with pytest.allure.step("清除认证信息"):
        mysql_opt.data_write("DELETE FROM a_id_card_auth WHERE ID_NAME = '许晨'",
                             'bicai_member_id_auth_test4_enc')
        mysql_opt.data_write(
            "DELETE FROM a_bank_card_auth WHERE ID_NAME = '许晨'",
            'bicai_member_id_auth_test4_enc')
        time.sleep(2)
    with pytest.allure.step("查询认证信息"):
        response_dicts = req.api_request("real_name_status_change",
                                         token=login_token)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("real_name_status_change")['code'],
            response_dicts['code'])
        test.assert_text(
            exp_results("real_name_status_change")['memberAuthComplete'],
            response_dicts['data']['memberAuthComplete'],
            "实名认证状态(true:完成 false:未完成)")
        test.assert_text(
            exp_results("real_name_status_change")['idCardAuthComplete'],
            response_dicts['data']['idCardAuthComplete'],
            "身份证认证状态(true:完成 false:未完成)")
        test.assert_text(
            exp_results("real_name_status_change")['userVerifyFlag'],
            response_dicts['data']['userVerifyFlag'], "用户是否通过短信校验(0：未通过 1：通过)")

    Consts.RESULT_LIST.append('True')


@allure.feature('sm', "身份证OCR(保存图片)")
@allure.severity('blocker')
def test_id_card_ocr_03():
    """
    身份证OCR(保存图片)
    :param login:
    :return:
    """

    with pytest.allure.step("身份证OCR(保存图片)"):
        response_dicts = req.api_request("id_card_ocr", token=login_token)
        global front_session_id  # 身份证人像面Sessionid
        global id_number  # 身份证号
        front_session_id = response_dicts['data']['frontSessionId']
        id_number = response_dicts['data']['idNumber']
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("id_card_ocr")['code'], response_dicts['code'])
        test.assert_text(
            exp_results("id_card_ocr")['idName'],
            response_dicts['data']['idName'], "姓名")
        test.assert_text(
            exp_results("id_card_ocr")['validityPeriod'],
            response_dicts['data']['validityPeriod'], "证件有效期")
        test.assert_text(
            exp_results("id_card_ocr")['validityPeriodExpired'],
            response_dicts['data']['validityPeriodExpired'],
            "证件是否过期(0证件未过期,1证件已过期)")
        test.assert_text(
            exp_results("id_card_ocr")['issuingAuthority'],
            response_dicts['data']['issuingAuthority'], "签发机关")
        test.assert_text(
            exp_results("id_card_ocr")['nation'],
            response_dicts['data']['nation'], "民族")
        test.assert_text(
            exp_results("id_card_ocr")['gender'],
            response_dicts['data']['gender'], "性别")
        test.assert_text(
            exp_results("id_card_ocr")['birthday'],
            response_dicts['data']['birthday'], "生日")
        test.assert_text(
            exp_results("id_card_ocr")['address'],
            response_dicts['data']['address'], "地址")
        Consts.RESULT_LIST.append('True')


@allure.feature('sm', "身份证,银行卡实名认证")
@allure.severity('blocker')
def test_real_name_verify_04():
    """
    身份证,银行卡实名认证
    :param login:
    :return:
    """
    with pytest.allure.step("身份证,银行卡实名认证"):
        response_dicts = req.api_request("real_name_verify",
                                         token=login_token,
                                         frontSessionId=front_session_id,
                                         idNumber=id_number)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("real_name_verify")['code'], response_dicts['code'])
    Consts.RESULT_LIST.append('True')


@allure.feature('sm', "查询认证信息未发短信验证码")
@allure.severity('blocker')
def test_real_name_status_no_message_05():
    """
    查询认证信息(已开户已绑卡用户未发送短信)
    :return:
    """

    with pytest.allure.step("查询认证信息(已开户已绑卡用户未发送短信)"):
        response_dicts = req.api_request("real_name_status_no_message",
                                         token=login_token)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("real_name_status_no_message")['code'],
            response_dicts['code'])
        test.assert_text(
            exp_results("real_name_status_no_message")['memberAuthComplete'],
            response_dicts['data']['memberAuthComplete'],
            "实名认证状态(true:完成 false:未完成)")
        test.assert_text(
            exp_results("real_name_status_no_message")['idCardAuthComplete'],
            response_dicts['data']['idCardAuthComplete'],
            "身份证认证状态(true:完成 false:未完成)")
        test.assert_text(
            exp_results("real_name_status_no_message")['userVerifyFlag'],
            response_dicts['data']['userVerifyFlag'], "用户是否通过短信校验(0：未通过 1：通过)")

    Consts.RESULT_LIST.append('True')


@allure.feature('sm', "短信验证码发送")
@allure.severity('blocker')
def test_get_phone_check_code_06():
    """
    短信验证码发送
    :return:
    """

    with pytest.allure.step("短信验证码发送"):
        response_dicts = req.api_request("get_phone_check_code",
                                         token=login_token)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("get_phone_check_code")['code'],
            response_dicts['code'])
    Consts.RESULT_LIST.append('True')
    time.sleep(2)


@allure.feature('sm', "短信验证码校验")
@allure.severity('blocker')
def test_verify_phone_check_code_07():
    """
    短信验证码校验
    :return:
    """

    with pytest.allure.step("短信验证码校验"):
        response_dicts = req.api_request("verify_phone_check_code",
                                         token=login_token)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("verify_phone_check_code")['code'],
            response_dicts['code'])
    Consts.RESULT_LIST.append('True')


@allure.feature('sm', "查询认证信息")
@allure.severity('blocker')
def test_real_name_status_end_08():
    """
    查询认证信息(已开户已绑卡用户)
    :param login: 预制登录信息 获取授权token:
    :return:
    """
    with pytest.allure.step("查询认证信息"):
        response_dicts = req.api_request("real_name_status", token=login_token)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("real_name_status")['code'], response_dicts['code'])
        test.assert_text(
            exp_results("real_name_status")['memberAuthComplete'],
            response_dicts['data']['memberAuthComplete'],
            "实名认证状态(true:完成 false:未完成)")
        test.assert_text(
            exp_results("real_name_status")['idCardAuthComplete'],
            response_dicts['data']['idCardAuthComplete'],
            "身份证认证状态(true:完成 false:未完成)")
        test.assert_text(
            exp_results("real_name_status")['userVerifyFlag'],
            response_dicts['data']['userVerifyFlag'], "用户是否通过短信校验(0：未通过 1：通过)")

    Consts.RESULT_LIST.append('True')
