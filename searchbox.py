from PyQt5.QtWidgets import (QMainWindow, QApplication, QVBoxLayout,
                             QLineEdit, QPushButton, QHBoxLayout, QWidget,
                             QLabel, QListWidget, QListWidgetItem)
from PyQt5.QtGui import QPalette, QColor
import sys
import threading
from climber import *

COLOR_MODE = 'DARK'
ORIGIN_SEARCH_PURPOSE = 'all for love'

class SearchBox(QMainWindow):
    def __init__(self):
        super().__init__()

        self.input_text = ORIGIN_SEARCH_PURPOSE
        self.button_list = []
        self.download_url = ''

        self.initUI()
        self.init_layout()
        self.init_CSS()
        self.show()
        self.search()

    def initUI(self):
        print('initUI')
        # 设置窗口标题和大小和最小大小
        self.setWindowTitle('搜索歌曲')
        self.setGeometry(0, 0, 1000, 1400)
        self.setMinimumSize(1000, 1400)
        # 设置主窗口背景色
        palette = QPalette()
        if COLOR_MODE == 'LIGHT':
            palette.setColor(QPalette.Window, QColor(255, 255, 255))  # 浅色背景
        else:
            palette.setColor(QPalette.Window, QColor(43,45,48))  # 深色背景
        self.setPalette(palette)
        # 窗口居中
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

        # 输入框
        self.inputbox = QLineEdit(self)
        self.inputbox.setFixedSize(780,80)
        self.inputbox.setPlaceholderText('输入歌曲名...')
        self.inputbox.setText(self.input_text)

        # 搜索按钮
        self.search_button = QPushButton('搜索',self)
        self.search_button.setFixedSize(180,80)
        self.search_button.clicked.connect(self.search)

        # 状态栏
        self.condition_label = QLabel('',self)
        self.condition_label.setFixedSize(1000,80)

        # 主列表
        self.main_list = QListWidget(self)

        # 试听按钮
        self.try_button = QPushButton('试听',self)
        #self.try_button.clicked.connect()

        # 下载按钮
        self.download_button = QPushButton('下载',self)
        self.download_button.clicked.connect(self.download_mp3)

    def init_layout(self):
        print('init_layout')
        # top_layout包含搜索栏、按钮和状态栏
        self.top_layout = QVBoxLayout()

        # 搜索栏和搜索按钮
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.inputbox)
        search_layout.addWidget(self.search_button)
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
        self.top_layout.setContentsMargins(0, 20, 0, 0) # 取消边距
        self.setMenuWidget(container)

        # 安置center_layout布局(Central)
        container2 = QWidget()
        container2.setLayout(self.center_layout)
        self.center_layout.setContentsMargins(2,0,2,5)
        self.setCentralWidget(container2)

    def init_CSS(self):
        print('init_CSS')
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
                        background-color: rgb(15,17,19);
                        color: white;
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
        print('search')
        if self.main_list.currentItem() != None:
            print(self.main_list.currentRow())

        # 搜索
        self.musiclist = get_music_url_list(self.inputbox.text())

        # 处理错误
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
        print('download')
        if self.main_list.currentItem() == None:
            print('请选择要下载的歌曲')
        else:
            self.show_condition('正在获取下载链接...')
            # 启动下载线程，以避免主线程阻塞使显示栏不更新
            threading.Thread(target = self.download_thread_geturl).start()

    # 供download_mp3函数以线程调用
    def download_thread_geturl(self):
        self.download_url = get_music_download_url(self.musiclist[self.main_list.currentRow()][0])
        self.show_condition('正在下载...')
        threading.Thread(target=self.download_thread_downloud).start()

    # 供download_thread_geturl以线程调用
    def download_thread_downloud(self):
        status_code = download_music(self.download_url,self.musiclist[self.main_list.currentRow()][1])
        if status_code == 200:
            self.show_condition('下载成功')
        else:
            self.show_condition(str('下载失败，状态码：'+str(status_code)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SearchBox()
    window.show()
    sys.exit(app.exec_())