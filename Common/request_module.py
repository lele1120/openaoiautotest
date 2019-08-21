# -*- coding: utf-8 -*-
# @Time    : 2019/7/12 2:55 PM
# @Author  : XuChen
# @File    : request_module.py
"""
封装request

"""
import json
import os
import random

import pytest
import requests
import Common.Consts
from Common import env_module, Consts
# from requests_toolbelt import MultipartEncoder

from Params.Params import get_value
import allure


class RequestModule:
    def __init__(self):
        """
        :param env:环境遍历：测试环境debug，生产环境release
        """
        self.get_environment = env_module.EnvModule()
        self.get_evn_url = self.get_environment.get_env_url()
        self.data = ''
        self.url = ''

    def get_url(self):
        path = self.get_evn_url
        login_url = ''
        if path[22:27] == 'test1':
            login_url = 'https://app-test1.bicai365.com'  # ytest 环境
            pytest.allure.environment(environment='test1')
        elif path[22:27] == 'test2':
            login_url = 'https://app-test2.bicai365.com'  # adv
            pytest.allure.environment(environment='test2')
        elif path[22:27] == 'test3':
            login_url = 'https://app-test3.bicai365.com'  # adv1
            pytest.allure.environment(environment='test3')
        elif path[22:27] == 'test4':
            login_url = 'https://app-test4.bicai365.com'  # adv2
            pytest.allure.environment(environment='test4')
        elif path[22:27] == 'test5':
            login_url = 'https://app-test5.bicai365.com'  # adv3
            pytest.allure.environment(environment='test5')
        return login_url

    def get_token(self, phone_number):

        # url = 'https://app-test4.bicai365.com'
        url = self.get_url()
        get_v_value = {
            "head": {
                "TYPE": "REQ_NO_VALIDATE",
                "TOKEN": "",
                "SESSION_ID": "D1C72196996528253F5846F3A0E586A2",
                "DEVICE_ID": "H5",
                "CHANNEL": "",
                "SCREEN_SIZE": "",
                "SYSTEM_TYPE": "h5",
                "CHANNEL_ID": "9",
                "APP_FLAG": "BC",
                "USER_CHANNEL": ""
            },
            "param": {
                "PHONE_NUM": str(phone_number),
                "SAFT_CODE": "1234"
            }
        }
        requests.post(url=url + '/finsuit/finsuitPhone/deal',
                      data={"param_key": json.dumps(get_v_value)})
        login_value = {
            "head": {
                "TYPE": "LOGIN",
                "TOKEN": "",
                "SESSION_ID": "D1C72196996528253F5846F3A0E586A2",
                "DEVICE_ID": "H5",
                "CHANNEL": "",
                "SCREEN_SIZE": "",
                "SYSTEM_TYPE": "h5",
                "CHANNEL_ID": "9",
                "APP_FLAG": "BC",
                "USER_CHANNEL": ""
            },
            "param": {
                "PHONE_NUM": str(phone_number),
                "PHONE_CODE": "123456"
            }
        }
        login_act_result = requests.post(
            url=url + '/finsuit/finsuitPhone/deal',
            data={"param_key": json.dumps(login_value)})
        print(json.dumps(login_act_result.json()))
        return login_act_result.json()['head']['TOKEN']

    def api_request(self, key_name, data=None, **kwargs):
        self.data = get_value(key_name)
        self.url = self.get_evn_url + self.data['url']
        headers = {
            'content-type': "application/json",
            'accept': "*/*",
        }
        if kwargs is not None:
            for i in kwargs:
                for j in self.data['payload']['head']:
                    if i == j:
                        self.data['payload']['head'][j] = kwargs[i]
                for i in kwargs:
                    for j in self.data['payload']['param']:
                        if i == j:
                            self.data['payload']['param'][j] = kwargs[i]
        if data is not None:
            self.data['payload'] = data
        response_dicts = requests.post(url=self.url,
                                       data=json.dumps(self.data['payload']),
                                       headers=headers)

        with allure.step("url:\r" + self.url):
            pass
        with allure.step("method:\r" + self.data['method']):
            pass
        with allure.step("headers:\r" + json.dumps(headers)):
            pass
        with allure.step("payload:\r" + json.dumps(self.data['payload'])):
            pass
        with allure.step("response:\r" + json.dumps(response_dicts.json())):
            pass
        with allure.step("response:\r" + str(response_dicts.json())):
            pass
        return response_dicts.json()


if __name__ == '__main__':
    # print(RequestModule().start_request('add_admin_user'))
    # print(RequestModule().login_request())
    # print(RequestModule().get_web_header())
    # print(RequestModule().api_request('query_login_status', orgId='203'))
    print(RequestModule().get_token(13911645993))
    # print(RequestModule().get_token(18301401092))
