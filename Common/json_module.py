# -*- coding: utf-8 -*-
# @Time    : 2019/7/12 2:35 PM
# @Author  : XuChen
# @File    : json_module.py
"""
获取返回值中指定值

"""
from Common import log_module


class JsonModule:
    def __init__(self):
        self.log = log_module.MyLog()

    def get_act_value(self, response_dicts, key_name):
        """
        :return: 获取返回值中指定的值
        """
        appoint_id = ''
        try:
            for i in range(0, response_dicts['data']['list'].__len__()):
                if response_dicts['data']['list'][i]['name'] == key_name:
                    appoint_id = response_dicts['data']['list'][i]['id']
        except Exception as e:
            print(e)
            self.log.error("未找到指定的id")
        return appoint_id
