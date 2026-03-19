import base64
import json
import os
import ast
import configparser

def string_to_base64(input_string):
    byte_data = input_string.encode('utf-8')
    base64_encoded = base64.b64encode(byte_data)
    return base64_encoded.decode('utf-8')

def base64_to_string(base64_string):
    byte_data = base64.b64decode(base64_string)
    original_string = byte_data.decode('utf-8')

    return original_string

def string_to_json(input_string):
    return json.loads(input_string)

def json_to_string(json_object):
    return json.dumps(json_object, ensure_ascii=False)

def add(target_file,music_name):
    # 确定文件路径
    if target_file == 'main':
        file_path = os.path.join('mp3_db','main_db.txt')
    else:
        file_path = os.path.join('mp3_db','my_lists',target_file)

    # 读取文件内容
    with open(file_path,'r',encoding='utf-8') as f:
        music_list = ast.literal_eval(base64_to_string(f.read()))

    # 添加歌曲(防止重复)
    if music_name in [n[0] for n in music_list]:
        print('文件已存在')
        return '文件已存在'
    else:
        music_list.append([music_name,0,0])

    # 覆写文件
    with open(file_path,'w',encoding='utf-8') as f:
        f.write(string_to_base64(str(music_list)))

def delete(target_file,music_name):
    # 确定文件路径
    if target_file == 'main':
        file_path = os.path.join('mp3_db', 'main_db.txt')
    else:
        file_path = os.path.join('mp3_db', 'my_lists', target_file)

    # 对target_file操作
    # 读取文件内容
    with open(file_path,'r',encoding='utf-8') as f:
        music_list = ast.literal_eval(base64_to_string(f.read()))
    # 生成删除目标歌曲后的列表
    new_list = []
    for n in music_list:
        if n[0] != music_name:
            new_list.append(n)
    # 覆写文件
    with open(file_path,'w',encoding='utf-8') as f:
        f.write(string_to_base64(str(new_list)))

    # 当target_file为main时删除其他歌单中的该歌曲
    if target_file == 'main':
        # 读取设置
        config = configparser.ConfigParser()
        config.read('config.ini')
        if config['dbcrudtool']['AUTO_DELETE'] == 'False':
            return None
        # 对其他歌单中的文件删除
        for file_name in os.listdir(os.path.join('mp3_db','my_lists')):
            full_path = os.path.join('mp3_db', 'my_lists',file_name)
            with open(full_path,'r',encoding='utf-8') as f:
                music_list = ast.literal_eval(base64_to_string(f.read()))

            new_list = []
            for n in music_list:
                if n[0] != music_name:
                    new_list.append(n)

            with open(full_path,'w',encoding='utf-8') as f:
                f.write(string_to_base64(str(new_list)))

def update(target_file,music_name,index,num):  # index为1时更改播放次数,为2时更改播放秒数
    # 确定文件路径
    if target_file == 'main':
        file_path = os.path.join('mp3_db', 'main_db.txt')
    else:
        file_path = os.path.join('mp3_db', 'my_lists', target_file)

    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        music_list = ast.literal_eval(base64_to_string(f.read()))

    # 更新操作
    for n in music_list:
        if n[0] == music_name:
            n[index] = num

    with open(file_path,'w',encoding='utf-8') as f:
        f.write(string_to_base64(str(music_list)))

def show(target_file):
    # 确定文件路径
    if target_file == 'main':
        file_path = os.path.join('mp3_db', 'main_db.txt')
    else:
        file_path = os.path.join('mp3_db', 'my_lists', target_file)

    with open(file_path,'r',encoding='utf-8') as f:
        music_list = ast.literal_eval(base64_to_string(f.read()))

    print(music_list)
    return music_list

def base64_and_save(target_file,str):
    # 确定文件路径
    if target_file == 'main':
        file_path = os.path.join('mp3_db', 'main_db.txt')
    else:
        file_path = os.path.join('mp3_db', 'my_lists', target_file)

    with open(file_path,'w',encoding='utf-8') as f:
        f.write(string_to_base64(str))

def add2(target_file,music_name,play_times):
    # 确定文件路径
    if target_file == 'main':
        file_path = os.path.join('mp3_db', 'main_db.txt')
    else:
        file_path = os.path.join('mp3_db', 'my_lists', target_file)

    # 读取文件内容
    with open(file_path,'r',encoding='utf-8') as f:
        print(base64_to_string(f.read()))


if __name__ == '__main__':
    print(string_to_base64('{}'))
    #base64_and_save('main',string_to_json("{}"))
    #add2('main',"v",30)

    #show('main')
    #show('list1.txt')
    #show('list2.txt')

    #print([n.split('.')[0] for n in os.listdir(os.path.join('mp3_db','my_lists'))])