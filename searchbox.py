from PyQt5.QtWidgets import (QMainWindow, QApplication, QVBoxLayout,
                             QLineEdit, QPushButton, QHBoxLayout, QWidget)
from PyQt5.QtGui import QPalette, QColor
import sys
from climber import *

COLOR_MODE = 'DARK'

class SearchBox(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.init_layout()
        self.init_CSS()


    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('搜索歌曲')
        self.setGeometry(0, 0, 1000, 1400)
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
        self.inputbox.setFixedSize(800,80)

        # 搜索按钮
        self.search_button = QPushButton(self)
        self.search_button.setFixedSize(200,80)


    def init_layout(self):
        self.main_layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.inputbox)
        search_layout.addWidget(self.search_button)
        self.main_layout.addLayout(search_layout)

        container = QWidget()  # 创建容器
        container.setLayout(self.main_layout)  # 把主布局添加到容器中
        self.setCentralWidget(container)  # 设置窗口的中心部件为容器

    def init_CSS(self):
        self.inputbox.setStyleSheet('')

    def run_climber(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SearchBox()
    window.show()
    sys.exit(app.exec_())