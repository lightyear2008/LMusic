# Copyright (c) 2026 lightyear2008
# SPDX-License-Identifier: MIT
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import (QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QLabel,
                             QLineEdit, QScrollArea, QSlider, QDialog)
import sys
import os
import configparser

current_directory = os.path.dirname(os.path.abspath(__file__))
external_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(external_directory)

from searchbox import SearchBox
from dbcrudtool2 import check
from switch_window import SwitchListDialog
from edit_window import EditDialog


class NowPlayingItemWidget(QWidget):
    """当前播放列表的每一行控件，包含歌曲名和删除按钮"""
    def __init__(self, song_name, parent=None):
        """
        初始化歌曲项控件
        :param song_name: 歌曲名称
        :param parent: 父控件
        """
        super().__init__(parent)
        self.song_name = song_name
        self.init_ui()
        self.setup_style()

    def init_ui(self):
        """初始化UI"""
        # 创建水平布局
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)

        # 歌曲名标签
        self.song_label = QLabel(self.song_name)
        self.song_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # 删除按钮
        self.delete_button = QPushButton("删除")
        self.delete_button.setFixedSize(60, 30)
        self.delete_button.setCursor(Qt.PointingHandCursor)

        # 将标签和按钮添加到布局
        layout.addWidget(self.song_label, 1)  # 标签占1份空间
        layout.addWidget(self.delete_button, 0)  # 按钮固定大小

        self.setLayout(layout)

        # 设置控件最小高度
        self.setMinimumHeight(50)

    def setup_style(self):
        """设置样式"""
        # 歌曲标签样式
        self.song_label.setStyleSheet("""
            QLabel {
                color: lightblue;
                font-size: 18px;
                background: transparent;
                font-weight: 500;
            }
        """)

        # 删除按钮样式
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4444;
                border: none;
                border-radius: 6px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF6666;
            }
            QPushButton:pressed {
                background-color: #CC3333;
            }
        """)

        # 控件整体样式（悬停效果）
        self.setStyleSheet("""
            NowPlayingItemWidget {
                background-color: transparent;
                border-bottom: 1px solid #3D3D3D;
            }
            NowPlayingItemWidget:hover {
                background-color: #2D2D2D;
            }
        """)

    def set_delete_callback(self, callback):
        """设置删除按钮的回调函数"""
        self.delete_button.clicked.connect(callback)


class now_playing_list:
    """Main_Page的第二行左边组件"""

    def __init__(self):
        super().__init__()
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.current_list_name = config['push_list']['push_list_name']
        self.current_list = list(check(str(self.current_list_name)).keys())

    def npl_initUI(self):
        self.top_label = QLabel(self.current_list_name)

        self.scroll_area = QScrollArea()
        self.scroll_area.setFixedHeight(500)
        self.scroll_area.setWidgetResizable(True)  # 让内容自适应

        self.scroll_list = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_list)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)

        # 使用自定义控件添加列表项
        for song_name in self.current_list:
            item_widget = NowPlayingItemWidget(song_name)
            # 连接删除按钮事件 - 直接删除，无需确认
            item_widget.delete_button.clicked.connect(
                lambda checked, name=song_name: self.delete_song(name)
            )
            self.scroll_layout.addWidget(item_widget)

        # 添加弹性空间
        self.scroll_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_list)

    def npl_init_layout(self):
        self.npl_container = QWidget()
        main_layout = QVBoxLayout(self.npl_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)

        # 顶部布局（标签和切换按钮）
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.top_label)
        # 可以在这里添加切换按钮等
        main_layout.addLayout(top_layout)

        # 滚动列表
        main_layout.addWidget(self.scroll_area)

    def npl_init_CSS_dark(self):
        self.top_label.setStyleSheet('''
            QLabel {
                color: red;
                font-size: 35px;
                padding: 10px;
            }
        ''')

        # 滚动区域样式
        self.scroll_area.setStyleSheet('''
            QScrollArea {
                background-color: #1E1E1E;
                border: none;
                border-radius: 10px;
            }
            QScrollBar:vertical {
                background-color: #2D2D2D;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #555555;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #666666;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        ''')

        # 容器样式
        self.npl_container.setStyleSheet('''
            QWidget {
                background-color: #1A1A1A;
                border-radius: 15px;
            }
        ''')

    def delete_song(self, song_name):
        """删除歌曲"""
        # 从数据列表中删除
        if song_name in self.current_list:
            self.current_list.remove(song_name)
            # 刷新UI显示
            self.refresh_list()
            # 可选：打印日志
            print(f"已删除歌曲: {song_name}")

    def refresh_list(self):
        """刷新列表显示"""
        # 清空现有内容（保留最后一个弹性空间）
        while self.scroll_layout.count() > 1:
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 重新添加列表项
        for song_name in self.current_list:
            item_widget = NowPlayingItemWidget(song_name)
            item_widget.delete_button.clicked.connect(
                lambda checked, name=song_name: self.delete_song(name)
            )
            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, item_widget)

        # 确保弹性空间在最后
        # 如果弹性空间被移动了，重新添加
        if self.scroll_layout.count() > 0:
            last_item = self.scroll_layout.itemAt(self.scroll_layout.count() - 1)
            if last_item and not last_item.widget():
                # 最后一项是弹性空间，保持不变
                pass
            else:
                # 添加弹性空间
                self.scroll_layout.addStretch()

    def update(self,show_list):
        """更新整个组件"""
        # 重新加载数据
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.current_list_name = config['push_list']['push_list_name']
        self.current_list = show_list

        # 刷新UI
        self.npl_initUI()
        self.npl_init_layout()
        self.npl_init_CSS_dark()


class musiclist:
    """Main_Page的第二行中间组件"""
    def __init__(self):
        super().__init__()

        # 读取ini中的push_list_name生成self.show_list
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.push_list_name = config['push_list']['push_list_name']
        self.show_list = list(check(self.push_list_name).keys())

    def ml_initUI(self):
        self.top_label_ml = QLabel('歌单')
        self.switch_button = QPushButton('切换')
        self.switch_button.clicked.connect(self.switch_list)
        self.edit_button = QPushButton('编辑歌单')
        self.edit_button.clicked.connect(self.edit_list)
        self.push_button = QPushButton('push')
        self.push_button.clicked.connect(self.push)

        # 歌单列表
        self.push_scroll_area = QScrollArea()
        self.push_scroll_area.setFixedHeight(500)
        self.push_scroll_list = QWidget()
        self.push_scroll_layout = QVBoxLayout(self.push_scroll_list)
        # 遍历self.show_list填充滚动区域
        for n in self.show_list:
            l = QLabel(n)
            l.setStyleSheet('QLabel {color:lightblue;}')
            self.push_scroll_layout.addWidget(l)
        # end
        self.push_scroll_list.adjustSize()
        self.push_scroll_area.setWidget(self.push_scroll_list)

    def ml_init_layout(self):
        self.ml_container = QWidget()
        main_layout = QVBoxLayout(self.ml_container)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.top_label_ml,stretch=2)
        top_layout.addWidget(self.switch_button,stretch=1)
        top_layout.addWidget(self.edit_button,stretch=1)
        top_layout.addWidget(self.push_button,stretch=1)
        main_layout.addLayout(top_layout)

        main_layout.addWidget(self.push_scroll_area)

    def ml_init_CSS_dark(self):
        self.top_label_ml.setStyleSheet('''
                QLabel {
                    color: red;
                    font-size: 35px;
                }
                ''')
        self.switch_button.setStyleSheet('''
                QPushButton {
                    background-color: blue;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    font-size: 23px;
                    font-weight: 500;
                    min-height: 40px;
                    min-width: 40px;
                }
                QPushButton:hover {
                    background-color: darkblue;
                }
                QPushButton:pressed {
                    border: 5px groove;
                    padding: 6px 5px 4px 5px;
                }
                ''')
        self.edit_button.setStyleSheet('''
                QPushButton {
                    background-color: blue;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    font-size: 21px;
                    font-weight: 500;
                    min-height: 40px;
                    min-width: 40px;
                }
                QPushButton:hover {
                    background-color: darkblue;
                }
                QPushButton:pressed {
                    border: 5px groove;
                    padding: 6px 5px 4px 5px;
                }
                ''')
        self.push_button.setStyleSheet('''
                QPushButton {
                    background-color: red;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    font-size: 23px;
                    font-weight: 500;
                    min-height: 40px;
                    min-width: 40px;
                }
                QPushButton:hover {
                    background-color: #8B0000;
                }
                QPushButton:pressed {
                    border: 5px groove;
                    padding: 6px 5px 4px 5px;
                }
                ''')

    def switch_list(self):
        """切换按钮调用函数"""
        dialog = SwitchListDialog(self.push_list_name, self.ml_container.parent())
        if dialog.exec_() == QDialog.Accepted:
            # 用户点击了确认，更新配置
            new_list_name = dialog.selected_list
            if new_list_name and new_list_name != self.push_list_name:
                # 更新配置文件
                config = configparser.ConfigParser()
                config.read('config.ini')
                config['push_list']['push_list_name'] = new_list_name
                with open('config.ini', 'w') as f:
                    config.write(f)
                # 更新显示
                def update():
                    # 重新加载数据
                    config = configparser.ConfigParser()
                    config.read('config.ini')
                    self.push_list_name = config['push_list']['push_list_name']
                    self.show_list = list(check(self.push_list_name).keys())

                    # 重新创建整个内容区域
                    # 删除旧的内容
                    if self.push_scroll_list:
                        self.push_scroll_list.deleteLater()

                    # 创建新的内容部件
                    self.push_scroll_list = QWidget()
                    self.push_scroll_layout = QVBoxLayout(self.push_scroll_list)

                    # 添加内容
                    for n in self.show_list:
                        l = QLabel(n)
                        l.setStyleSheet('QLabel {color:lightblue;}')
                        self.push_scroll_layout.addWidget(l)

                    # 添加弹簧
                    self.push_scroll_layout.addStretch()

                    # 设置到滚动区域
                    self.push_scroll_area.setWidget(self.push_scroll_list)
                update()

    def edit_list(self):
        """编辑按钮调用函数 弹出EditDialog"""
        dialog = EditDialog(self.push_list_name)
        if dialog.exec_() != QDialog.Accepted:
            def update():
                # 重新加载数据
                config = configparser.ConfigParser()
                config.read('config.ini')
                self.push_list_name = config['push_list']['push_list_name']
                self.show_list = list(check(self.push_list_name).keys())

                # 重新创建整个内容区域
                # 删除旧的内容
                if self.push_scroll_list:
                    self.push_scroll_list.deleteLater()

                # 创建新的内容部件
                self.push_scroll_list = QWidget()
                self.push_scroll_layout = QVBoxLayout(self.push_scroll_list)

                # 添加内容
                for n in self.show_list:
                    l = QLabel(n)
                    l.setStyleSheet('QLabel {color:lightblue;}')
                    self.push_scroll_layout.addWidget(l)

                # 添加弹簧
                self.push_scroll_layout.addStretch()

                # 设置到滚动区域
                self.push_scroll_area.setWidget(self.push_scroll_list)
            update()

    def push(self):
        # 重新加载数据
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.push_list_name = config['push_list']['push_list_name']
        self.show_list = list(check(self.push_list_name).keys())


class Main_Page(now_playing_list,musiclist):
    def __init__(self):
        super().__init__()

    def initUI_main(self):
        self.searchbox = QLineEdit()

        self.search_button = QPushButton('搜索')
        self.search_button.clicked.connect(self.search)

        now_playing_list.npl_initUI(self)

        musiclist.ml_initUI(self)

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

        # 2.主布局第二行横向布局,包括(当前播放列表 歌单 (打开微型播放器 音量)竖直布局)
        self.second_layout = QHBoxLayout()
        self.second_layout.setSpacing(15)
        def set_second_layout():
            #2.1 当前播放列表
            now_playing_list.npl_init_layout(self)
            self.second_layout.addWidget(self.npl_container,stretch=1)

            #2.2 歌单
            musiclist.ml_init_layout(self)
            self.second_layout.addWidget(self.ml_container, stretch=1)

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
                        border: 5px groove #0f172a;
                    }
                ''')
        self.npl_container.setStyleSheet('''
                QWidget {
                    border-radius: 15px;
                    background: #000000;
                }
                ''')
        now_playing_list.npl_init_CSS_dark(self)

        self.ml_container.setStyleSheet('''
                QWidget {
                    border-radius: 15px;
                    background: #000000;
                }  
                ''')
        musiclist.ml_init_CSS_dark(self)