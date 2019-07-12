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
    # print(MySqlModule().data_read(" select * from sys_user")[0])
    # MySqlModule().data_write("INSERT INTO sys_user VALUES ( 0, 'xiaocccb', '{bcrypt}$2a$10$XQgkulIVN0UdDRQXGNISfOBQmxwBBv.XQ75Fq8NPVmBePYIbqxu4W', NULL, '173992642333', NULL, 3, '2018-08-06 14:44:42', '2018-12-29 10:18:09', '0' );")cccb', '{bcrypt}$2a$10$XQgkulIVN0UdDRQXGNISfOBQmxwBBv.XQ75Fq8NPVmBePYIbqxu4W', NULL, '173992642333', NULL, 3, '2018-08-06 14:44:42', '2018-12-29 10:18:09', '0' );")
    # MySqlModule().data_write("DELETE FROM sys_user WHERE username = 'xiaobbbb';")
    # username = ["xiaohuang", "xiaohong", "xiaolv", "xiaozi", "xiaohei", "xiaobai", "xiaocheng"]
    # phone_num = ["13922290999", "13933390999", "13944490999", "13955590999", "13966690999", "13977790999", "13988890999"]
    # for i in range(username.__len__()):
    #     sql_insert = "INSERT INTO sys_user VALUES ( 0, '%s', '{bcrypt}$2a$10$XQgkulIVN0UdDRQXGNISfOBQmxwBBv.XQ75Fq8NPVmBePYIbqxu4W', NULL, '%s', NULL, 3, '2018-08-06 14:44:42', '2018-12-29 10:18:09', '0' )"%(str(username[i]), str(phone_num[i]))
    #     MySqlModule().data_write(sql_insert)
    #
    # for i in range(username.__len__()):
    #     sql_insert = "DELETE FROM sys_user WHERE username = '%s' ;" % username[i]
    #     MySqlModule().data_write(sql_insert)
    list_aa = MySqlModule().data_read_all(
        "SELECT * FROM sys_role_menu WHERE role_id = '1'", 'bicai_admin')
    # list_bb = []
    # for i in range(0, list_aa.__len__()):
    #     list_bb.append(list_aa[i][0])
    # list_cc = [x[0] for x in list_aa]
    print(list_aa)
    # print(MySqlModule().data_read("SELECT menu_id FROM sys_role_menu WHERE role_id = '1'"))
