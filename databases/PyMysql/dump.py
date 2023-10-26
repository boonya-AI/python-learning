# -*- coding: utf-8 -*-
# @File  : mysql_backup.py
# @Author: AaronJny
# @date  : 2019/11/19
# @Desc  : 使用Python脚本，批量备份MySQL数据库结构和数据
import logging
import os
import subprocess
import pymysql

# 设置日志输出格式
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)

# MySQL数据库用户名
MYSQL_USERNAME = 'root'
# 数据库密码
MYSQL_PASSWORD = 'mypassword'
# 数据库主机地址
MYSQL_HOST = '192.168.1.4'
# 数据库端口
MYSQL_PORT = 3306
# 备份文件存放路径
BACKUP_PATH = 'backup'
# 排除，不进行备份操作的数据库名称集合
DISABLED_DATABASES = {'information_schema', 'PyMysql', 'performance_schema', 'sys'}


def mkdir_if_not_exists(path):
    """
    判断给定目录是否存在，不存在则创建它

    Args:
        path: 带创建目录名称
    """
    if not os.path.exists(path):
        os.mkdir(path)


def create_mysql_conn(db='PyMysql'):
    """
    创建并返回一个mysql数据库连接

    Args:
        db: 要连接的数据库名称

    Returns:

    """
    conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USERNAME, password=MYSQL_PASSWORD, db='PyMysql')
    return conn


def read_all_databases():
    """
    从数据库中读取全部数据库名称

    Returns:
        list,数据库名称列表
    """
    logging.info('读取全部数据库名称...')
    conn = create_mysql_conn()
    cursor = conn.cursor()
    # 查询服务器上有哪些数据库
    cursor.execute('show databases')
    res = cursor.fetchall()
    databases = {item[0] for item in res}
    # 排除掉指定不备份的数据库
    databases = list(databases - DISABLED_DATABASES)
    cursor.close()
    conn.close()
    logging.info('读取完毕，数据库列表如下：{}'.format(databases))
    return databases


def backup_database(database):
    """
    备份指定数据库的数据和表结构

    Args:
        database: 待备份的数据库名称
    """
    logging.info('开始备份数据库 {}...'.format(database))
    # 通过调用mysqldump完成指定数据库的备份
    command = 'mysqldump -h192.168.1.4 -uroot -p666 --add-drop-database --databases {database} > {backup_path}/{database}.sql'.format(
        database=database,
        backup_path=BACKUP_PATH)
    exit_code = subprocess.call(command, shell=True)
    # 判断命令是否正常执行，异常则直接抛出
    if exit_code != 0:
        raise Exception('在备份数据库的过程中出错，请检查！')
    logging.info('数据库 {} 备份完毕！'.format(database))


def backup():
    """
    读取全部数据库名称，并对这些数据库的数据和结构进行备份
    """
    # 检查备份路径是否存在，不存在则进行创建
    mkdir_if_not_exists(BACKUP_PATH)
    # 读取全部待备份数据库名称
    databases = read_all_databases()
    # 逐个对数据库进行备份
    for database in databases:
        backup_database(database)


if __name__ == '__main__':
    backup()

