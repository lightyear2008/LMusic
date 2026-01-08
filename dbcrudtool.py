import base64
import os
import ast

def string_to_base64(input_string):
    byte_data = input_string.encode('utf-8')
    base64_encoded = base64.b64encode(byte_data)
    return base64_encoded.decode('utf-8')

def base64_to_string(base64_string):
    byte_data = base64.b64decode(base64_string)
    original_string = byte_data.decode('utf-8')

    return original_string

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


if __name__ == '__main__':
    add('main','adfdfkvnadkofgmqe')