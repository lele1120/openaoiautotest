# -*- coding: utf-8 -*-
# @Time    : 2019/7/15 9:37 AM
# @Author  : XuChen
# @File    : test_bhns.py

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
Consts.MYSQL_ENVIRONMENT = 'bicai_admin'


@allure.feature('bhns', "登录状态查询接口-liming")
@allure.severity('blocker')
def test_query_login_status_01():
    """
    用户开户状态查询接口-liming
    :param login: 预制登录信息 获取授权token:
    :return:
    """
    global login_token
    login_token = req.get_token(13911645993)
    # login_token = 'BC-a62ce02bb89946e9b6638c3a0ab74ca7'

    with pytest.allure.step("用户开户状态查询"):
        response_dicts = req.api_request("query_login_status",
                                         token=login_token)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("query_login_status")['code'], response_dicts['code'])
        test.assert_text(
            exp_results("query_login_status")['hasLogin'],
            response_dicts['data']['hasLogin'], "是否需要登录银行 0：不需要登录 1：已登录 2：未登陆")
        test.assert_text(
            exp_results("query_login_status")['hasOpenBank'],
            response_dicts['data']['hasOpenBank'], "是否已开户")
    Consts.RESULT_LIST.append('True')


@allure.feature('bhns', "查询资产首页总数据（qxx）")
@allure.severity('blocker')
def test_api_query_bank_center_02():
    """
    查询资产首页总数据（qxx）
    :return: 
    """
    with pytest.allure.step("查询资产首页总数据（qxx）"):
        response_dicts = req.api_request("api_query_bank_center",
                                         token=login_token)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("api_query_bank_center")['code'],
            response_dicts['code'])

    global totalAsset  # 总资产
    global balance  # 可用余额
    global hold_amount  # 持有求和
    totalAsset = response_dicts['data']['totalAsset']
    balance = response_dicts['data']['balance']
    hold_amount = 0
    for i in range((response_dicts['data']['prodList']).__len__()):
        print(response_dicts['data']['prodList'][i]['prdTypeName'] + "持有金额:" +
              response_dicts['data']['prodList'][i]['holdAmount'])
        hold_amount = Decimal(
            response_dicts['data']['prodList'][i]['holdAmount']) + hold_amount
    print("总资产:" + str(totalAsset))
    print("可用余额:" + str(balance))
    print("持有金额求和:" + str(hold_amount))
    test.assert_text(hold_amount + Decimal(balance), Decimal(totalAsset),
                     "持有产品汇总")
    Consts.RESULT_LIST.append('True')


@allure.feature('bhns', "交易通用校验（qxx）,tradeType=10")
@allure.severity('blocker')
def test_api_trade_check_cz_03():
    """
    交易通用校验（qxx）,tradeType=10
    :return: 
    """
    with pytest.allure.step("交易通用校验（qxx）,tradeType=10"):
        response_dicts = req.api_request("api_trade_check",
                                         token=login_token,
                                         tradeType=10)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("api_trade_check")['code'], response_dicts['code'])
    Consts.RESULT_LIST.append('True')


@allure.feature('bhns', "查询机构绑卡信息-qxx")
@allure.severity('blocker')
def test_api_query_org_bind_card_cz_04():
    """
    查询机构绑卡信息-qxx
    :return: 
    """
    global bankName
    global bankCardNum
    with pytest.allure.step("查询机构绑卡信息-qxx"):
        response_dicts = req.api_request("api_query_org_bind_card",
                                         token=login_token)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("api_trade_check")['code'], response_dicts['code'])
        bankName = response_dicts['data']['cardList'][0]['bankName']
        bankCardNum = response_dicts['data']['cardList'][0]['bankCardNum']
    Consts.RESULT_LIST.append('True')


@allure.feature('bhns', "充值短信验证码-liming")
@allure.severity('blocker')
def test_api_send_phoneCode_cz_05():
    """
    充值短信验证码-liming
    :return:
    """
    with pytest.allure.step("短信验证码-liming"):
        response_dicts = req.api_request(
            "api_send_phoneCode", token=login_token)
    with pytest.allure.step("结果对比"):
        global apiPackSeq,validateCodeSerialNum
        apiPackSeq = response_dicts['data']['apiPackSeq']  # openapi流水号

        validateCodeSerialNum = response_dicts['data']['validateCodeSerialNum']  # 短信验证码编号

        test.assert_code(
            exp_results("api_send_phoneCode")['code'],
            response_dicts['code'])

    Consts.RESULT_LIST.append('True')


