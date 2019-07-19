# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 1:55 PM
# @Author  : XuChen
# @File    : dd_module.py
import requests
import json


class SendDingDing:
    def sendDingDing(self):
        url = 'https://oapi.dingtalk.com/robot/send?access_token=00eaa883c32dcc023a95b4ee84045659e2ddd8a8d5a98233cb0e2809d33c5f3d'
        program = {
            "msgtype": "text",
            "text": {
                "content": "金城银行充值存入赎回提现接口已经通过测试。"
            },
        }
        headers = {'Content-Type': 'application/json'}
        requests.post(url, data=json.dumps(program), headers=headers)


if __name__ == '__main__':
    SendDingDing().sendDingDing()
