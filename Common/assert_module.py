# -*- coding: utf-8 -*-
# @Time    : 2019/7/12 2:32 PM
# @Author  : XuChen
# @File    : assert_module.py
"""
封装Assert方法

"""
import allure

from Common import log_module
from Common import Consts
import json


class AssertModule:
    def __init__(self):
        self.log = log_module.MyLog()

    def assert_code(self, expected_code, code):
        """
        验证response状态码
        :param code:
        :param expected_code:
        :return:
        """

        with allure.step("使用返回code做对比："):

            with allure.step("预期状态码:" + str(expected_code)):
                pass
            with allure.step("实际状态码:" + str(code)):
                pass

        try:

            assert code == expected_code
            print("预期状态码:" + str(expected_code))
            print("实际状态码:" + str(code))
            return True
        except:
            self.log.error(
                "statusCode error, expected_code is %s, statusCode is %s " %
                (expected_code, code))
            Consts.ASSERT_FAIL_LIST.append('fail')

            raise

    def assert_text(self, act_msg, expected_msg, remark=None):
        """
        验证response act_msg中是否等于预期字符串
        :param act_msg:
        :param expected_msg:
        :return:
        """
        if remark is not None:
            with allure.step("使用" + remark + "做对比:"):
                with allure.step("预期结果:" + str(expected_msg)):
                    pass
                with allure.step("实际结果:" + str(act_msg)):
                    pass
        else:
            with allure.step("预期结果:" + str(expected_msg)):
                pass
            with allure.step("实际结果:" + str(act_msg)):
                pass
        try:

            assert act_msg == expected_msg
            return True

        except:
            self.log.error(
                "Response body != expected_msg, expected_msg is %s, body is %s"
                % (expected_msg, body))
            Consts.ASSERT_FAIL_LIST.append('fail')

            raise

    def assert_body(self, body, body_msg, expected_msg):
        """
        验证response body中任意属性的值
        :param body:
        :param body_msg:
        :param expected_msg:
        :return:
        """
        try:
            msg = body[body_msg]
            assert msg == expected_msg
            return True

        except:
            self.log.error(
                "Response body msg != expected_msg, expected_msg is %s, body_msg is %s"
                % (expected_msg, body_msg))
            Consts.ASSERT_FAIL_LIST.append('fail')

            raise

    def assert_in_text(self, body, expected_msg):
        """
        验证response body中是否包含预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            text = json.dumps(body, ensure_ascii=False)
            # print(text)
            assert expected_msg in text
            return True

        except:
            self.log.error(
                "Response body Does not contain expected_msg, expected_msg is %s"
                % expected_msg)
            Consts.ASSERT_FAIL_LIST.append('fail')

            raise

    def assert_time(self, time, expected_time):
        """
        验证response body响应时间小于预期最大响应时间,单位：毫秒
        :param body:
        :param expected_time:
        :return:
        """
        try:
            assert time < expected_time
            return True

        except:
            self.log.error(
                "Response time > expected_time, expected_time is %s, time is %s"
                % (expected_time, time))
            Consts.ASSERT_FAIL_LIST.append('fail')

            raise

    def assert_in_results(self, actual_results, expected_results):
        """
        验证response状态码
        :param actual_results:实际结果
        :param expected_results: 预期结果
        :return:
        """
        try:
            assert actual_results == expected_results
            print("预期结果:" + str(expected_results))
            print("实际结果:" + str(actual_results))
            return True
        except:
            self.log.error(
                "query results error, expected_results is %s, actual_results is %s "
                % (actual_results, expected_results))
            Consts.ASSERT_FAIL_LIST.append('fail')

    def assert_not_in_results(self, actual_results, expected_results):
        """
        验证response状态码
        :param actual_results:实际结果
        :param expected_results: 预期结果
        :return:
        """
        try:
            assert actual_results is not expected_results
            print("预期结果:" + str(expected_results))
            print("实际结果:" + str(actual_results))
            return True
        except:
            self.log.error(
                "query results error, expected_results is %s, actual_results is %s "
                % (actual_results, expected_results))
            Consts.ASSERT_FAIL_LIST.append('fail')
