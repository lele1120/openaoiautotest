# -*- coding: utf-8 -*-
# @Time    : 2019/7/12 2:23 PM
# @Author  : XuChen
# @File    : run.py

from Common import email_module, log_module, Consts, Shell
from Conf import Config
import pytest
if __name__ == '__main__':
    """
    执行所有case并生成报告
    """
    conf = Config.Config()
    shell = Shell.Shell()
    log = log_module.MyLog()
    log.info('初始化配置文件, path=' + conf.conf_path)
    test_run_path = conf.run_path
    xml_report_path = conf.xml_report_path
    html_report_path = conf.html_report_path

    # 定义测试集
    allure_list = '--allure_features=jch'
    args = ['-q', '--maxfail=5', '--alluredir', xml_report_path, allure_list]
    log.info('执行用例集为：%s' % allure_list)
    pytest.main(args)
    cmd = 'allure generate %s -o %s  --clean' % (xml_report_path,
                                                 html_report_path)

    try:
        shell.invoke(cmd)
    except Exception:
        log.error('执行用例失败，请检查环境配置')
        raise

    test_body = Consts.TEST_LIST
    result_body = Consts.RESULT_LIST
    error_number = test_body.__len__() - result_body.__len__()

    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("运行" + str(test_body.__len__()) + "个测试用例")
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("成功" + str(result_body.__len__()) + "个测试用例")
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("失败" + str(error_number) + "个测试用例")
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")

    # try:
    #     mail = email_module.SendMail()
    #     mail.sendMail()
    # except:
    #     log.error('发送邮件失败，请检查邮件配置')
    #     raise
