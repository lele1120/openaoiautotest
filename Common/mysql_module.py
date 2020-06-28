# -*- coding: utf-8 -*-
# @Time    : 2019/7/12 2:44 PM
# @Author  : XuChen
# @File    : mysql_module.py
import pymysql

from Common import log_module, env_module

log = log_module.MyLog()


class MySqlModule:
    def __init__(self):
        """
        初始化类，定义数据库连接，定义游标
        """
        self.con = ''  # 数据库连接
        self.cur = ''  # 游标
        self.get_environment = env_module.EnvModule()
        # self.data_db = ''  # 连接数据库信息
        # self.get_evn_mysql_para = self.get_environment.get_env_mysql_para(self.data_db)

    def get_evn_mysql_para(self, data_db):
        return self.get_environment.get_env_mysql_para(data_db)

    def create_connect(self, data_db):
        """
        初始化类，创建数据库连接，创建游标
        """
        try:
            self.data_db = data_db
            self.con = pymysql.connect(**self.get_evn_mysql_para(data_db))
            log.info('数据库连接正常，已创建连接')
        except Exception:
            log.error('请检查数据的参数是否正确')
        else:
            self.cur = self.con.cursor()

    def data_read(self, sqlexp, data_db):
        """
        获取数据库信息
        :param sqlexp:接收sql语句
        :param search_num: 接收查询条数，与search_all参数互斥
        :param search_all: 是否查询全部，与search_num参数互斥
        :return:返回查询结果
        """
        try:
            self.create_connect(data_db)
            self.cur.execute(sqlexp)

        except Exception:
            log.error('请检查sql语句 = %s 是否正确' % sqlexp)
        else:
            # log.info(self.cur.fetchall())
            # return self.cur.fetchall()
            # return dict(zip(col_list, self.cur.fetchone()))
            return self.cur.fetchone()
        self.close_db()

    def data_read_all(self, sqlexp, data_db):
        """
        获取数据库信息
        :param sqlexp:接收sql语句
        :param search_num: 接收查询条数，与search_all参数互斥
        :param search_all: 是否查询全部，与search_num参数互斥
        :return:返回查询结果
        """
        try:
            self.create_connect(data_db)
            self.cur.execute(sqlexp)

        except Exception:
            log.error('请检查sql语句 = %s 是否正确' % sqlexp)
        else:
            # log.info(self.cur.fetchall())
            return self.cur.fetchall()
            # # return dict(zip(col_list, self.cur.fetchone()))
            # return self.cur.fetchone()
        self.close_db()

    def data_write(self, sqlexp, data_db):
        """
        根据sql语句修改/删除数据库信息
        :param sqlexp:接收sql语句
        :return:返回查询结果
        """
        try:
            self.create_connect(data_db)
            self.cur.execute(sqlexp)
            self.con.commit()
        except:
            print('请检查sql语句 = %s 是否正确' % sqlexp)
            log.error('请检查sql语句 = %s 是否正确' % sqlexp)
            self.con.rollback()
        self.close_db()

    def close_db(self):
        """
        关闭游标，关闭数据库连接
        """
        # self.cur.close()
        # self.con.close()
        log.info('游标与数据库连接已关闭')


if __name__ == '__main__':
    print(MySqlModule().data_read_all(
        "SELECT * FROM a_id_card_auth WHERE ID_NAME = '许晨'",
        'bicai_member_id_auth_test4_enc'))
