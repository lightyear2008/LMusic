import requests
from bs4 import BeautifulSoup

url = 'https://www.gequbao.com/s/all%20for%20love'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

response = requests.get(url,verify = False,headers = headers)

soup = BeautifulSoup(response.text,'html.parser')

music_list = soup.find(class_='card-text').find_all('div', class_='row') #找到所有歌曲的div标签
music_list = music_list[1:] #第一个元素不包含歌曲，切掉

# 二次处理，得到歌曲的url列表
url_list = []
for n in range(len(music_list)):
    url_list.append('https://www.gequbao.com/' + str(music_list[n])[str(music_list[n]).find('href') + 6:].split('"')[0])

print(url_list)

response2 = requests.get(url_list[2],verify = False,headers = headers)
soup2 = BeautifulSoup(response2.text,'html.parser')
print(soup2)



# 处理动态网页
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options

edge_options = Options()
edge_options.add_argument("--headless")

driver = webdriver.Edge(service=Service(os.path.join(os.path.dirname(os.path.abspath(__file__)),'drivers','msedgedriver.exe')))
driver.get('https://www.gequbao.com/music/34427')

def click_button(driver, type, value):# 自动点击按钮
    try:
        #根据type和value确定元素定位器
        if type.lower() == 'id':
            element_locator = (By.ID, value)
        elif type.lower() == 'class_name':
            element_locator = (By.CLASS_NAME, value)
        elif type.lower() == 'xpath':
            element_locator = (By.XPATH, value)
        else:
            raise ValueError("Unsupported element locator type. Use 'id', 'class_name' or 'xpath'.")
        # 等待元素可点击
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(element_locator))
        # 查找并点击元素
        element = driver.find_element(*element_locator)#解包元素定位器并查找元素
        ActionChains(driver).click(element).perform()#执行点击操作
    except Exception as e:
        print('异常:', '\n',e)

click_button(driver,'id','btn-download-mp3')
import time
time.sleep(20)# 问题在这里，href不加载，空的
page_html = driver.page_source


# 测试用
with open('return_text.txt','w',encoding='utf-8') as f:
    for url in url_list:
        f.write(url+'\n')
    f.write(str(page_html))





'''
#试一下怎么下载   OK成功了,现在只需要找到URL
#AI给的逐块下载
import requests

# MP3 文件的 URL
mp3_url = 'https://lx-sycdn.kuwo.cn/446af18fd4e9a826585d6630827f5546/693ce904/resource/n3/28/25/3173429631.mp3?bitrate$128&from=vip'

# 发送 HTTP GET 请求下载 MP3 文件
response = requests.get(mp3_url, stream=True, verify=False)

# 检查请求是否成功
if response.status_code == 200:
    # 打开文件以二进制写入模式保存 MP3 文件
    with open('All For Love (LÜ Remix)-TUNGEVAAG&Raaban.mp3', 'wb') as file:
        # 写入下载的文件内容
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print("MP3 文件下载成功并保存为 All For Love (LÜ Remix)-TUNGEVAAG&Raaban.mp3")
else:
    print("无法下载 MP3 文件，状态码：", response.status_code)
'''