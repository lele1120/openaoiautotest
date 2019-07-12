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

    def login_request(self, **kwargs):
        """
        获取登录后返回授权
        :return:
        """
        dict_parm = get_value('login')
        for i in kwargs:
            for j in dict_parm['payload']:
                if i == j:
                    dict_parm['payload'][j] = kwargs[i]
        headers = {
            'authorization': "Basic YmljYWk6QmljYWkzNjU=",
            'origin': "http://manager.bicai365.com",
            'user-agent':
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            'content-type': "application/x-www-form-urlencoded",
            'accept': "*/*",
            'cache-control': "no-cache",
            'postman-token': "6db8f158-30c1-6a85-093c-7c7ffc88284b"
        }
        response = requests.request("POST",
                                    url=self.get_evn_url + dict_parm['url'],
                                    data=dict_parm['payload'],
                                    headers=headers)
        # return response
        response_dicts = json.loads(response.text)
        authorization = response_dicts['token_type'].capitalize(
        ) + ' ' + response_dicts['access_token']
        return authorization

    def get_web_header(self):
        """
        获取接口header
        :return:
        """
        response_authorization = self.login_request()

        headers = {
            'authorization': str(response_authorization),
            'origin': "http://manager.bicai365.com",
            'user-agent':
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            'content-type': "application/json;charset=UTF-8",
            'accept': "*/*",
            'cache-control': "no-cache",
            'postman-token': "a2336e2d-770c-81bc-919a-5192d95a912e"
        }
        return headers

    def start_request(self, key_name, payload=None, **kwargs):
        """
        根据value值匹配yaml文件内name获取字典数据源参数
        :param value:
        :param payload:
        :param kwargs:
        :return:response_dicts
        """
        dict_parm = get_value(key_name)
        if kwargs is not None and 'payload' in dict_parm:
            if type(dict_parm['payload']) == dict:
                for i in kwargs:
                    for j in dict_parm['payload']:
                        if i == j:
                            dict_parm['payload'][j] = kwargs[i]
        # if 'payload' in dict_parm:
            if type(dict_parm['payload']) == str:
                dict_parm['payload'] = json.loads(dict_parm['payload'])
                if kwargs is not None and 'payload' in dict_parm:
                    for i in kwargs:
                        for j in dict_parm['payload']:
                            if i == j:
                                dict_parm['payload'][j] = kwargs[i]
                dict_parm['payload'] = json.dumps(dict_parm['payload'])

        if payload is not None:
            dict_parm['payload'] = payload
        try:
            if dict_parm['method'] == 'POST':
                with allure.step("请求内容"):
                    with allure.step("method:" + dict_parm['method']):
                        pass
                    with allure.step("url:" + self.get_evn_url +
                                     str(dict_parm['url'])):
                        pass
                    with allure.step("headers:" +
                                     json.dumps(self.get_web_header())):
                        pass
                    if 'payload' in dict_parm:
                        with allure.step(
                                "payload:" +
                                str(json.loads(dict_parm['payload']))):
                            response = requests.request(
                                "POST",
                                url=self.get_evn_url + dict_parm['url'],
                                data=dict_parm['payload'],
                                headers=self.get_web_header())
                    else:
                        with allure.step("payload为空"):
                            response = requests.post(
                                url=self.get_evn_url + dict_parm['url'],
                                headers=self.get_web_header())
            elif dict_parm['method'] == 'PUT':
                with allure.step("请求内容"):
                    with allure.step("method:" + dict_parm['method']):
                        pass
                    with allure.step("url:" + self.get_evn_url +
                                     str(dict_parm['url'])):
                        pass
                    with allure.step("headers:" + str(self.get_web_header())):
                        pass

                    with allure.step("payload:" +
                                     str(json.loads(dict_parm['payload']))):
                        response = requests.request(
                            "PUT",
                            url=self.get_evn_url + dict_parm['url'],
                            data=dict_parm['payload'],
                            headers=self.get_web_header())

            elif dict_parm['method'] == 'GET':
                with allure.step("请求内容"):
                    with allure.step("method:" + dict_parm['method']):
                        pass
                    with allure.step("url:" + self.get_evn_url +
                                     str(dict_parm['url'])):
                        pass
                    with allure.step("headers:" + str(self.get_web_header())):
                        pass
                    if 'payload' in dict_parm:
                        with allure.step("payload:" +
                                         str(dict_parm['payload'])):
                            response = requests.get(
                                url=self.get_evn_url + dict_parm['url'],
                                params=dict_parm['payload'],
                                headers=self.get_web_header())
                    else:
                        with allure.step("payload为空"):
                            response = requests.get(
                                url=self.get_evn_url + dict_parm['url'],
                                headers=self.get_web_header())

        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ',
                            self.get_evn_url + dict_parm['url']))
            print(e)
            return ()

        except Exception as e:
            print('%s%s' %
                  ('Exception url: ', self.get_evn_url + dict_parm['url']))
            print(e)
            return ()

        time_consuming = response.elapsed.microseconds / 1000
        time_total = response.elapsed.total_seconds()

        Common.Consts.STRESS_LIST.append(time_consuming)

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''
        response_dicts['text'] = response.text

        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total
        with allure.step("响应报文:"):
            with allure.step("act_results:" + str(response_dicts['text'])):
                pass
        return json.loads(response_dicts['text'])

    def del_request(self, key_name, key, key2=None):
        """
        delete请求
        :param key_name:
        :param key:
        :return:

        """
        dict_parm = get_value(key_name)
        try:
            with allure.step("请求内容"):
                with allure.step("method:" + dict_parm['method']):
                    pass
                with allure.step("url:" + self.get_evn_url +
                                 str(dict_parm['url']) + "/" + str(key)):
                    pass
                with allure.step("headers:" + str(self.get_web_header())):
                    pass
                with allure.step("payload为空"):
                    if key2 is None:
                        response = requests.request(
                            "DELETE",
                            url=self.get_evn_url + dict_parm['url'] + "/" +
                            str(key),
                            headers=self.get_web_header())
                    elif key2 is not None:
                        with allure.step("url:" + self.get_evn_url +
                                         dict_parm['url'] + "/" + str(key) +
                                         "/" + str(key2)):
                            response = requests.request(
                                "DELETE",
                                url=self.get_evn_url + dict_parm['url'] + "/" +
                                str(key) + "/" + str(key2),
                                headers=self.get_web_header())

        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ',
                            self.get_evn_url + dict_parm['url'] + "/" + key))
            print(e)
            return ()

        except Exception as e:
            print('%s%s' % ('Exception url: ',
                            self.get_evn_url + dict_parm['url'] + "/" + key))
            print(e)
            return ()

        time_consuming = response.elapsed.microseconds / 1000
        time_total = response.elapsed.total_seconds()

        Common.Consts.STRESS_LIST.append(time_consuming)

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''
        response_dicts['text'] = response.text
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total
        with allure.step("响应报文:"):
            with allure.step("act_results:" + str(response_dicts['text'])):
                pass
        return json.loads(response_dicts['text'])

    def get_request(self, key_name, key):
        """
        delete请求
        :param url:

        :param header:
        :return:

        """
        dict_parm = get_value(key_name)
        try:
            with allure.step("请求内容"):
                with allure.step("method:" + str(dict_parm['method'])):
                    pass
                with allure.step("url:" + self.get_evn_url + dict_parm['url'] +
                                 "/" + str(key)):
                    pass
                with allure.step("headers:" +
                                 json.dumps(self.get_web_header())):
                    pass
                with allure.step("payload为空"):
                    response = requests.request("GET",
                                                url=self.get_evn_url +
                                                dict_parm['url'] + "/" +
                                                str(key),
                                                headers=self.get_web_header())

        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ',
                            self.get_evn_url + dict_parm['url'] + "/" + key))
            print(e)
            return ()

        except Exception as e:
            print('%s%s' % ('Exception url: ',
                            self.get_evn_url + dict_parm['url'] + "/" + key))
            print(e)
            return ()

        time_consuming = response.elapsed.microseconds / 1000
        time_total = response.elapsed.total_seconds()

        Common.Consts.STRESS_LIST.append(time_consuming)

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''
        response_dicts['text'] = response.text
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total
        with allure.step("响应报文:"):
            with allure.step("act_results:" + str(response_dicts['text'])):
                pass
        return json.loads(response_dicts['text'])

    def put_request(self, key_name, payload=None, **kwargs):
        """
        根据value值匹配yaml文件内name获取字典数据源参数
        :param value:
        :param payload:
        :param kwargs:
        :return:response_dicts
        """
        dict_parm = get_value(key_name)
        if kwargs is not None and 'payload' in dict_parm:
            if type(dict_parm['payload']) == dict:
                for i in kwargs:
                    for j in dict_parm['payload']:
                        if i == j:
                            dict_parm['payload'][j] = kwargs[i]
            if type(dict_parm['payload']) == str:
                dict_parm['payload'] = json.loads(dict_parm['payload'])
                if kwargs is not None and 'payload' in dict_parm:
                    for i in kwargs:
                        for j in dict_parm['payload']:
                            if i == j:
                                dict_parm['payload'][j] = kwargs[i]
                dict_parm['payload'] = json.dumps(dict_parm['payload'])

        if payload is not None:
            dict_parm['payload'] = payload
        try:
            with allure.step("请求内容"):
                with allure.step("method:" + dict_parm['method']):
                    pass
                with allure.step("url:" + self.get_evn_url +
                                 str(dict_parm['url'])):
                    pass
                with allure.step("headers:" + str(self.get_web_header())):
                    pass
                if 'payload' in dict_parm:
                    with allure.step("payload:" + str(dict_parm['payload'])):
                        response = requests.request(
                            "PUT",
                            url=self.get_evn_url + dict_parm['url'],
                            params=dict_parm['payload'],
                            headers=self.get_web_header())
                else:
                    with allure.step("payload为空"):
                        response = requests.post(url=self.get_evn_url +
                                                 dict_parm['url'],
                                                 headers=self.get_web_header())

        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ',
                            self.get_evn_url + dict_parm['url']))
            print(e)
            return ()

        except Exception as e:
            print('%s%s' %
                  ('Exception url: ', self.get_evn_url + dict_parm['url']))
            print(e)
            return ()

        time_consuming = response.elapsed.microseconds / 1000
        time_total = response.elapsed.total_seconds()

        Common.Consts.STRESS_LIST.append(time_consuming)

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''
        response_dicts['text'] = response.text

        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total
        with allure.step("响应报文:"):
            with allure.step("act_results:" + str(response_dicts['text'])):
                pass
        return json.loads(response_dicts['text'])


if __name__ == '__main__':
    # print(RequestModule().start_request('add_admin_user'))
    print(RequestModule().login_request())
    # print(RequestModule().get_web_header())
