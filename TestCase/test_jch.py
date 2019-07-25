# -*- coding: utf-8 -*-
# @Time    : 2019/7/15 9:37 AM
# @Author  : XuChen
# @File    : test_jch.py

from __future__ import absolute_import

import random
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


@allure.feature('jch', "用户开户状态查询（温旭雲）")
@allure.severity('blocker')
def test_query_login_status_01():
    """
    用户开户状态查询
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


@allure.feature('jch', "资产首页--(郝志阳)")
@allure.severity('blocker')
def test_api_query_bank_center_02():
    """
    资产首页余额查询
    :return: 
    """
    with pytest.allure.step("资产首页--(郝志阳)"):
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


@allure.feature('jch', "交易通用校验(黄新)-充值")
@allure.severity('blocker')
def test_api_trade_check_cz_03():
    """
    交易通用校验-(黄新),10-充值
    :return: 
    """
    with pytest.allure.step("交易通用校验-(黄新),10-充值"):
        response_dicts = req.api_request("api_trade_check",
                                         token=login_token,
                                         tradeType=10)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("api_trade_check")['code'], response_dicts['code'])
    Consts.RESULT_LIST.append('True')


@allure.feature('jch', "机构绑卡列表查询")
@allure.severity('blocker')
def test_api_query_org_bind_card_cz_04():
    """
    机构绑卡列表查询
    :return: 
    """
    global bankName
    global bankCardNum
    with pytest.allure.step("机构绑卡列表查询"):
        response_dicts = req.api_request("api_query_org_bind_card",
                                         token=login_token)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("api_trade_check")['code'], response_dicts['code'])
        bankName = response_dicts['data']['cardList'][0]['bankName']
        bankCardNum = response_dicts['data']['cardList'][0]['bankCardNum']
    Consts.RESULT_LIST.append('True')


@allure.feature('jch', "充值(黄新)")
@allure.severity('blocker')
def test_api_recharge_05():
    """
    充值(黄新)
    :return: 
    """
    with pytest.allure.step("充值(黄新)"):
        global cz_amount
        cz_amount = "2000.00"
        response_dicts = req.api_request("api_recharge",
                                         token=login_token,
                                         bankCardNum=bankCardNum,
                                         bankName=bankName,
                                         amount=cz_amount)
        global reqSerial, apiPackSeq, amount, validateCodeSerialNum

        reqSerial = response_dicts['data']['reqSerial']  # 充值交易流水号

        apiPackSeq = response_dicts['data']['apiPackSeq']  # 比财报文参考号

        amount = response_dicts['data']['amount']  # 金额

        validateCodeSerialNum = response_dicts['data'][
            'validateCodeSerialNum']  # 短信验证码ID

        print(reqSerial, apiPackSeq, amount, validateCodeSerialNum)

    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("api_recharge")['code'], response_dicts['code'])
    Consts.RESULT_LIST.append('True')


@allure.feature('jch', "充值确认(黄新)")
@allure.severity('blocker')
def test_api_recharge_confirm_06():
    """
    充值确认(黄新)
    :return: 
    """
    with pytest.allure.step("充值确认(黄新)"):
        response_dicts = req.api_request(
            "api_recharge_confirm",
            token=login_token,
            reqSerial=reqSerial,
            validateCode=str(random.randint(111111, 999999)),
            validateCodeSerialNum=validateCodeSerialNum)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("api_recharge_confirm")['code'],
            response_dicts['code'])
        test.assert_text(cz_amount, response_dicts['data']['amount'], "充值金额")
    Consts.RESULT_LIST.append('True')


@allure.feature('jch', "充值后查询余额")
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


@allure.feature('jch', "购买(黄新)")
@allure.severity('blocker')
def test_api_buy_08():
    """
    购买(黄新)
    :return: 
    """
    global amount_buy  # 购买金额
    amount_buy = "1001.00"
    with pytest.allure.step("购买(黄新)"):
        response_dicts = req.api_request("api_buy",
                                         token=login_token,
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


@allure.feature('jch', "存入后查询余额")
@allure.severity('blocker')
def test_api_query_bank_center_cr_09():
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


@allure.feature('jch', "持有列表--(郝志阳)")
@allure.severity('blocker')
def test_api_query_hold_info_10():
    """
    持有列表--(郝志阳)
    :return: 
    """
    with pytest.allure.step("持有列表--(郝志阳)"):
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


@allure.feature('jch', "赎回利息试算(黄新)")
@allure.severity('blocker')
def test_interest_calculatioin_11():
    """
    赎回利息试算(黄新)
    :return: 
    """
    with pytest.allure.step("赎回利息试算(黄新)"):
        response_dicts = req.api_request("interest_calculatioin",
                                         token=login_token,
                                         amount=amount_buy,
                                         reqSerial=reqSerial_cr)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("interest_calculatioin")['code'],
            response_dicts['code'])
    Consts.RESULT_LIST.append('True')


@allure.feature('jch', "赎回(黄新)")
@allure.severity('blocker')
def test_api_redemption_12():
    """
    赎回(黄新)
    :return: 
    """
    with pytest.allure.step("赎回(黄新)"):
        response_dicts = req.api_request("api_redemption",
                                         token=login_token,
                                         amount=amount_buy,
                                         reqSerial=reqSerial_cr)
    with pytest.allure.step("结果对比"):
        test.assert_code(
            exp_results("api_redemption")['code'], response_dicts['code'])
        test.assert_text(response_dicts['data']['amount'], amount_buy,
                         "持有列表中包含该笔交易记录")
    Consts.RESULT_LIST.append('True')


@allure.feature('jch', "持有列表-赎回后--(郝志阳)")
@allure.severity('blocker')
def test_api_query_hold_info_sh_13():
    """
    持有列表-赎回后--(郝志阳)
    :return: 
    """
    time.sleep(2)
    with pytest.allure.step("持有列表--(郝志阳)"):
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


@allure.feature('jch', "支取后查询余额")
@allure.severity('blocker')
def test_api_query_bank_center_zq_14():
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


@allure.feature('jch', "提现(黄新)")
@allure.severity('blocker')
def test_api_cash_15():
    """
    提现(黄新)
    :return: 
    """
    with pytest.allure.step("提现(黄新)"):
        global tx_amount
        tx_amount = "2000.00"
        response_dicts = req.api_request("api_cash",
                                         token=login_token,
                                         bankCardNum=bankCardNum,
                                         bankName=bankName,
                                         amount=tx_amount)
        with pytest.allure.step("结果对比"):
            test.assert_code(
                exp_results("api_cash")['code'], response_dicts['code'])
            test.assert_text(response_dicts['data']['amount'], tx_amount,
                             "提现金额")
        Consts.RESULT_LIST.append('True')


@allure.feature('jch', "提现后查询余额")
@allure.severity('blocker')
def test_api_query_bank_center_tx_16():
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
