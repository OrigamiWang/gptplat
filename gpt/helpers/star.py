# _*_ coding : utf-8 _*_
# @Time : 2023/10/16 19:28
# @Author : Origami
# @File : star
# @Project : gptplat

from common.mysql.star import get_star_list, update_start_name, create_star, find_star, delete_star


def get_star_list_by_id(user_id: int):
    return get_star_list(user_id)


def update_star_name_by_name(user_id: int, old_name: str, new_name:str):
    if not find_star(new_name):
        update_start_name(user_id, old_name, new_name)
        return True
    return False


def create_star_by_id(user_id: int, name: str):
    create_star(user_id, name)


def delete_user_by_id(user_id: int, name: str):
    delete_star(user_id, name)
