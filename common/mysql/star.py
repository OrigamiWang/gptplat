# _*_ coding : utf-8 _*_
# @Time : 2023/10/16 19:29
# @Author : Origami
# @File : star
# @Project : gptplat
from common.mysql.mysql_util import db


# 获取某个用户的收藏夹列表
def get_star_list(user_id: int):
    with db.cursor() as cursor:
        sql = 'select * from star where user_id = ' + str(user_id)
        print(sql)
        cursor.execute(sql)
    return cursor.fetchall()


# 修改收藏夹名字
def update_start_name(user_id: int, old_name: str, new_name: str):
    with db.cursor() as cursor:
        sql = "UPDATE star SET `name`= \'" + new_name + "\' WHERE user_id = " + str(
            user_id) + " AND BINARY `name` = \'" + old_name + "\'"
        print(sql)
        cursor.execute(sql)
    db.commit()


# 根据名字删除某个收藏夹(那么收藏夹名字不允许重复)
def delete_star(user_id: int, name: str):
    with db.cursor() as cursor:
        sql = "DELETE FROM star WHERE BINARY `name` = \'" + name + "\' AND `user_id` = " + str(user_id)
        print(sql)
        cursor.execute(sql)
    db.commit()
    return


# 创建收藏夹
def create_star(user_id: int, name: str):
    with db.cursor() as cursor:
        sql = "INSERT INTO star(`user_id`, `name`) VALUES(" + str(user_id) + ", \'" + name + "\')"
        print(sql)
        cursor.execute(sql)
    db.commit()


# 查询某个用户是否已经创建了某个名字的收藏夹（防止收藏夹名字重复）
# BINARY: 强制mysql区分大小写
def find_star(name: str):
    with db.cursor() as cursor:
        sql = "SELECT * FROM star WHERE BINARY `name`= \'" + name + "\'"
        print(sql)
        cursor.execute(sql)
    res = cursor.fetchone()
    if res is not None and len(res) > 0:
        return True
    return False