@allure.feature('bhns', "充值（qxx）")
@allure.severity('blocker')
def test_api_recharge_06():
    """
    充值（qxx）
    :return: 
    """
    with pytest.allure.step("充值（qxx）"):
        global cz_amount, amount
        cz_amount = "2000.00"
        response_dicts = req.api_request("api_recharge",
                                         token=login_token,
                                         bankCardNum=bankCardNum,
                                         bankName=bankName,
                                         amount=cz_amount,
                                         bizType=3,
                                         validateCodeSerialNum=validateCodeSerialNum)

    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("api_recharge")['code'], response_dicts['code'])
    Consts.RESULT_LIST.append('True')


@allure.feature('bhns', "充值后查询余额")
@allure.severity('blocker')
def test_api_query_bank_center_cz_07():
    """
    充值后查询余额
    :return: 
    """
    time.sleep(2)
    with pytest.allure.step("充值后查询余额"):
        response_dicts = req.api_request("api_query_bank_center",
                                         token=login_token)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("api_query_bank_center")['code'],
            response_dicts['code'])

    global totalAsset_cz  # 总资产
    global balance_cz  # 可用余额
    global hold_amount_cz  # 持有求和
    totalAsset_cz = response_dicts['data']['totalAsset']
    balance_cz = response_dicts['data']['balance']
    hold_amount_cz = 0
    for i in range((response_dicts['data']['prodList']).__len__()):
        print(response_dicts['data']['prodList'][i]['prdTypeName'] + "持有金额:" +
              response_dicts['data']['prodList'][i]['holdAmount'])
        hold_amount_cz = Decimal(response_dicts['data']['prodList'][i]
                                 ['holdAmount']) + hold_amount_cz
    print("总资产:" + str(totalAsset_cz))
    print("可用余额:" + str(balance_cz))
    print("持有金额求和:" + str(hold_amount_cz))
    test.assert_text(Decimal(balance_cz),
                     Decimal(balance) + Decimal(cz_amount), "充值后余额")
    test.assert_text(Decimal(totalAsset_cz),
                     Decimal(totalAsset) + Decimal(cz_amount), "充值后总资产")
    test.assert_text(hold_amount_cz, hold_amount, "充值后持有")
    Consts.RESULT_LIST.append('True')


@allure.feature('bhns', "存入短信验证码-liming")
@allure.severity('blocker')
def test_api_send_phoneCode_cr_08():
    """
    存入短信验证码-liming
    :return:
    """
    with pytest.allure.step("存入短信验证码-liming"):
        response_dicts = req.api_request(
            "api_send_phoneCode", token=login_token, bizType=6)
    with pytest.allure.step("结果对比"):
        global validateCodeSerialNum_cr
        validateCodeSerialNum_cr = response_dicts['data']['validateCodeSerialNum']  # 存入短信验证码编号

        test.assert_code(
            exp_results("api_send_phoneCode")['code'],
            response_dicts['code'])

    Consts.RESULT_LIST.append('True')


@allure.feature('bhns', "购买（qxx）")
@allure.severity('blocker')
def test_api_buy_09():
    """
    购买（qxx）
    :return: 
    """
    global amount_buy  # 购买金额
    amount_buy = "1001.00"
    with pytest.allure.step("购买（qxx）"):
        response_dicts = req.api_request("api_buy",
                                         token=login_token,
                                         validateCodeSerialNum=validateCodeSerialNum_cr,
                                         amount=amount_buy)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("api_buy")['code'], response_dicts['code'])
        test.assert_text(Decimal(amount_buy),
                         Decimal(response_dicts['data']['amount']), "存入金额")
        global reqSerial_cr  # 交易流水号
        global apiPackSeq_cr  # 请求流水号
        reqSerial_cr = response_dicts['data']['reqSerial']
        apiPackSeq_cr = response_dicts['data']['apiPackSeq']
    Consts.RESULT_LIST.append('True')


