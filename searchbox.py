# Copyright (c) 2026 lightyear2008
# SPDX-License-Identifier: MIT
from PyQt5.QtWidgets import (QMainWindow, QApplication, QVBoxLayout,
                             QLineEdit, QPushButton, QHBoxLayout, QWidget,
                             QLabel, QListWidget, QListWidgetItem)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
import sys
import os
import threading
import configparser
import playsound3
from climber import *
from dbcrudtool2 import add


class SearchBox(QMainWindow,):
    def __init__(self,ORIGIN_SEARCH_PURPOSE):
        super().__init__()

        self.input_text = ORIGIN_SEARCH_PURPOSE
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.COLOR_MODE = config['main']['COLOR_MODE']
        self.button_list = []
        self.download_url = ''
        self.sound = None
        self.setAttribute(Qt.WA_DeleteOnClose) # 关闭窗口时自动删除C++对象

        self.initUI()
        self.init_layout()
        self.init_CSS()
        self.show()
        # 首次搜索
        self.show_condition('正在搜索...')
        def first_search_thread():
            time.sleep(0.2) # 我真的不理解... 为啥加这个就好了
            self.search()
        threading.Thread(target=first_search_thread).start()

    def initUI(self):
        # 设置窗口标题和大小和最小大小(在开发机上这个大小对应1400*1000)
        self.setWindowTitle('搜索歌曲')
        screen = QApplication.desktop().screenGeometry()
        self.setGeometry(0, 0, screen.width() // 3, int(screen.height() * 0.7))
        self.setMinimumSize(screen.width() // 3, int(screen.height() * 0.7))
        # 设置主窗口背景色
        palette = QPalette()
        if self.COLOR_MODE == 'LIGHT':
            palette.setColor(QPalette.Window, QColor(255, 255, 255))  # 浅色背景
        else:
            palette.setColor(QPalette.Window, QColor(43,45,48))  # 深色背景
        self.setPalette(palette)
        # 窗口居中
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

        # 输入框
        self.inputbox = QLineEdit(self)
        self.inputbox.setFixedHeight(int(0.0572 * size.height())) # 开发机上此高度为80
        self.inputbox.setPlaceholderText('输入歌曲名...')
        self.inputbox.setText(self.input_text)
        self.inputbox.returnPressed.connect(lambda :self.search_button.click()) # 回车触发点击事件

        # 搜索按钮
        self.search_button = QPushButton('搜索',self)
        self.search_button.setFixedHeight(int(0.0572 * size.height()))
        self.search_button.clicked.connect(self.search)

        # 状态栏
        self.condition_label = QLabel('',self)
        self.condition_label.setFixedSize(size.width(),int(0.0572 * size.height()))

        # 主列表
        self.main_list = QListWidget(self)
        self.main_list.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.main_list.verticalScrollBar().setSingleStep(4)

        # 试听按钮
        self.try_button = QPushButton('试听',self)
        self.try_button.clicked.connect(self.try_music)

        # 下载按钮
        self.download_button = QPushButton('下载',self)
        self.download_button.clicked.connect(self.download_mp3)

    def init_layout(self):
        # top_layout包含搜索栏、按钮和状态栏
        self.top_layout = QVBoxLayout()

        # 搜索栏和搜索按钮
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.inputbox,stretch=39)
        search_layout.addWidget(self.search_button,stretch=9)
        self.top_layout.addLayout(search_layout)

        # 状态栏
        condition_layout = QVBoxLayout()
        condition_layout.addWidget(self.condition_label)
        self.top_layout.addLayout(condition_layout)

        # center_layout包括主列表、试听和下载按钮
        self.center_layout = QVBoxLayout()

        # 主列表
        self.center_layout.addWidget(self.main_list)

        # 试听和下载按钮
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.try_button,stretch=1)
        bottom_layout.addWidget(self.download_button,stretch=1)
        self.center_layout.addLayout(bottom_layout)

        # 安置top_layout布局(Menu)
        container = QWidget()
        container.setLayout(self.top_layout)
        self.top_layout.setContentsMargins(0,int(self.geometry().height()*0.0143), 0, 0) # 取消边距
        self.setMenuWidget(container)

        # 安置center_layout布局(Central)
        container2 = QWidget()
        container2.setLayout(self.center_layout)
        self.center_layout.setContentsMargins(2,0,2,5)
        self.setCentralWidget(container2)

    def init_CSS(self):
        self.inputbox.setStyleSheet('''
                    QLineEdit {
                        background-color: rgb(43,45,48); 
                        border: 2px solid #ECF0F1; 
                        border-radius: 15px; 
                        font-size: 40px;
                        font-weight: bold;
                        color: white;
                    }
                    QLineEdit:focus {
                        border: 5px outset #3498DB;
                    }
                    ''')
        self.search_button.setStyleSheet('''
                    QPushButton {
                        background-color: #3574F0;
                        border: none;
                        border-radius: 15px;
                        font-weight: bold;
                        color: white;  
                    }
                    QPushButton:pressed {
                        background-color: #4584FF;
                        border: 5px inset #4584FF;
                    }
                    ''')
        self.condition_label.setStyleSheet('''
                    QLabel {
                        background-color: rgb(35,37,39);
                        color: white;
                    }
                    ''')
        self.main_list.setStyleSheet('''
                    QListWidget {
                        background-color: rgb(15, 17, 19);
                        color: white;
                        border: none;
                        outline: none;
                    }
                    QListWidget QScrollBar:horizontal {
                        height: 0px;
                        background: transparent;
                    }
                    QListWidget QScrollBar:vertical {
                        background: #1a1a1a;
                        width: 16px;
                        margin: 0px;
                        border-radius: 6px;
                    }
                    QListWidget QScrollBar::handle:vertical {
                        background: #3a3a3a;
                        min-height: 30px;
                        border-radius: 4px;
                    }
                    QListWidget QScrollBar::handle:vertical:hover {
                        background: #4a4a4a;
                    }
                    QListWidget QScrollBar::handle:vertical:pressed {
                        background: #555555;
                    }
                    QListWidget QScrollBar::sub-line:vertical,
                    QListWidget QScrollBar::add-line:vertical {
                        height: 0px;
                        border: none;
                    }
                    QListWidget QScrollBar::up-arrow:vertical,
                    QListWidget QScrollBar::down-arrow:vertical {
                        height: 0px;
                        width: 0px;
                        border: none;
                    }
                    QListWidget QScrollBar::add-page:vertical,
                    QListWidget QScrollBar::sub-page:vertical {
                        background: none;
                    }
                    QListWidget::item:selected {
                        background-color: #3574F0;
                        color: white;
                    }
                    QListWidget::item:hover {
                        background-color: rgba(53, 116, 240, 0.2);
                        border: 1px solid white;
                        border-radius: 7px;
                        margin: 0px 0px 0px 0px;
                    }
                    ''')
        self.try_button.setStyleSheet('''
                    QPushButton {
                        min-width: 300px;
                        min-height: 80px;
                        background-color: rgb(43,45,48);
                        border: 2px solid #FFFFFF;
                        border-radius: 10px;
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: #1e1f22;
                    }
                    QPushButton:pressed {
                        border: 2px solid #3574F0;
                    }
                    ''')
        self.download_button.setStyleSheet('''
                     QPushButton {
                        min-width: 300px;
                        min-height: 80px;
                        background-color: #3574F0;
                        border: none;
                        border-radius: 10px;
                        color: white;
                    }
                    QPushButton:pressed {
                        background-color: #4584FF;
                        border: 3px inset #4584FF;
                    }
                    ''')

    # 查找歌曲并更新列表
    def search(self):
        if self.main_list.currentItem() != None:
            print(self.main_list.currentRow())

        # 验证输入框中是否有内容
        if self.inputbox.text() == '':
            self.show_condition('请输入搜索内容')
            return None

        # 搜索
        self.musiclist = get_music_url_list(self.inputbox.text())

        # 处理错误(当get_music_url_list错误会返回字符串)
        if isinstance(self.musiclist,str):
            self.show_condition(self.musiclist)
            return None

        # 显示搜索结果
        self.main_list.clear()
        for n in range(len(self.musiclist)):
            text = self.musiclist[n][1] + '\n               ——' + self.musiclist[n][2]
            item = QListWidgetItem(text,self.main_list)

        self.show_condition(f'已找到 {len(self.musiclist)} 条内容')

    # 更新状态栏
    def show_condition(self,message):
        self.condition_label.setText(message)
        self.condition_label.update()

    def download_mp3(self):
        # 两个线程函数
        def download_thread_geturl():
            self.download_url = get_music_download_url(self.musiclist[self.main_list.currentRow()][0])
            if self.download_url:
                self.show_condition('正在下载...')
                threading.Thread(target=download_thread_download).start()  # 启动下载线程
            else:
                self.show_condition('下载链接获取失败')

        def download_thread_download():
            status_code = download_music(self.download_url,os.path.join('mp3_db', 'main_list', self.musiclist[self.main_list.currentRow()][1]))
            if status_code == 200:
                self.show_condition('下载成功')
                add('main',self.musiclist[self.main_list.currentRow()][1])
            else:
                self.show_condition(str('下载失败，状态码：' + str(status_code)))

        # 开始下载操作
        if self.main_list.currentItem() is None:
            print('请选择要下载的歌曲')
        else:
            self.show_condition('正在获取下载链接...')
            # 启动下载线程，以避免主线程阻塞使显示栏不更新
            threading.Thread(target = download_thread_geturl).start()

    def try_music(self):
        if self.main_list.currentItem() is None:
            print('请选择要试听的歌曲')
            self.show_condition('请选择要试听的歌曲')
            return None

        # 清空目录
        del_path = 'try_music'
        for file in os.listdir(del_path):
            os.remove(os.path.join(del_path,file))

        download_finished_event = threading.Event() # 下载完成事件,用于两个线程通信

        # 执行下载操作(耗时)
        def download_thread():
            self.show_condition('正在下载试听文件...')
            download_url = get_music_download_url(self.musiclist[self.main_list.currentRow()][0])
            path = os.path.join('try_music', self.musiclist[self.main_list.currentRow()][1])
            if not download_url:
                self.show_condition('下载链接获取失败,请重试')
                return None
            download_music(download_url, path)
            download_finished_event.set()
        threading.Thread(target=download_thread).start()

        # 停止上一个试听
        try:
            self.sound.stop()
        except:
            pass

        # 等待下载完成并播放(线程)
        def wait_and_play_thread():
            download_finished_event.wait()
            self.show_condition('下载成功,正在试听')
            self.sound = playsound3.playsound(os.path.join('try_music', self.musiclist[self.main_list.currentRow()][1]) + '.mp3', block=False)
        thread = threading.Thread(target=wait_and_play_thread)
        thread.daemon = True  # 设置为守护线程
        thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SearchBox('天另一侧')
    window.show()
    sys.exit(app.exec())