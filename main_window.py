# Copyright (c) 2026 lightyear2008
# SPDX-License-Identifier: MIT
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QApplication, QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QLabel)
from PyQt5.QtGui import QPalette, QColor, QPixmap, QIcon
import sys
import os
from pages.main_page import Main_Page

COLOR_MODE = 'DARK'

class ranking_page:
    def __init__(self):
        pass

    def initUI_ranking(self):
        self.button = QPushButton('这是第二页')

    def init_layout_ranking(self):
        # 主布局(竖方向)
        self.page_ranking = QVBoxLayout()
        self.page_ranking.setAlignment(Qt.AlignTop)  # 将元素全部靠顶部对齐
        self.page_ranking.addSpacing(20)  # 设置竖直方向的间距为10

        self.page_ranking.addWidget(self.button)

    def init_CSS_DARK_ranking(self):
        pass


class MainWindow(QMainWindow,Main_Page,ranking_page):
    def __init__(self):
        self.page = 'main_page'

        super().__init__()
        self.initUI()
        self.init_main_layout()
        self.init_CSS_DARK()

    def update_UI_to_main_page(self):
        self.page = 'main_page'
        Main_Page.__init__(self)
        self.initUI()
        self.init_main_layout()
        self.init_CSS_DARK()

    def update_UI_to_ranking_page(self):
        self.page = 'ranking_page'
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
        self.logo.setMaximumHeight(150)  #最大高度
        self.logo.setScaledContents(True)  #图片填充

        self.main_page_button = QPushButton('主页')
        self.main_page_button.setIcon(QIcon(os.path.join('images','main_page.jpg')))  # 设置图标
        self.main_page_button.clicked.connect(self.update_UI_to_main_page)

        self.ranking_page_button = QPushButton('排名')
        self.ranking_page_button.clicked.connect(self.update_UI_to_ranking_page)

        self.musicsquare_page_button = QPushButton('广场')

        self.stargame_page_button = QPushButton('星')

        self.config_page_button = QPushButton('设置')


        # 右侧主页面(继承)
        if self.page == 'main_page':
            Main_Page.initUI_main(self)
        elif self.page == 'ranking_page':
            ranking_page.initUI_ranking(self)

    def init_main_layout(self):
        # 主布局,包括左侧菜单栏和右侧页面
        main_layout = QHBoxLayout()

        # 左侧菜单栏,包括上部的logo和下面的页面切换按钮列表
        left_button_layout = QVBoxLayout()
        left_button_layout.setSpacing(0)
        left_button_layout.addWidget(self.logo,stretch=1)
        left_button_layout.addWidget(self.main_page_button,stretch=1)
        left_button_layout.addWidget(self.ranking_page_button,stretch=1)
        left_button_layout.addWidget(self.musicsquare_page_button,stretch=1)
        left_button_layout.addWidget(self.stargame_page_button,stretch=1)
        left_button_layout.addWidget(self.config_page_button,stretch=1)
        left_button_layout.setAlignment(Qt.AlignTop)  #将元素全部靠顶部对齐
        main_layout.addLayout(left_button_layout,stretch=1)

        # 右侧主界面(继承)
        if self.page == 'main_page':
            Main_Page.init_layout_main(self)
            main_layout.addLayout(self.page_main,stretch=10)
        elif self.page == 'ranking_page':
            ranking_page.init_layout_ranking(self)
            main_layout.addLayout(self.page_ranking,stretch=10)

        # 安置主布局
        container = QWidget()
        container.setLayout(main_layout)
        main_layout.setContentsMargins(0,0,0,0)
        self.setCentralWidget(container)

    def init_CSS_DARK(self):
        self.main_page_button.setStyleSheet('''
                QPushButton {
                    border: none;
                    border-bottom: 1px solid blue;
                    background-color: #1F1F1F;
                    min-height: 120px;
                    color: white;
                    font-size: 35px;
                    font-family: Courier New;
                }
                ''')
        self.ranking_page_button.setStyleSheet('''
                QPushButton {
                    border: none;
                    border-bottom: 1px solid blue;
                    background-color: #1F1F1F;
                    min-height: 120px;
                    color: white;
                    font-size: 35px;
                    font-family: Courier New;
                }
                ''')
        self.musicsquare_page_button.setStyleSheet('''
                QPushButton {
                    border: none;
                    border-bottom: 1px solid blue;
                    background-color: #1F1F1F;
                    min-height: 120px;
                    color: white;
                    font-size: 35px;
                    font-family: Courier New;
                }
                ''')
        self.stargame_page_button.setStyleSheet('''
                QPushButton {
                    border: none;
                    border-bottom: 1px solid blue;
                    background-color: #1F1F1F;
                    min-height: 120px;
                    color: white;
                    font-size: 35px;
                    font-family: Courier New;
                }
                ''')
        self.config_page_button.setStyleSheet('''
                QPushButton {
                    border: none;
                    background-color: #1F1F1F;
                    min-height: 120px;
                    color: white;
                    font-size: 35px;
                    font-family: Courier New;
                }
                ''')

        # 右侧主页面(继承)
        if self.page == 'main_page':
            Main_Page.init_CSS_DARK_main(self)
        elif self.page == 'ranking_page':
            ranking_page.init_CSS_DARK_ranking(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())