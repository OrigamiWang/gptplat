import os
import logging
import time
from logging.handlers import RotatingFileHandler


# log配置，实现日志自动按日期生成日志文件
def make_dir(make_dir_path):
    path = make_dir_path.strip()
    if not os.path.exists(path):
        os.makedirs(path)


# 过滤日志，只获取对应日志级别的文件
class LevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


def getLogHandler(log_level):
    # 日志地址
    log_dir_name = "Logs"
    # 文件名，以日期作为文件名
    log_file_name = f'logger-{logging.getLevelName(log_level).lower()}-{time.strftime("%Y-%m-%d", time.localtime(time.time()))}.log'
    log_file_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)) + os.sep + log_dir_name
    make_dir(log_file_folder)
    log_file_str = log_file_folder + os.sep + log_file_name

    # 默认日志等级的设置
    logging.basicConfig(level=log_level)
    # 创建日志记录器，指明日志保存路径,每个日志的大小，保存日志的上限
    file_log_handler = RotatingFileHandler(log_file_str, maxBytes=1024 * 1024, backupCount=10, encoding='UTF-8')
    # 设置日志的格式                   发生时间    日志等级     日志信息文件名      函数名          行数        日志信息
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    # 将日志记录器指定日志的格式
    file_log_handler.setFormatter(formatter)

    file_log_handler.addFilter(LevelFilter(log_level))
    # 日志等级的设置
    file_log_handler.setLevel(log_level)

    return file_log_handler