@allure.feature('bhns', "存入后查询余额")
@allure.severity('blocker')
def test_api_query_bank_center_cr_10():
    """
    存入后查询余额
    :return: 
    """
    time.sleep(2)
    with pytest.allure.step("存入后查询余额"):
        response_dicts = req.api_request("api_query_bank_center",
                                         token=login_token)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("api_query_bank_center")['code'],
            response_dicts['code'])

    global totalAsset_cr  # 总资产
    global balance_cr  # 可用余额
    global hold_amount_cr  # 持有求和

    totalAsset_cr = response_dicts['data']['totalAsset']
    balance_cr = response_dicts['data']['balance']
    hold_amount_cr = 0
    for i in range((response_dicts['data']['prodList']).__len__()):
        print(response_dicts['data']['prodList'][i]['prdTypeName'] + "持有金额:" +
              response_dicts['data']['prodList'][i]['holdAmount'])
        hold_amount_cr = Decimal(response_dicts['data']['prodList'][i]
                                 ['holdAmount']) + Decimal(hold_amount_cr)
    print("总资产:" + str(totalAsset_cr))
    print("可用余额:" + str(balance_cr))
    print("持有金额求和:" + str(hold_amount_cr))
    test.assert_text(Decimal(balance_cr),
                     Decimal(balance_cz) - Decimal(amount_buy), "存入后余额")
    test.assert_text(Decimal(totalAsset_cz), Decimal(totalAsset_cr), "存入后总资产")
    test.assert_text(Decimal(hold_amount_cr),
                     Decimal(hold_amount_cz) + Decimal(amount_buy), "存入后持有")
    Consts.RESULT_LIST.append('True')


@allure.feature('bhns', "存入后查用户持有（qxx）")
@allure.severity('blocker')
def test_api_query_hold_info_11():
    """
    存入后查用户持有（qxx）
    :return: 
    """
    with pytest.allure.step("存入后查用户持有（qxx）"):
        response_dicts = req.api_request("api_query_hold_info",
                                         token=login_token)
    ret_list = {}
    # for i in range(response_dicts['data']['retList'].__len__()):
    #     ret_list[response_dicts['data']['retList'][i]
    #              ['reqSerial']] = response_dicts['data']['retList'][i][
    #                  'dynamicList']['amount']['fieldValue']
    ret_list[response_dicts['data']['retList'][0]
             ['reqSerial']] = response_dicts['data']['retList'][0][
                 'dynamicList']['amount']['fieldValue']
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("api_query_bank_center")['code'],
            response_dicts['code'])
        test.assert_text(Decimal(ret_list[reqSerial_cr].replace(',', '')),
                         Decimal(amount_buy), "持有列表中包含该笔交易记录")

    Consts.RESULT_LIST.append('True')


@allure.feature('bhns', "支取短信验证码-liming")
@allure.severity('blocker')
def test_api_send_phoneCode_zq_12():
    """
    支取短信验证码-liming
    :return:
    """
    with pytest.allure.step("支取短信验证码-liming"):
        response_dicts = req.api_request(
            "api_send_phoneCode", token=login_token, bizType=7, amount=amount_buy)
    with pytest.allure.step("结果对比"):
        global validateCodeSerialNum_zq
        validateCodeSerialNum_zq = response_dicts['data']['validateCodeSerialNum']  # 支取短信验证码编号

        test.assert_code(
            exp_results("api_send_phoneCode")['code'],
            response_dicts['code'])

    Consts.RESULT_LIST.append('True')


@allure.feature('bhns', "赎回（qxx）")
@allure.severity('blocker')
def test_api_redemption_13():
    """
    赎回（qxx）
    :return: 
    """
    with pytest.allure.step("赎回（qxx）"):
        response_dicts = req.api_request("api_redemption",
                                         token=login_token,
                                         amount=amount_buy,
                                         reqSerial=reqSerial_cr,
                                         validateCodeSerialNum=validateCodeSerialNum_zq)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("api_redemption")['code'], response_dicts['code'])
        test.assert_text(response_dicts['data']['amount'], amount_buy,
                         "持有列表中包含该笔交易记录")
    Consts.RESULT_LIST.append('True')


@allure.feature('bhns', "支取后查用户持有（qxx）")
@allure.severity('blocker')
def test_api_query_hold_info_sh_14():
    """
    支取后查用户持有（qxx）
    :return: 
    """
    time.sleep(2)
    with pytest.allure.step("赎回后查用户持有（qxx）"):
        response_dicts = req.api_request("api_query_hold_info",
                                         token=login_token)
    # ret_list = []
    # for i in range(response_dicts['data']['retList'].__len__()):
    #     ret_list.append(response_dicts['data']['retList'][i]['dynamicList']
    #                     ['reqSerial']['fieldValue'])

    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("api_query_bank_center")['code'],
            response_dicts['code'])
        # assert reqSerial_cr not in ret_list
        test.assert_text(
            Decimal(hold_amount_cr) - Decimal(amount_buy),
            Decimal(response_dicts['data']['totalHoldAmount']), "存入后持有")

    Consts.RESULT_LIST.append('True')


