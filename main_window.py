from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QApplication, QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QLabel,
                             QLineEdit, QScrollArea, QSlider)
from PyQt5.QtGui import QPalette, QColor, QPixmap, QIcon
import sys
import os
from searchbox import SearchBox

COLOR_MODE = 'DARK'

class main_page:
    def __init__(self):
        pass

    def initUI_main(self):
        self.searchbox = QLineEdit()

        self.search_button = QPushButton('搜索')
        self.search_button.clicked.connect(self.search)

        self.now_playing_list_inner_top_label = QLabel('list_name')
        self.now_playing_list_inner_switch_button = QPushButton('切换')
        self.now_playing_list_inner_scroll_area = QScrollArea()

        self.tiny_player_button = QPushButton('打开微型播放器')

        # 音量条
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)  # 设置最小值
        self.volume_slider.setMaximum(100)  # 设置最大值
        self.volume_slider.setValue(50)  # 设置默认值
        self.volume_slider.setTickInterval(10)  # 设置刻度间隔
        self.volume_slider.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置

    def init_layout_main(self):
        # 主布局(竖方向)
        self.page_main = QVBoxLayout()
        self.page_main.setAlignment(Qt.AlignTop)  # 将元素全部靠顶部对齐
        self.page_main.addSpacing(25)  # 设置竖直方向间距

        # 1.搜索栏和搜索按钮
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.searchbox,stretch=4)
        search_layout.addWidget(self.search_button,stretch=1)
        self.page_main.addLayout(search_layout)

        # 2.主布局第二行横向布局,包括(当前播放列表 主页播放器 (打开微型播放器 音量)竖直布局)
        self.second_layout = QHBoxLayout()
        def set_second_layout():
            # 2.1当前播放列表
            self.now_playing_list_container = QWidget() # 给它写CSS
            self.now_playing_list_layout = QHBoxLayout(self.now_playing_list_container)
            def set_now_playing_list():
                # 2.1.1('当前列表名'标签和切换列表按钮)的横向布局
                now_playing_list_inner_top_layout = QHBoxLayout()
                def set_top_layout():
                    # 2.1.1.1'当前列表名'标签
                    now_playing_list_inner_top_layout.addWidget(self.now_playing_list_inner_top_label)
                    # 2.1.1.2切换列表按钮
                    now_playing_list_inner_top_layout.addWidget(self.now_playing_list_inner_switch_button)
                set_top_layout()
                self.now_playing_list_layout.addLayout(now_playing_list_inner_top_layout)# 2.1.1结束

                # 2.1.2不定长播放列表
                # 滚动区域内容
                self.now_playing_list_inner_scroll_area_container = QWidget()
                scroll_layout = QVBoxLayout(self.now_playing_list_inner_scroll_area_container)

                def set_scroll_layout():
                    label = QLabel('标签1')
                    label.setStyleSheet('color: red;')
                    scroll_layout.addWidget(label)
                set_scroll_layout()

                self.now_playing_list_inner_scroll_area.setWidget(self.now_playing_list_inner_scroll_area_container)
                self.now_playing_list_layout.addWidget(self.now_playing_list_inner_scroll_area)
            set_now_playing_list()
            self.second_layout.addWidget(self.now_playing_list_container)

            #2.2 主页播放器
            self.musicplayer_container = QWidget()
            self.musicplayer_layout = QHBoxLayout(self.musicplayer_container)
            def set_musicplayer():
                pass
            set_musicplayer()
            self.second_layout.addWidget(self.musicplayer_container)

            #2.3 (打开微型播放器 音量)竖直布局
            self.open_button_and_volume_layout = QVBoxLayout()
            def set_open_button_and_volume_layout():
                # 打开微型播放器按钮
                self.open_button_and_volume_layout.addWidget(self.tiny_player_button)
                # 音量条
                self.open_button_and_volume_layout.addWidget(self.volume_slider)
            set_open_button_and_volume_layout()
            self.second_layout.addLayout(self.open_button_and_volume_layout)
        set_second_layout()
        self.page_main.addLayout(self.second_layout)

    def search(self):
        # 这里之前用的线程,跑不了,显示'进程已结束，退出代码为 -1073741819 (0xC0000005)'
        self.search_window = SearchBox(self.searchbox.text())
        self.search_window.show()

    def init_CSS_DARK_main(self):
        self.searchbox.setStyleSheet('''
                QLineEdit {
                    background-color: #D0D2D4;
                    min-height: 80px;
                    border-radius: 40px;
                    font-size: 45px;
                    color: #239B56;
                }
                QLineEdit:focus {
                    border: 6px solid;
                    border-color: qradialgradient(cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 #66B2FF, stop:1 #0056FF);
                }
                ''')
        self.search_button.setStyleSheet('''
                QPushButton {
                        background-color: #3574F0;
                        border: none;
                        border-radius: 40px;
                        font-weight: bold;
                        color: white;
                        min-height: 80px;
                    }
                    QPushButton:pressed {
                        background-color: #4584FF;
                        border: 5px inset #4584FF;
                    }
                ''')

        
        self.now_playing_list_container.setStyleSheet('''
                QWidget {
                    border-radius: 10px;
                    background: #000000;
                }
                ''')
        self.now_playing_list_inner_top_label.setStyleSheet('''
                QLabel {
                    color: white;
                }
                ''')
        self.now_playing_list_inner_switch_button.setStyleSheet('''
                QPushButton {
                    background: #AAAAAA;
                }
                ''')

        self.musicplayer_container.setStyleSheet('''
                QWidget {
                    border-radius: 10px;
                    background: #000000;
                }
                ''')

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


class MainWindow(QMainWindow,main_page,ranking_page):
    def __init__(self):
        self.page = 'main_page'

        super().__init__()
        self.initUI()
        self.init_main_layout()
        self.init_CSS_DARK()

    def update_UI_to_main_page(self):
        self.page = 'main_page'
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
            main_page.initUI_main(self)
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
            main_page.init_layout_main(self)
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
            main_page.init_CSS_DARK_main(self)
        elif self.page == 'ranking_page':
            ranking_page.init_CSS_DARK_ranking(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

