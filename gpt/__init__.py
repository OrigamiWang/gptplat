# _*_ coding : utf-8 _*_
# @Time : 2023/9/2 15:17
# @Author : Origami
# @File : __init__2
# @Project : gptplat
from flask import Blueprint

# avoid circle import
gpt_api = Blueprint("gpt", __name__)
from gpt import views
