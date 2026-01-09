from PyQt5.QtWidgets import (QMainWindow, QApplication, QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QLabel)
from PyQt5.QtGui import QPalette, QColor, QPixmap
import sys
import os

COLOR_MODE = 'DARK'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.init_main_layout()
        self.init_CSS_DARK()

    def initUI(self):
        # 主窗口的标题、宽高、居中等设置
        def init_MainWindow():
            # 设置窗口标题
            self.setWindowTitle('LMusic')

            # 获取屏幕的宽度和高度
            screen = QApplication.desktop().screenGeometry()
            screen_width = screen.width()
            screen_height = screen.height()

            # 设置窗口的宽度和高度值
            window_width = int(screen_width / 1.75)
            window_height = int(screen_height / 1.5)

            # 设置窗口大小
            self.setGeometry(0, 0, window_width, window_height)
            self.setMinimumSize(window_width, window_height)

            # 设置主窗口背景色
            palette = QPalette()
            if COLOR_MODE == 'LIGHT':
                palette.setColor(QPalette.Window, QColor(255, 255, 255))  # 浅色背景
            else:
                palette.setColor(QPalette.Window, QColor(43, 45, 48))  # 深色背景
            self.setPalette(palette)

            # 窗口居中
            screen = QApplication.desktop().screenGeometry()
            size = self.geometry()
            self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
        init_MainWindow()

        # logo和左侧按钮列表
        self.logo = QLabel('logo')
        self.logo.setPixmap(QPixmap(os.path.join('images','logo.jpg')))

        self.main_page_button = QPushButton('aaaaaaaaaa')

        self.b = QPushButton('aaa')

    def init_main_layout(self):
        # 主布局,包括左侧菜单栏和右侧页面
        main_layout = QHBoxLayout()

        # 左侧菜单栏,包括上部的logo和下面的页面切换按钮列表
        left_button_layout = QVBoxLayout()
        left_button_layout.addWidget(self.logo,stretch=1)
        left_button_layout.addWidget(self.main_page_button, stretch=1)
        main_layout.addLayout(left_button_layout,stretch=1)

        # 右侧主界面
        page_main = QVBoxLayout()
        page_main.addWidget(self.b)
        main_layout.addLayout(page_main,stretch=10)

        # 安置主布局
        container = QWidget()
        container.setLayout(main_layout)
        main_layout.setContentsMargins(0,0,0,0)
        self.setCentralWidget(container)

    def init_CSS_DARK(self):
        self.main_page_button.setStyleSheet('''
                    QPushButton {
                        background-color: rgb(100,100,100); 
                    }
                    ''')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())