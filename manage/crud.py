# _*_ coding : utf-8 _*_
# @Time : 2023/9/9 16:49
# @Author : Origami
# @File : crud
# @Project : gptplat
import threading

from common.mysql import mysql_util



def get_all_user():
    with mysql_util.db.cursor() as cursor:
        sql = 'select * from users'
        cursor.execute(sql)
        users = cursor.fetchall()
    return users


def get_user_by_pages(page_num, page_size):
    """
    :param page_num: 页码
    :param page_size: 每页条数
    :return: res
    """
    with mysql_util.db.cursor() as cursor:
        offset = (int(page_num) - 1) * int(page_size)
        sql = 'select * from users limit ' + str(offset) + "," + str(page_size) + ";"
        cursor.execute(sql)
        users = cursor.fetchall()
    return users


def get_user_by_id(user_id):
    with mysql_util.db.cursor() as cursor:
        sql = "select * from users u where u.`id` = " + user_id + ";"
        cursor.execute(sql)
        user = cursor.fetchone()
    return user




def add_users(user_list):
    with mysql_util.db.cursor() as cursor:
        sql = "insert into users(`username`, `password`, `permission`) values "
        for user in user_list:
            username = user['username']
            password = user['password']
            permission = user['permission']

            sql += "(\'" + username + "\',\'" + password + "\'," + str(permission) + "),"
        sql = sql[0:len(sql) - 1] + ";"
        print(sql)
        cursor.execute(sql)
        mysql_util.db.commit()


def update_user(past_username, user):
    with mysql_util.db.cursor() as cursor:
        sql = "UPDATE users u SET u.`username` = \'" + user['username'] \
              + "\', u.`password` = \'" + user['password'] + "\', u.`permission` = " \
              + str(user['permission']) + " WHERE u.`username` = \'" + past_username + "\';"
        cursor.execute(sql)
        mysql_util.db.commit()


def delete_user_by_id(user_id):
    with mysql_util.db.cursor() as cursor:
        sql = "DELETE u FROM users u WHERE u.`id` = \'" + str(user_id) + "\'"
        cursor.execute(sql)
        mysql_util.db.commit()
