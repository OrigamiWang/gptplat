import os
import time
import yaml


def get_session_id():
    return str(time.time()).replace('.', '')


def get_num_by_role(role):
    role_dict = {'system': 1, 'user': 2, 'assistant': 3}
    return role_dict[role]


def get_role_by_num(num):
    role_dict = {1: "system", 2: "user", 3: "assistant"}
    return role_dict[num]

# 将datetime字段从datetime类型转成str类型
def process_history_datetime(history_list):
    for history in history_list:
        history[3] = str(history[3])
    return history_list


def list_to_dict(content_list):
    content_dict_list = []
    for content in content_list:
        content_dict_list.append(
            {"sessionId": content[1], "role": get_role_by_num(content[2]), "content": content[3]})
    return content_dict_list


def tuple_to_list(tu):
    li = []
    for t in tu:
        li.append(list(t))
    return li


def read_yaml(keys):
    try:
        key_list = str(keys).split('.')
        data = None
        # 相对路径，保证不同文件都能访问的到
        file_path = os.path.join(os.path.dirname(__file__), '../gpt/resources/config.yml')
        fs = open(file_path, encoding="UTF-8")
        data = yaml.load(fs, Loader=yaml.FullLoader)
        for key in key_list:
            data = data[key]
        return data
    except Exception as e:
        print(e)


if __name__ == '__main__':
    arr = [1, 2, 3, 4]
    idx = "2"
