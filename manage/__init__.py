# _*_ coding : utf-8 _*_
# @Time : 2023/9/9 14:28
# @Author : Origami
# @File : __init__
# @Project : gptplat

from flask import Blueprint

manage_api = Blueprint("manage", __name__)
from manage import views
