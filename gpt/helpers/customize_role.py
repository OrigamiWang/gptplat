# _*_ coding : utf-8 _*_
# @Time : 2023/9/25 21:37
# @Author : Origami
# @File : customize_role
# @Project : gptplat
from common.mysql.customize_role import get_role_by_id, select_role_list, add_role


def get_role_list():
    arr = select_role_list()
    print(arr)
    return arr


def get_role_sentence(id):
    return get_role_by_id(int(id))[0]


def add_new_role(name, sentence):
    add_role(name, sentence)
