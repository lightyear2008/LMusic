import requests
from bs4 import BeautifulSoup
import os
import time
import logging
import configparser
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options

# 初始化日志记录器
log_format = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'
logging.basicConfig(
    filename='logs/log.log',
    level=logging.WARNING,
    format=log_format,
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
config = configparser.ConfigParser()
config.read('config.ini')
if config['main']['VERIFY'] == 'False':
    verify = False #  关闭证书验证，解决Win10的SSL过期问题
else:
    verify = True

def get_music_url_list(name): # 因网站更新已重写 最后更改日期2026-3-4
    # 替换歌曲名中的空格为%20
    if ' ' in name:
        name = name.replace(' ','%20')

    # 发送请求
    url = 'https://www.gequbao.com/s/' + name
    response = requests.get(url,verify = verify,headers = headers)

    # 处理错误
    if response.status_code == 503:
        error_message = '服务器已关闭或正在维护中，错误码：503'
        logging.error(error_message)
        return error_message
    elif response.status_code == 502:
        error_message = '网关错误，错误码：502'
        logging.error(error_message)
        return error_message
    elif response.status_code == 500:
        error_message = '服务端错误，错误码：500'
        logging.error(error_message)
        return error_message
    elif response.status_code == 404:
        error_message = '找不到网页，错误码：404'
        logging.error(error_message)
        return error_message
    elif response.status_code == 403:
        error_message = '服务端拒绝请求，错误码：403'
        logging.error(error_message)
        return error_message
    elif response.status_code != 200:
        logging.warning(f'可能的错误：HTTP{response.status_code}')

    soup = BeautifulSoup(response.text,'html.parser')

    music_list = soup.find(class_='card-text').find_all('div', class_='row')  # 找到所有歌曲的div标签
    music_list = music_list[1:]  # 第一个元素不包含歌曲，切掉

    # 二次处理，得到歌曲的url列表
    url_list = []
    for n in range(len(music_list)):
        inside_list = []

        # 获取URL
        music_item = music_list[n] # 这是一个HTML标签，包含了歌曲的所有信息
        href_start = str(music_item).find('href') + 6 # URL后半部分开始位置索引
        href = str(music_item)[href_start:].split('"')[0]
        full_url = 'https://www.gequbao.com' + href
        inside_list.append(full_url)

        # 获取歌名(删除换行符和前后的空格)
        music_name = music_list[n].find_all('span', class_='text-primary font-weight-bold h6 mb-0 text-truncate')[0].get_text()
        while music_name[0] == ' ' or music_name[0] == '\n':
            music_name = music_name[1:]
        while music_name[-1] == ' ' or music_name[-1] == '\n':
            music_name = music_name[:-1]
        inside_list.append(music_name)

        # 处理作者名(删除换行符和前后的空格)
        author = music_list[n].find('small').get_text().replace('\n','')
        while author[0] == ' ':
            author = author[1:]
        while author[-1] == ' ':
            author = author[:-1]
        inside_list.append(author)
        url_list.append(inside_list)
    return url_list

def get_music_download_url(url): # 因网站更新已重写 最后更改日期2026-3-6
    print('get_music_download_url')
    #  设置无头模式和User-Agent
    edge_options = Options()
    edge_options.add_argument("--headless")
    edge_options.add_argument(f"user-agent={headers['User-Agent']}")

    # 启动浏览器并发送请求
    driver = webdriver.Edge(
            service=Service(os.path.join(os.path.dirname(os.path.abspath(__file__)),'drivers','msedgedriver.exe')),
            options=edge_options
            )
    driver.get(url)
    print('get')

    # 等待按钮可点击
    try:
        WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,'btn-download-mp3')))
    except TimeoutError:
        logging.error('get_music_download_url中等待按钮点击超时')
        print('等待按钮点击超时')
        driver.quit()
        return 'url获取失败'

    # 点击按钮
    driver.find_element(By.ID,'btn-download-mp3').click()
    print('click')
    time.sleep(3)

    fail_times = 0
    while True:
        try:
            # 获得HTML并解析
            page_html = driver.page_source
            soup = BeautifulSoup(page_html, 'html.parser')
            # 尝试寻找按钮,找不到会抛出AttributeError异常并进行下一次循环
            purpose_url = soup.find(class_='download-option-card default-link').get('href')
            # 运行到此则成功获取URL
            driver.quit()
            return purpose_url
        except AttributeError:
            fail_times += 1
            print(f'fail for {fail_times} times')
            # 处理超时
            if fail_times >= 40:
                logging.error('get_music_download_url中url获取超时')
                driver.quit()
                return 'url获取失败'
            time.sleep(1)
            continue
        except Exception as e:
            logging.error(f'get_music_download_url中发生未知错误: {e},重试次数{fail_times}次')
            driver.quit()
            return 'url获取失败'

def download_music(download_url,file_path): # 网站更新未影响该函数正常工作
    # 发送 GET 请求下载 MP3 文件
    response = requests.get(download_url, stream=True, verify=verify,headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        # 打开文件以二进制写入模式保存 MP3 文件
        with open(file_path + '.mp3', 'wb') as file:
            # 写入下载的文件内容
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print('MP3 文件下载成功')
        return 200
    else:
        error_message = '无法下载 MP3 文件,状态码:', response.status_code
        print(error_message)
        logging.warning(error_message)
        return response.status_code