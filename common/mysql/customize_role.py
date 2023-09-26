# _*_ coding : utf-8 _*_
# @Time : 2023/9/25 22:14
# @Author : Origami
# @File : customize_role
# @Project : gptplat
from common.mysql.mysql_util import db


def get_role_by_id(id: int):
    with db.cursor() as cursor:
        sql = 'SELECT r.`sentence` FROM customize_role r WHERE r.`id` = ' + str(id)
        cursor.execute(sql)
    return cursor.fetchone()


def select_role_list():
    """
    :return role的id和name
    """
    with db.cursor() as cursor:
        sql = 'SELECT c.`id`, c.`name` FROM customize_role c'
        cursor.execute(sql)
    return cursor.fetchall()


def add_role(name, sentence):
    with db.cursor() as cursor:
        sql = "INSERT INTO customize_role(`name`, `sentence`) VALUES('" + name + "', '" + sentence + "');"
        cursor.execute(sql)
        db.commit()