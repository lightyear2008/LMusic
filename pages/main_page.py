# Copyright (c) 2026 lightyear2008
# SPDX-License-Identifier: MIT
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtWidgets import (QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QLabel,
                             QLineEdit, QScrollArea, QSlider, QDialog)
import sys
import os
import configparser
import json
from just_playback import Playback
from threading import Lock

current_directory = os.path.dirname(os.path.abspath(__file__))
external_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(external_directory)

from searchbox import SearchBox
from dbcrudtool2 import check
from switch_window import SwitchListDialog
from edit_window import EditDialog


class NowPlayingItemWidget(QWidget):
    """当前播放列表的每一行控件，包含歌曲名和删除按钮"""
    select_signal = pyqtSignal(object,bool)

    def __init__(self, song_name, parent=None):
        super().__init__(parent)
        self.song_name = song_name
        self.selected = False
        self.init_UI()
        self.setup_style()

    def init_UI(self):
        """初始化UI"""
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)

        self.song_label = QLabel(self.song_name)
        self.song_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.delete_button = QPushButton("删除")
        self.delete_button.setFixedSize(60, 30)
        self.delete_button.setCursor(Qt.PointingHandCursor)

        layout.addWidget(self.song_label, 1)
        layout.addWidget(self.delete_button, 0)

        self.setLayout(layout)
        self.setMinimumHeight(50)

    def setup_style(self):
        """设置基础样式（只调用一次）"""
        # 歌曲标签基础样式
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

        # 控件整体样式（包含选中状态）
        self.setStyleSheet("""
            NowPlayingItemWidget {
                background-color: transparent;
                border-bottom: 1px solid #3D3D3D;
            }
            NowPlayingItemWidget:hover {
                background-color: #2D2D2D;
            }
            NowPlayingItemWidget[selected="true"] {
                background-color: #3A6EA5;
                border-left: 4px solid #5B9BD5;
            }
            NowPlayingItemWidget[selected="true"]:hover {
                background-color: #4A7EB5;
            }
        """)

    def set_selected(self, selected, emit_signal=True):
        """设置选中状态"""
        if self.selected != selected:
            self.selected = selected

            # 更新控件自身的属性
            self.setProperty("selected", str(selected).lower())
            self.style().unpolish(self)
            self.style().polish(self)

            # 更新歌曲标签样式
            self.update_label_style(selected)

            if emit_signal:
                self.select_signal.emit(self, selected)

    def update_label_style(self, selected):
        """根据选中状态更新标签样式"""
        if selected:
            self.song_label.setStyleSheet("""
                QLabel {
                    color: #2ECC71;
                    font-size: 24px;
                    background: transparent;
                    font-weight: bold;
                }
            """)
        else:
            self.song_label.setStyleSheet("""
                QLabel {
                    color: lightblue;
                    font-size: 18px;
                    background: transparent;
                    font-weight: 500;
                }
            """)

    def is_selected(self):
        """返回是否选中"""
        return self.selected

    def mousePressEvent(self, event):
        """鼠标点击时切换选中状态"""
        if event.button() == Qt.LeftButton:
            self.set_selected(not self.selected)
        super().mousePressEvent(event)

    def set_delete_callback(self, callback):
        """设置删除按钮的回调函数"""
        self.delete_button.clicked.connect(callback)


