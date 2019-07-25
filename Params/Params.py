# -*- coding: utf-8 -*-
# @Time    : 2019/7/12 2:57 PM
# @Author  : XuChen
# @File    : Params.py
import json
import os
import yaml
from Common import log_module

log = log_module.MyLog()
path_dir = str(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))


def get_value(key_name):
    """
    获取yaml文件
    :param value:
    :return:
    """
    log.info('解析yaml, Path:' + path_dir + '/Params/Param/Basics')
    yamlPath = path_dir + '/Params/Param/Basics.yaml'
    f = open(yamlPath, 'r', encoding='utf-8')
    y = yaml.load_all(f)
    try:
        for data in y:
            if data['name'] == key_name:
                return data
    except Exception:
        log.info("未获取到name为:" + key_name + "的数据")
        raise


def exp_results(key_name):
    """
    获取yaml文件中的预期结果
    :param value:
    :return:
    """
    log.info('解析yaml, Path:' + path_dir + '/Params/Param/Basics')
    yamlPath = path_dir + '/Params/Param/Basics.yaml'
    f = open(yamlPath, 'r', encoding='utf-8')
    y = yaml.load_all(f)
    try:
        for data in y:
            if data['name'] == key_name:
                return data['check']
    except Exception:
        log.info("未获取到name为:" + key_name + "的数据")
        raise


def get_payload(key_name):
    payload = {
        "head": get_value(key_name)['head'],
        "param": get_value(key_name)['param']
    }
    return payload


if __name__ == '__main__':
    print(exp_results('query_login_status')['code'])
