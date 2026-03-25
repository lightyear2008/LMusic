from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QLabel,
                             QLineEdit, QScrollArea, QSlider)
import sys
import os
import configparser

current_directory = os.path.dirname(os.path.abspath(__file__))
external_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(external_directory)

from searchbox import SearchBox
from dbcrudtool2 import check

class now_playing_list:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.current_list_name = config['now_playing_message']['now_list']
        self.current_list = list(check(str(self.current_list_name).split("'")[1]).keys())

    def npl_initUI(self):
        self.top_label = QLabel(self.current_list_name.split("'")[1])
        self.switch_button = QPushButton('切换')

        self.scroll_area = QScrollArea()
        self.scroll_area.setFixedHeight(500)
        self.scroll_list = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_list)
        # add something...
        for n in self.current_list:
            l = QLabel(n)
            l.setStyleSheet('QLabel {color:lightblue;}')
            self.scroll_layout.addWidget(l)
        # end
        self.scroll_list.adjustSize()
        self.scroll_area.setWidget(self.scroll_list)

    def npl_init_layout(self):
        self.npl_container = QWidget()  # 给它写CSS
        main_layout = QVBoxLayout(self.npl_container)

        # 1('当前列表名'标签 切换列表按钮)的横向布局
        top_layout = QHBoxLayout()
        # 1.1'当前列表名'标签
        top_layout.addWidget(self.top_label)
        # 1.2切换列表按钮
        top_layout.addWidget(self.switch_button)
        main_layout.addLayout(top_layout)

        # 2可滚动列表
        main_layout.addWidget(self.scroll_area)

    def npl_init_CSS_dark(self):
        self.top_label.setStyleSheet('''
                QLabel {
                    color: red;
                    font-size: 35px;
                }
                ''')
        self.switch_button.setStyleSheet('''
                QPushButton {
                    background-color: blue;
                    color: white;
                    border: 1px solid white;
                    border-radius: 10px;
                    font-size: 25px;
                    min_height: 80px;
                }
                QPushButton:hover {
                    background-color: #5DADE2;
                }
                ''')

    def update(self):
        self.npl_initUI()
        self.npl_init_layout()
        self.npl_init_CSS_dark()


class Main_Page(now_playing_list):
    def __init__(self):
        super().__init__()

    def initUI_main(self):
        self.searchbox = QLineEdit()

        self.search_button = QPushButton('搜索')
        self.search_button.clicked.connect(self.search)

        now_playing_list.npl_initUI(self)

        self.tiny_player_button = QPushButton('打开微型播放器')

        # 音量条
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)  # 设置最小值
        self.volume_slider.setMaximum(100)  # 设置最大值
        self.volume_slider.setValue(80)  # 设置默认值
        self.volume_slider.setTickInterval(100)  # 设置刻度间隔
        self.volume_slider.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置

    def init_layout_main(self):
        # 主布局(竖方向)
        self.page_main = QVBoxLayout()
        self.page_main.setAlignment(Qt.AlignTop)  # 将元素全部靠顶部对齐
        self.page_main.addSpacing(25)  # 设置竖直方向间距

        # 1.搜索栏和搜索按钮
        search_layout = QHBoxLayout()
        search_layout.addSpacing(20)
        search_layout.addWidget(self.searchbox,stretch=4)
        search_layout.addWidget(self.search_button,stretch=1)
        search_layout.addSpacing(20)
        self.page_main.addLayout(search_layout)

        # 2.主布局第二行横向布局,包括(当前播放列表 主页播放器 (打开微型播放器 音量)竖直布局)
        self.second_layout = QHBoxLayout()
        self.second_layout.setSpacing(15)
        def set_second_layout():
            now_playing_list.npl_init_layout(self)
            self.second_layout.addWidget(self.npl_container,stretch=1)

            #2.2 主页播放器
            self.musicplayer_container = QWidget()
            self.musicplayer_layout = QHBoxLayout(self.musicplayer_container)
            def set_musicplayer():
                pass
            set_musicplayer()
            self.second_layout.addWidget(self.musicplayer_container,stretch=1)

            #2.3 (打开微型播放器 音量)竖直布局
            self.open_button_and_volume_layout = QVBoxLayout()
            def set_open_button_and_volume_layout():
                # 打开微型播放器按钮
                self.open_button_and_volume_layout.addWidget(self.tiny_player_button)
                # 音量条
                self.open_button_and_volume_layout.addWidget(self.volume_slider)
            set_open_button_and_volume_layout()
            self.second_layout.addLayout(self.open_button_and_volume_layout,stretch=1)
        set_second_layout()
        self.page_main.addSpacing(30)
        self.page_main.addLayout(self.second_layout,stretch=3)

        #3.主布局第三行横向布局,包括(主歌单 自建歌单横向滚动列表)
        self.third_layout = QHBoxLayout()
        self.third_layout.setSpacing(15)
        def set_third_layout():
            #3.1 主歌单
            pass

            #3.2 自建歌单横向滚动列表
            pass
        set_third_layout()
        self.page_main.addSpacing(30)
        self.page_main.addLayout(self.third_layout,stretch=2)

    def search(self):
        # 这里之前用的线程,跑不了,显示'进程已结束，退出代码为 -1073741819 (0xC0000005)'
        self.search_window = SearchBox(self.searchbox.text())
        self.search_window.show()
        #self.search_window.destroyed.connect(lambda :print('search_window已关闭'))
        now_playing_list.update(self)

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


        self.npl_container.setStyleSheet('''
                QWidget {
                    border-radius: 15px;
                    background: #000000;
                }
                ''')
        now_playing_list.npl_init_CSS_dark(self)

        self.musicplayer_container.setStyleSheet('''
                QWidget {
                    border-radius: 15px;
                    background: #000000;
                }
                ''')