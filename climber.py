import requests
from bs4 import BeautifulSoup
import os
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
verify = False #  关闭证书验证，解决Win10的SSL过期问题

def get_music_url_list(name):
    # 替换歌曲名中的空格为%20
    if ' ' in name:
        name = name.replace(' ','%20')
    url = 'https://www.gequbao.com/s/' + name

    response = requests.get(url,verify = verify,headers = headers)
    soup = BeautifulSoup(response.text,'html.parser')

    music_list = soup.find(class_='card-text').find_all('div', class_='row')  # 找到所有歌曲的div标签
    music_list = music_list[1:]  # 第一个元素不包含歌曲，切掉

    # 二次处理，得到歌曲的url列表
    url_list = []
    for n in range(len(music_list)):
        url_list.append('https://www.gequbao.com/' + str(music_list[n])[str(music_list[n]).find('href') + 6:].split('"')[0])

    return url_list

def get_music_download_url(url):
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
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,'btn-download-mp3')))
    time.sleep(2) #  不加href就是空的
    print('sleeped')

    # 点击按钮
    driver.find_element(By.ID,'btn-download-mp3').click()
    print('click')

    # 获得HTML并解析
    page_html = driver.page_source
    soup = BeautifulSoup(page_html,'html.parser')

    # 确保返回值不为空
    for n in range(3):
        if soup.find(class_='default-link').get('href') == '':
            print('retry')
            driver.get(url)
            time.sleep(3)
            page_html = driver.page_source
            soup = BeautifulSoup(page_html, 'html.parser')
    if soup.find(class_='default-link').get('href') == '':
        return 'url获取失败'

    return soup.find(class_='default-link').get('href')

def download_music(download_url,file_path):
    # 发送 GET 请求下载 MP3 文件
    response = requests.get(download_url, stream=True, verify=verify)

    # 检查请求是否成功
    if response.status_code == 200:
        # 打开文件以二进制写入模式保存 MP3 文件
        with open(file_path + '.mp3', 'wb') as file:
            # 写入下载的文件内容
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("MP3 文件下载成功")
    else:
        print("无法下载 MP3 文件，状态码：", response.status_code)