class now_playing_list:
    """Main_Page的第二行左边组件"""

    def __init__(self):
        super().__init__()
        with open('now_playing_message.json', 'r', encoding='utf-8') as f:
            self.now_playing_message_json = json.load(f)
        self.current_list_name = self.now_playing_message_json['play_list_name']
        self.current_list = self.now_playing_message_json['now_playing_list']

        self.current_selected_item = None
        self.item_list = []

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
            item_widget.select_signal.connect(self.on_item_selected_change)
            item_widget.text = song_name
            self.item_list.append(item_widget)

            # 选中json中指定的歌
            with open('now_playing_message.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            if song_name == data['selected_item']:
                item_widget.set_selected(True)

            # 连接删除按钮事件 - 直接删除，无需确认
            item_widget.delete_button.clicked.connect(
                lambda checked, name=song_name: self.delete_song(name)
            )
            self.scroll_layout.addWidget(item_widget)

        # 防止json中记录的选中项不在列表中
        if not any([n.is_selected() for n in self.item_list]) and len(self.item_list) > 0:
            self.item_list[0].set_selected(True) # 默认选中第一项
            # 修改json
            with open('now_playing_message.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            data['selected_item'] = self.item_list[0].song_name
            with open('now_playing_message.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        # 调试输出
        print(self.item_list)
        print([n.is_selected() for n in self.item_list])

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
        ''');

    def delete_song(self, song_name):
        """删除歌曲"""
        if song_name in self.current_list:
            # 同步json
            with open('now_playing_message.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            data['now_playing_list'].remove(song_name)
            with open('now_playing_message.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            # 记录是否删除的是当前选中项
            was_selected = (self.current_selected_item and
                            self.current_selected_item.song_name == song_name)

            self.current_list.remove(song_name)

            # 如果删除的是选中项，清除记录
            if was_selected:
                self.current_selected_item = None
                with open('now_playing_message.json','r',encoding='utf-8') as f:
                    data = json.load(f)
                if data['now_playing_list'][0]:
                    data['selected_item'] = data['now_playing_list'][0]
                    with open('now_playing_message.json','w',encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)

            # 刷新UI显示
            self.refresh_list()

    def refresh_list(self):
        """刷新列表显示"""
        # 清空现有内容（保留最后一个弹性空间）
        while self.scroll_layout.count() > 1:
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 清空列表记录
        self.item_list.clear()

        # 记录之前选中的歌曲名
        previously_selected_name = self.current_selected_item.song_name if self.current_selected_item else None

        # 重新添加列表项
        for i, song_name in enumerate(self.current_list):
            item_widget = NowPlayingItemWidget(song_name)
            item_widget.select_signal.connect(self.on_item_selected_change)
            self.item_list.append(item_widget)

            # 恢复选中状态
            should_select = False

            # 1. 如果是之前选中的歌曲且仍在列表中
            if previously_selected_name and song_name == previously_selected_name:
                should_select = True
            # 2. 如果没有之前选中的记录，且是第一项
            elif previously_selected_name is None and i == 0:
                should_select = True
            # 3. 如果列表只有一项，强制选中
            elif len(self.current_list) == 1:
                should_select = True

            if should_select:
                item_widget.set_selected(True, emit_signal=False)
                self.current_selected_item = item_widget

            item_widget.delete_button.clicked.connect(
                lambda checked, name=song_name: self.delete_song(name)
            )
            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, item_widget)

        # 确保至少有一个选中项
        if self.current_selected_item is None and len(self.current_list) > 0:
            first_item = self.item_list[0]
            first_item.set_selected(True, emit_signal=False)
            self.current_selected_item = first_item

        # 确保弹性空间在最后
        if self.scroll_layout.count() > 0:
            last_item = self.scroll_layout.itemAt(self.scroll_layout.count() - 1)
            if last_item and not last_item.widget():
                pass
            else:
                self.scroll_layout.addStretch()

    def update_npl(self,show_list):
        """更新整个组件"""
        # 重新加载数据
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.current_list_name = config['push_list']['push_list_name']
        self.current_list = show_list
        self.top_label.setText(self.current_list_name)

        # 刷新UI
        self.refresh_list()

    def on_item_selected_change(self,item,selected):
        """当NowPlayingItemWidget的mousePressEvent运行时调用"""
        if selected:
            # 取消之前选中的项
            if self.current_selected_item and self.current_selected_item != item:
                self.current_selected_item.set_selected(False, emit_signal=False)

            # 设置新的选中项
            self.current_selected_item = item

            # 修改json
            with open('now_playing_message.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            data['selected_item'] = item.song_name
            with open('now_playing_message.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            # 选中已经选中的项
            if self.current_selected_item == item:
                item.set_selected(True, emit_signal=False)

    def change_selected_item_callback(self,song_name):
        self.current_selected_item.set_selected(False, emit_signal=False)
        for item in self.item_list:
            if item.song_name == song_name:
                item.set_selected(True, emit_signal=False)
                self.current_selected_item = item
                break


class musiclist:
    """Main_Page的第二行中间组件"""
    def __init__(self):
        super().__init__()

        # 读取ini中的push_list_name生成self.show_list
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.push_list_name = config['push_list']['push_list_name']
        self.show_list = list(check(self.push_list_name).keys())

        self.push_callback = None

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

        if self.push_callback:
            self.push_callback(self.show_list)
            # 同步json
            with open('now_playing_message.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            data['play_list_name'] = self.push_list_name
            data['now_playing_list'] = self.show_list
            with open('now_playing_message.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def set_push_callback(self, callback):
        """设置push按钮的回调函数"""
        self.push_callback = callback

    def refresh(self):
        """刷新显示"""
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


class musicplayer:
    """Main_Page的第二行右上方组件"""
    def __init__(self):
        super().__init__()

    def mp_initUI(self):
        self.last_btn = QPushButton('上一首')
        self.play_btn = QPushButton('播放')
        self.play_btn.clicked.connect(self.play_state_changed)
        self.next_btn = QPushButton('下一首')
        with open('now_playing_message.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.mode_btn = QPushButton('顺序' if data['play_mode']=='normal' else '循环' if data['play_mode']=='repeat' else '随机')
        self.mode_btn.clicked.connect(self.change_mode)

        # 添加滑块
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setRange(0, 100)
        self.progress_slider.setValue(0)

    def mp_init_layout(self):
        self.mp_container = QWidget()
        main_layout = QVBoxLayout(self.mp_container)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.last_btn)
        btn_layout.addWidget(self.play_btn)
        btn_layout.addWidget(self.next_btn)
        btn_layout.addWidget(self.mode_btn)
        main_layout.addLayout(btn_layout)

        # 添加滑块布局
        slider_layout = QVBoxLayout()
        slider_layout.addWidget(self.progress_slider)
        main_layout.addLayout(slider_layout)

    def mp_init_CSS_dark(self):
        self.last_btn.setStyleSheet('''
                QPushButton {
                    background-color: #555555;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    font-size: 21px;
                    font-weight: 500;
                    min-height: 40px;
                    min-width: 40px;
                }
                QPushButton:hover {
                    background-color: #666666;
                }
                QPushButton:pressed {
                    border: 5px groove;
                    padding: 6px 5px 4px 5px;
                }
                ''')
        self.play_btn.setStyleSheet('''
                QPushButton {
                    background-color: #555555;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    font-size: 21px;
                    font-weight: 500;
                    min-height: 40px;
                    min-width: 40px;
                }
                QPushButton:hover {
                    background-color: #666666;
                }
                QPushButton:pressed {
                    border: 5px groove;
                    padding: 6px 5px 4px 5px;
                }
                ''')
        self.next_btn.setStyleSheet('''
                QPushButton {
                    background-color: #555555;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    font-size: 21px;
                    font-weight: 500;
                    min-height: 40px;
                    min-width: 40px;
                }
                QPushButton:hover {
                    background-color: #666666;
                }
                QPushButton:pressed {
                    border: 5px groove;
                    padding: 6px 5px 4px 5px;
                }
                ''')
        self.mode_btn.setStyleSheet('''
                QPushButton {
                    background-color: #555555;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    font-size: 21px;
                    font-weight: 500;
                    min-height: 40px;
                    min-width: 40px;
                }
                QPushButton:hover {
                    background-color: #666666;
                }
                QPushButton:pressed {
                    border: 5px groove;
                    padding: 6px 5px 4px 5px;
                }
                ''')
        # 滑块样式
        config = configparser.ConfigParser()
        config.read('config.ini')
        style = int(config['main']['slider_style'])
        if style == 1:
            # 经典蓝色风格
            self.progress_slider.setStyleSheet('''
                QSlider {
                    min-height: 30px;
                }
                QSlider::groove:horizontal {
                    height: 6px;
                    background: #3a3a3a;
                    border-radius: 3px;
                }
                QSlider::sub-page:horizontal {
                    background: #3574F0;
                    border-radius: 3px;
                }
                QSlider::add-page:horizontal {
                    background: #3a3a3a;
                    border-radius: 3px;
                }
                QSlider::handle:horizontal {
                    background: #ffffff;
                    width: 15px;
                    height: 15px;
                    margin: -5px 0;
                    border-radius: 7px;
                }
                QSlider::handle:horizontal:hover {
                    background: #3574F0;
                    transform: scale(1.2);
                }
                ''')
        elif style == 2:
            # 蓝色渐变风格
            self.progress_slider.setStyleSheet('''
                QSlider {
                    min-height: 40px;
                }
                QSlider::groove:horizontal {
                    height: 4px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                stop:0 #2a2a2a, stop:1 #3a3a3a);
                    border-radius: 2px;
                }
                QSlider::sub-page:horizontal {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                stop:0 #3574F0, stop:1 #5B9AFF);
                    border-radius: 2px;
                }
                QSlider::handle:horizontal {
                    background: white;
                    width: 14px;
                    height: 14px;
                    margin: -5px 0;
                    border-radius: 7px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                }
                QSlider::handle:horizontal:hover {
                    background: #5B9AFF;
                    width: 16px;
                    height: 16px;
                    margin: -6px 0;
                }
                ''')
        elif style == 3:
            # 绿-蓝渐变风格
            self.progress_slider.setStyleSheet('''
                QSlider {
                    min-height: 50px;
                }
                QSlider::groove:horizontal {
                    height: 6px;
                    background: #2a2a2a;
                    border-radius: 3px;
                }
                QSlider::sub-page:horizontal {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                stop:0 #00FF88,
                                                stop:0.3 #00FFCC,
                                                stop:0.6 #00CCFF,
                                                stop:1 #0088FF);
                    border-radius: 3px;
                }
                QSlider::add-page:horizontal {
                    background: #2a2a2a;
                    border-radius: 3px;
                }
                QSlider::handle:horizontal {
                    background: white;
                    width: 24px;
                    height: 24px;
                    margin: -9px 0;
                    border-radius: 12px;
                    border: 2px solid #00FF88;
                    box-shadow: 0 0 8px rgba(0,255,136,0.5);
                }
                QSlider::handle:horizontal:hover {
                    background: #f0f0f0;
                    width: 28px;
                    height: 28px;
                    margin: -11px 0;
                    border-radius: 14px;
                    border: 2px solid #00FFCC;
                    box-shadow: 0 0 12px rgba(0,255,204,0.6);
                }
                QSlider::handle:horizontal:pressed {
                    background: #e0e0e0;
                    width: 26px;
                    height: 26px;
                    margin: -10px 0;
                    border-radius: 13px;
                    border: 2px solid #0088FF;
                    box-shadow: 0 0 10px rgba(0,136,255,0.5);
                }
                ''')
        elif style == 4:
            # 荧光渐变风格
            self.progress_slider.setStyleSheet('''
                    QSlider {
                        min-height: 55px;
                    }
                    QSlider::groove:horizontal {
                        height: 8px;
                        background: #1a1a1a;
                        border-radius: 4px;
                    }
                    QSlider::sub-page:horizontal {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                    stop:0 #7FFF00,
                                                    stop:0.25 #00FF7F,
                                                    stop:0.5 #00FFFF,
                                                    stop:0.75 #1E90FF,
                                                    stop:1 #0000FF);
                        border-radius: 4px;
                    }
                    QSlider::handle:horizontal {
                        background: qradialgradient(cx:0.5, cy:0.5, radius: 0.5,
                                                    stop:0 #FFFFFF,
                                                    stop:0.7 #E0E0E0,
                                                    stop:1 #C0C0C0);
                        width: 26px;
                        height: 26px;
                        margin: -9px 0;
                        border-radius: 13px;
                        border: 3px solid #7FFF00;
                        box-shadow: 0 0 10px rgba(127,255,0,0.4);
                    }
                    QSlider::handle:horizontal:hover {
                        background: #FFFFFF;
                        width: 30px;
                        height: 30px;
                        margin: -11px 0;
                        border: 3px solid #00FFFF;
                        box-shadow: 0 0 15px rgba(0,255,255,0.6);
                    }
                    QSlider::handle:horizontal:pressed {
                        background: #E0E0E0;
                        width: 28px;
                        height: 28px;
                        margin: -10px 0;
                        border: 3px solid #1E90FF;
                    }
                    ''')

    def change_mode(self):
        with open('now_playing_message.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        current_mode = data['play_mode']
        if current_mode == 'normal':
            new_mode = 'repeat'
            self.mode_btn.setText('循环')
        elif current_mode == 'repeat':
            new_mode = 'random'
            self.mode_btn.setText('随机')
        elif current_mode == 'random':
            new_mode = 'normal'
            self.mode_btn.setText('顺序')
        else:
            new_mode = 'normal'
            self.mode_btn.setText('顺序')
        data['play_mode'] = new_mode
        with open('now_playing_message.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def play_state_changed(self):
        """根据播放状态更新按钮文本"""
        with open('now_playing_message.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        if data['if_playing']:
            self.play_btn.setText('播放')
            data['if_playing'] = False
        else:
            self.play_btn.setText('暂停')
            data['if_playing'] = True
        with open('now_playing_message.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def update_position_callback(self, percent):
        """更新进度条位置"""
        self.progress_slider.setValue(percent)


class Main_Playing_Thread(QThread):
    """音乐播放线程"""

    # 定义信号
    position_changed = pyqtSignal(int)  # 播放进度百分比 (0-100)
    song_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.playback = Playback()
        self.lock = Lock()
        data = self.read_json()
        data['if_playing'] = False
        self.rewrite_json(data)

        self.update_data()
        self.thread_current_file = self.read_json()['selected_item']
        self.thread_is_playing = False  # 记录此线程的播放状态,用来判断播放按钮被点击

    def read_json(self):
        with self.lock:
            with open('now_playing_message.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data

    def rewrite_json(self, data):
        with self.lock:
            with open('now_playing_message.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def update_data(self):
        data = self.read_json()
        self.current_file = data['selected_item']
        self.is_playing = data['if_playing']
        self.mode = data['play_mode']

    def run(self):
        """线程主循环"""
        while True:
            self.update_data()

            # 开始播放
            if self.is_playing and not self.thread_is_playing:
                if self.playback.paused:
                    self.resume()
                else:
                    status = self.load()
                    if status:
                        self.play()

            # 暂停播放
            if not self.is_playing and self.thread_is_playing:
                self.pause()

            # 用户切换歌曲
            if self.thread_current_file != self.current_file:
                self.stop_()
                self.load()
                self.play()
                self.thread_current_file = self.current_file

            # 播放结束
            if not self.playback.active and self.is_playing:
                # 根据self.mode切换音频并开始播放
                if self.mode == 'repeat':
                    self.playback.play()
                elif self.mode == 'normal':
                    print('normal')
                    # 计算下一首歌的名字
                    data = self.read_json()
                    list = data['now_playing_list']
                    if len(list) - 1 == list.index(data['selected_item']):
                        next_song = list[0]
                    else:
                        next_song = list[list.index(data['selected_item']) + 1]
                    self.thread_current_file = next_song # 防止'用户切歌'被触发

                    # 更新json并开始播放
                    data = self.read_json()
                    data['selected_item'] = next_song
                    self.rewrite_json(data)
                    self.update_data()
                    self.load()
                    self.playback.play()

                    # 丢信号让UI更新
                    self.song_changed.emit(next_song)

                elif self.mode == 'random':
                    print('random')

            # 计算播放进度百分比
            if self.is_playing:
                current_pos_ms = int(self.playback.curr_pos * 1000)
                duration_ms = int(self.playback.duration * 1000)
                percent = int((current_pos_ms / duration_ms) * 100)
                percent = max(0, min(100, percent))  # 限制在 0-100 范围内
                self.position_changed.emit(percent) # 丢信号

            self.msleep(500)  # 更新时间

    def load(self):
        """加载音乐文件"""
        try:
            def path_deal():
                full_path = os.path.join('mp3_db','main_list',self.current_file + '.mp3')
                if os.path.isfile(full_path):
                    return full_path
                else:
                    raise FileNotFoundError(f"文件 {full_path} 不存在")
            self.playback.load_file(path_deal())
            return True
        except Exception as e:
            print(f"加载文件失败: {str(e)}")
            return False

    def play(self):
        """播放"""
        try:
            self.playback.play()
            # 同步json和线程状态
            data = self.read_json()
            data['if_playing'] = True
            self.rewrite_json(data)
            self.thread_is_playing = True
        except Exception as e:
            print(f"播放失败: {str(e)}")

    def pause(self):
        """暂停"""
        try:
            self.playback.pause()
            data = self.read_json()
            data['if_playing'] = False
            self.rewrite_json(data)
            self.thread_is_playing = False
        except Exception as e:
            print(f"暂停失败: {str(e)}")

    def resume(self):
        """继续播放"""
        try:
            self.playback.resume()
            data = self.read_json()
            data['if_playing'] = True
            self.rewrite_json(data)
            self.thread_is_playing = True
        except Exception as e:
            print(f"继续播放失败: {str(e)}")

    def stop_(self):
        """停止 加下划线是防止命名重复"""
        try:
            self.playback.stop()
            self.position_changed.emit(0)  # 重置进度为 0%
        except Exception as e:
            print(f"停止失败: {str(e)}")

    def seek(self, percent):
        """跳转到指定位置（百分比 0-100）"""
        try:
            if self.length_ms > 0:
                position_ms = int((percent / 100.0) * self.length_ms)
                position_sec = position_ms / 1000.0
                self.playback.seek(position_sec)
                self.position_changed.emit(percent)
        except Exception as e:
            print(f"跳转失败: {str(e)}")


class Main_Page(now_playing_list,musiclist,musicplayer):
    def __init__(self):
        super().__init__()
        self.init_player()
        self.set_push_callback(self.update_npl)

    def init_player(self):
        self.player_thread = Main_Playing_Thread()
        self.player_thread.position_changed.connect(self.on_position_changed)
        self.player_thread.song_changed.connect(self.on_song_changed)
        self.player_thread.start()

    def on_position_changed(self, percent):
        """接收播放线程的进度更新信号"""
        self.update_position_callback(percent)

    def on_song_changed(self,song):
        """接收播放线程的歌曲切换信号"""
        self.change_selected_item_callback(song)


    def initUI_main(self):
        self.searchbox = QLineEdit()

        self.search_button = QPushButton('搜索')
        self.search_button.clicked.connect(self.search)

        now_playing_list.npl_initUI(self)

        musiclist.ml_initUI(self)

        musicplayer.mp_initUI(self)

        self.tiny_player_button = QPushButton('最小化播放器')

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

            #2.3 (音乐播放器 打开微型播放器 音量)竖直布局
            self.right_layout = QVBoxLayout()
            def set_right_layout():
                # 音乐播放器
                musicplayer.mp_init_layout(self)
                self.right_layout.addWidget(self.mp_container,stretch=2)
                self.right_layout.addSpacing(200)
                # 打开微型播放器按钮
                self.right_layout.addWidget(self.tiny_player_button,stretch=1)
                self.right_layout.addSpacing(20)
                # 音量条
                self.right_layout.addWidget(self.volume_slider,stretch=1)
            set_right_layout()
            self.second_layout.addLayout(self.right_layout, stretch=1)
            self.second_layout.addSpacing(20)
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
        self.search_window.destroyed.connect(lambda :musiclist.refresh(self))

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

        self.mp_container.setStyleSheet('''
                QWidget {
                    border-radius: 15px;
                    background: #000000;
                }  
                ''')
        musicplayer.mp_init_CSS_dark(self)