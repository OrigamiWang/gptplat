# _*_ coding : utf-8 _*_
# @Time : 2023/9/2 15:16
# @Author : Origami
# @File : __init__
# @Project : gptplat
from flask import Blueprint

# avoid circle import
auth_api = Blueprint("auth", __name__)
from auth import views
