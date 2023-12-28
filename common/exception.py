# _*_ coding : utf-8 _*_
# @Time : 2023/9/2 15:32
# @Author : Origami
# @File : exception
# @Project : gptplat
import traceback

from flask import jsonify, make_response, current_app
from common import status as status_code


class PageNotFoundException(Exception):
    def __init__(self, msg="unknown err"):
        self.msg = msg
        self.status = status_code.HTTP_PAGE_NOT_FOUND

    @staticmethod
    def handler_err(self, e: Exception, url: str):
        current_app.logger.error(f"An error occurred: {e}")
        resp = make_response("we cannot found the page: {}".format(url))
        resp.status = status_code.HTTP_PAGE_NOT_FOUND
        return resp


class FileParseException(Exception):
    def __init__(self, msg="unknown err"):
        self.msg = msg
        self.status = status_code.HTTP_FILE_PARSE_ERR

    @staticmethod
    def handler_err(self, e: Exception):
        file_path = 'unnamed'
        current_app.logger.error(f"An error occurred: {e}")
        resp = make_response("we cannot parse the file: {}".format(file_path))
        resp.status = status_code.HTTP_FILE_PARSE_ERR
        return resp


class ServerException(Exception):
    def __init__(self, msg="unknown err"):
        self.msg = msg
        self.status = status_code.HTTP_SERVER_ERR

    @staticmethod
    def handler_err(self, e: Exception):
        current_app.logger.error(f"An error occurred: {e}")
        resp = make_response("some error may occurred in the server")
        resp.status = status_code.HTTP_SERVER_ERR
        return resp
