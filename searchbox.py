from PyQt5.QtWidgets import (QMainWindow, QApplication, QVBoxLayout,
                             QLineEdit, QPushButton, QHBoxLayout, QWidget,
                             QLabel, QListWidget, QListWidgetItem)
from PyQt5.QtGui import QPalette, QColor
import sys
from climber import *

COLOR_MODE = 'DARK'
ORIGIN_SEARCH_PURPOSE = 'Run Free'

class SearchBox(QMainWindow):
    def __init__(self):
        super().__init__()

        self.input_text = ORIGIN_SEARCH_PURPOSE
        self.button_list = []

        self.initUI()
        self.init_layout()
        self.init_CSS()
        self.show()
        self.show_condition()

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
        self.search_button.clicked.connect(self.show_condition)

        # 状态栏
        self.condition_label = QLabel('',self)
        self.condition_label.setFixedSize(1000,80)

        # 主列表
        self.main_list = QListWidget(self)

    def init_layout(self):
        print('init_layout')
        self.top_layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.inputbox)
        search_layout.addWidget(self.search_button)
        self.top_layout.addLayout(search_layout)

        condition_layout = QVBoxLayout()
        condition_layout.addWidget(self.condition_label)
        self.top_layout.addLayout(condition_layout)

        container = QWidget()  # 创建容器
        container.setLayout(self.top_layout)
        self.top_layout.setContentsMargins(0, 20, 0, 0) # 取消边距
        self.setMenuWidget(container)

        self.setCentralWidget(self.main_list)

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
                        background-color: rgb(15,17,19)
                        color: white;
                    }
                    ''')

    def show_condition(self):# 查找歌曲
        print('show_condition')
        self.musiclist = get_music_url_list(self.inputbox.text())

        self.main_list.clear()
        for n in range(len(self.musiclist)):
            text = self.musiclist[n][1] + '\n               ——' + self.musiclist[n][2]
            item = QListWidgetItem(text,self.main_list)
            

        print(self.musiclist)
        self.condition_label.setText(f'已找到 {len(self.musiclist)} 条内容')

    def run_climber(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SearchBox()
    window.show()
    sys.exit(app.exec_())