@allure.feature('bhns', "支取后查询余额")
@allure.severity('blocker')
def test_api_query_bank_center_zq_15():
    """
    支取后查询余额
    :return: 
    """
    time.sleep(2)
    with pytest.allure.step("支取后查询余额"):
        response_dicts = req.api_request("api_query_bank_center",
                                         token=login_token)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("api_query_bank_center")['code'],
            response_dicts['code'])

    global totalAsset_zq  # 总资产
    global balance_zq  # 可用余额
    global hold_amount_zq  # 持有求和

    totalAsset_zq = response_dicts['data']['totalAsset']
    balance_zq = response_dicts['data']['balance']
    hold_amount_zq = 0
    for i in range((response_dicts['data']['prodList']).__len__()):
        print(response_dicts['data']['prodList'][i]['prdTypeName'] + "持有金额:" +
              response_dicts['data']['prodList'][i]['holdAmount'])
        hold_amount_zq = Decimal(response_dicts['data']['prodList'][i]
                                 ['holdAmount']) + Decimal(hold_amount_zq)
    print("总资产:" + str(totalAsset_zq))
    print("可用余额:" + str(balance_zq))
    print("持有金额求和:" + str(hold_amount_zq))
    test.assert_text(Decimal(balance_zq),
                     Decimal(balance_cr) + Decimal(amount_buy), "支取后余额")
    test.assert_text(Decimal(totalAsset_cr), Decimal(totalAsset_zq), "支取后总资产")
    test.assert_text(Decimal(hold_amount_zq),
                     Decimal(hold_amount_cr) - Decimal(amount_buy), "支取后持有")
    Consts.RESULT_LIST.append('True')

@allure.feature('bhns', "提现短信验证码-liming")
@allure.severity('blocker')
def test_api_send_phoneCode_tx_16():
    """
    提现短信验证码-liming
    :return:
    """
    with pytest.allure.step("提现短信验证码-liming"):
        response_dicts = req.api_request(
            "api_send_phoneCode", token=login_token, bizType=4, amount=cz_amount)
    with pytest.allure.step("结果对比"):
        global validateCodeSerialNum_tx
        validateCodeSerialNum_tx = response_dicts['data']['validateCodeSerialNum']  # 提现短信验证码编号

        test.assert_code(
            exp_results("api_send_phoneCode")['code'],
            response_dicts['code'])

    Consts.RESULT_LIST.append('True')


@allure.feature('bhns', "提现 (qxx)")
@allure.severity('blocker')
def test_api_cash_17():
    """
    提现 (qxx)
    :return: 
    """
    with pytest.allure.step("提现 (qxx)"):
        global tx_amount
        tx_amount = "2000.00"
        response_dicts = req.api_request("api_cash",
                                         token=login_token,
                                         bankCardNum=bankCardNum,
                                         bankName=bankName,
                                         validateCodeSerialNum=validateCodeSerialNum_tx,
                                         amount=tx_amount)
        with pytest.allure.step("结果对比"):
            test.assert_code(
                exp_results("api_cash")['code'], response_dicts['code'])
            test.assert_text(response_dicts['data']['amount'], tx_amount,
                             "提现金额")
    Consts.RESULT_LIST.append('True')


@allure.feature('bhns', "提现后查询余额")
@allure.severity('blocker')
def test_api_query_bank_center_tx_18():
    """
    提现后查询余额
    :return: 
    """
    time.sleep(2)
    with pytest.allure.step("提现后查询余额"):
        response_dicts = req.api_request("api_query_bank_center",
                                         token=login_token)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("api_query_bank_center")['code'],
            response_dicts['code'])

    global totalAsset_tx  # 总资产
    global balance_tx  # 可用余额
    global hold_amount_tx  # 持有求和

    totalAsset_tx = response_dicts['data']['totalAsset']
    balance_tx = response_dicts['data']['balance']
    hold_amount_tx = 0
    for i in range((response_dicts['data']['prodList']).__len__()):
        print(response_dicts['data']['prodList'][i]['prdTypeName'] + "持有金额:" +
              response_dicts['data']['prodList'][i]['holdAmount'])
        hold_amount_tx = Decimal(response_dicts['data']['prodList'][i]
                                 ['holdAmount']) + Decimal(hold_amount_tx)
    print("总资产:" + str(totalAsset_tx))
    print("可用余额:" + str(balance_tx))
    print("持有金额求和:" + str(hold_amount_tx))
    test.assert_text(Decimal(balance_tx),
                     Decimal(balance_zq) - Decimal(tx_amount), "提现后余额")
    test.assert_text(Decimal(totalAsset_tx),
                     Decimal(totalAsset_zq) - Decimal(tx_amount), "提现后总资产")
    test.assert_text(Decimal(hold_amount_zq), Decimal(hold_amount_tx), "提现后持有")
    Consts.RESULT_LIST.append('True')
