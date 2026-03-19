import base64
import json
import os
import logging

logging.basicConfig(
    filename = 'logs/dbcrudtool.log',
    level = logging.WARNING,
    format = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    encoding = 'utf-8'
)


def dict_to_base64(data):
    json_data = json.dumps(data)
    base64_encoded = base64.b64encode(json_data.encode('utf-8'))
    return base64_encoded.decode('utf-8')

def base64_to_dict(base64_code):
    base64_decoded = base64.b64decode(base64_code)
    json_data = base64_decoded.decode('utf-8')
    return json.loads(json_data)

def path_deal(func):
    def wrapper(target_file, music_name=None):
        # 处理路径逻辑
        if target_file == 'main':
            file_path = os.path.join('mp3_db', 'main_db.txt')
        elif os.path.exists(os.path.join('mp3_db', 'my_lists', target_file + '.txt')):
            file_path = os.path.join('mp3_db', 'my_lists', target_file + '.txt')
        else:
            logging.warning(f'歌单不存在: {target_file} at {os.path.join("mp3_db", "my_lists", target_file + ".txt")}')
            return None

        # music_name是否存在返回结果不同
        if music_name is None:
            return func(file_path)
        else:
            return func(file_path, music_name)

    return wrapper


@path_deal
def add(file_path, music_name):
    # 读取并处理
    with open(file_path, 'r', encoding='utf-8') as f:
        origin_dict = base64_to_dict(f.read())

    # 检查是否有重复歌曲
    if music_name in origin_dict:
        print('add中文件已存在')
        logging.warning(f'add中文件已存在: {music_name} in {file_path}')
        return '文件已存在'

    # 添加歌曲
    origin_dict[music_name] = 0
    purpose_data = dict_to_base64(origin_dict)

    # 覆写文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(purpose_data)

@path_deal
def delete(file_path, music_name):
    # 读取并处理
    with open(file_path, 'r', encoding='utf-8') as f:
        origin_dict = base64_to_dict(f.read())

    # 删除歌曲
    if music_name in origin_dict:
        del origin_dict[music_name]
    else:
        print('delete中文件不存在')
        logging.warning(f'delete中文件不存在: {music_name} not in {file_path}')
        return '文件不存在'
    purpose_data = dict_to_base64(origin_dict)

    # 覆写文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(purpose_data)

@path_deal
def clean(file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(dict_to_base64({}))

@path_deal
def add_time(file_path,music_name):
    # 读取
    with open(file_path,'r',encoding='utf-8') as f:
        origin_dict = base64_to_dict(f.read())

    # 播放次数加1(主歌单中如果存在也加1)
    if music_name in origin_dict:
        origin_dict[music_name] += 1
        if file_path != os.path.join('mp3_db', 'main_db.txt'):
            add_time('main', music_name)
    else:
        print('add_time中文件不存在')
        logging.warning(f'add_time中文件不存在: {music_name} not in {file_path}')
        return '文件不存在'

    # 覆写
    with open(file_path,'w',encoding='utf-8') as f:
        f.write(dict_to_base64(origin_dict))

@path_deal
def check(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        origin_dict = base64_to_dict(f.read())
    return origin_dict

@path_deal
def check_time(file_path,music_name):
    # 打开文件
    with open(file_path,'r',encoding='utf-8') as f:
        origin_dict = base64_to_dict(f.read())

    if music_name in origin_dict:
        return origin_dict[music_name]
    else:
        print('check_time中文件不存在')
        logging.warning(f'check_time中文件不存在: {music_name} not in {file_path}')
        return '文件不存在'

@path_deal
def check_time_sum(file_path):
    # 打开文件
    with open(file_path,'r',encoding='utf-8') as f:
        origin_dict = base64_to_dict(f.read())

    return sum(origin_dict.values())

def add_list(file_name):
    file_path = os.path.join('mp3_db', 'my_lists', file_name + '.txt')
    if os.path.exists(file_path):
        print('歌单已存在')
        logging.warning(f'歌单已存在: {file_name} at {file_path}')
        return '歌单已存在'
    else:
        with open(file_path,'w',encoding='utf-8') as f:
            f.write(dict_to_base64({}))

def delete_list(file_name):
    file_path = os.path.join('mp3_db', 'my_lists', file_name + '.txt')
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print('歌单不存在')
        logging.warning(f'歌单不存在: {file_name} at {file_path}')
        return '歌单不存在'

def check_lists():
    lists = []
    for file_name in os.listdir(os.path.join('mp3_db', 'my_lists')):
        if file_name.endswith('.txt'):
            lists.append(file_name.split('.')[0])
    return lists


# 调试区
print(check_time_sum('main'))
print(check('main'))
print(check('list1'))
print(check('list2'))
print(check_time('main','test'))
print(check_lists())



'Shift+F10'