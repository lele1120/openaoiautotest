# -*- coding: utf-8 -*-
# @Time    : 2020/6/16 2:29 PM
# @Author  : XuChen
# @File    : redis_module.py
import redis
from Common import log_module, env_module
log = log_module.MyLog()
# r = redis.Redis(host='39.105.127.54',
#                 port=6379,
#                 password='qwer1234',
#                 db=1,
#                 decode_responses=True)
# # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
# aa = r.hgetall('1538420_165_ASSET_AMOUNT_BY_ORG')
# bb = r.hgetall('1538420_ASSET_AMOUNT_BY_PRD_TYPE')
# cc = r.hkeys('1538420_ASSET_AMOUNT_BY_PRD_TYPE')
# print(aa)
# print("========================")
# print(bb)
# print("========================")
# print(cc)


class RedisModule:
    def __init__(self):
        """
        初始化类，定义redis连接
        """
        self.get_environment = env_module.EnvModule()

    def get_evn_redis_para(self):
        return self.get_environment.get_env_redis_para()

    # def create_connect(self):
    #     """
    #     初始化类，创建redis连接，创建游标
    #     """
    #     try:
    #         redis.Redis(**self.get_evn_redis_para())
    #         log.info('redis连接正常，已创建连接')
    #     except Exception:
    #         log.error('请检查数据的参数是否正确')

    def data_read_by_org(self, member_id, org_id):
        """
        根据orgid和memberid在机构维度查询        
        """
        query_key = str(member_id) + "_" + str(org_id) + "_ASSET_AMOUNT_BY_ORG"

        try:
            r = redis.Redis(**self.get_evn_redis_para())
            return r.hgetall(str(query_key))
        except Exception:
            log.error('请检查querykey = %s 是否正确' % query_key)

    def data_read_by_prd_type(self, member_id):
        """
        根据memberid在产品维度查询        
        """
        query_key = str(member_id) + "_ASSET_AMOUNT_BY_PRD_TYPE"

        try:
            r = redis.Redis(**self.get_evn_redis_para())
            return r.hgetall(str(query_key))
        except Exception:
            log.error('请检查querykey = %s 是否正确' % query_key)


if __name__ == '__main__':
    print(RedisModule().data_read_by_org("1538420", "165"))
    print("+++++++++++++++++++++")
    print(RedisModule().data_read_by_prd_type("1538420"))
