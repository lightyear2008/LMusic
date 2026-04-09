from PyQt5.QtWidgets import (QDialog, QApplication, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QListWidget,
                             QListWidgetItem, QLabel, QLineEdit)
from PyQt5.QtGui import QPalette, QColor
from PyQt5 import QtCore

import sys

from dbcrudtool2 import check, delete, check_lists, delete_from_db, add, add_list, delete_list, rename_list
from switch_window import SwitchListDialog

COLOR_MODE = 'DARK'


class MessageDialog(QDialog):
    """自定义提示窗口类"""

    def __init__(self, message, title="提示", parent=None, show_cancel=False):
        """
        初始化提示窗口
        :param message: 提示消息
        :param title: 窗口标题，默认为"提示"
        :param parent: 父窗口
        :param show_cancel: 是否显示取消按钮
        """
        super().__init__(parent)
        self.message = message
        self.title = title
        self.show_cancel = show_cancel
        self.init_ui()
        self.setup_style()
        self.center_on_parent()

    def init_ui(self):
        """初始化UI"""
        # 设置窗口标题
        self.setWindowTitle(self.title)

        # 设置窗口大小
        self.setFixedSize(450, 250)

        # 设置窗口标志（使窗口置顶）
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowStaysOnTopHint)

        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(25)

        # 消息标签
        self.message_label = QLabel(self.message)
        self.message_label.setWordWrap(True)  # 自动换行
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setMinimumHeight(100)

        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        if self.show_cancel:
            # 显示取消按钮
            self.cancel_button = QPushButton("取消")
            self.cancel_button.setFixedSize(120, 45)
            self.cancel_button.clicked.connect(self.reject)

            self.ok_button = QPushButton("确定")
            self.ok_button.setFixedSize(120, 45)
            self.ok_button.clicked.connect(self.accept)

            # 两个按钮居中
            button_layout.addStretch()
            button_layout.addWidget(self.ok_button)
            button_layout.addWidget(self.cancel_button)
            button_layout.addStretch()
        else:
            # 只显示确定按钮
            self.ok_button = QPushButton("确定")
            self.ok_button.setFixedSize(120, 45)
            self.ok_button.clicked.connect(self.accept)

            # 按钮居中
            button_layout.addStretch()
            button_layout.addWidget(self.ok_button)
            button_layout.addStretch()

        # 添加到主布局
        main_layout.addWidget(self.message_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def setup_style(self):
        """设置样式"""
        # 设置窗口背景色
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(43, 45, 48))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

        # 设置消息标签样式
        self.message_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 30px;
                background-color: #2D2D2D;
                border-radius: 8px;
                padding: 20px;
                font-weight: 500;
            }
        """)

        # 设置确定按钮样式
        self.ok_button.setStyleSheet("""
            QPushButton {
                background-color: #3574F0;
                border: none;
                border-radius: 8px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4A8CF7;
            }
            QPushButton:pressed {
                background-color: #2A5FD0;
            }
        """)

        # 设置取消按钮样式（如果有）
        if self.show_cancel:
            self.cancel_button.setStyleSheet("""
                QPushButton {
                    background-color: #555555;
                    border: none;
                    border-radius: 8px;
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #666666;
                }
                QPushButton:pressed {
                    background-color: #444444;
                }
            """)

    def center_on_parent(self):
        """在父窗口居中偏上显示"""
        if self.parent():
            parent_geometry = self.parent().geometry()
            dialog_geometry = self.geometry()
            # 计算位置：水平居中，垂直方向向上偏移20%
            x = parent_geometry.x() + (parent_geometry.width() - dialog_geometry.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - dialog_geometry.height()) // 3
            self.move(x, y)
        else:
            # 如果没有父窗口，在屏幕中央偏上显示
            screen = QApplication.desktop().screenGeometry()
            dialog_geometry = self.geometry()
            x = (screen.width() - dialog_geometry.width()) // 2
            y = (screen.height() - dialog_geometry.height()) // 3
            self.move(x, y)

    @staticmethod
    def show_message(message, title="提示", parent=None, show_cancel=False):
        """
        静态方法：显示提示窗口
        :param message: 提示消息
        :param title: 窗口标题
        :param parent: 父窗口
        :param show_cancel: 是否显示取消按钮
        :return: 如果有取消按钮返回True/False，否则返回None
        """
        dialog = MessageDialog(message, title, parent, show_cancel)
        result = dialog.exec_()

        if show_cancel:
            # 如果有取消按钮，返回用户选择结果
            return result == QDialog.Accepted
        else:
            # 如果没有取消按钮，返回None
            return None


class InputDialog(QDialog):
    """自定义输入框类"""

    def __init__(self, message, title="输入", parent=None, default_text=''):
        """
        初始化输入窗口
        :param message: 提示消息
        :param title: 窗口标题，默认为"输入"
        :param parent: 父窗口
        :param default_text: 默认输入文本
        """
        super().__init__(parent)
        self.message = message
        self.title = title
        self.default_text = default_text
        self.input_value = ''
        self.init_UI()
        self.init_layout()
        self.init_CSS()

    def init_UI(self):
        """初始化UI"""
        def init_dialog():
            # 设置窗口标题
            self.setWindowTitle(self.title)

            # 设置窗口大小
            self.setFixedSize(450, 300)

            # 设置窗口标志（使窗口置顶）
            self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowStaysOnTopHint)

            # 在父窗口居中偏上显示
            if self.parent():
                parent_geometry = self.parent().geometry()
                dialog_geometry = self.geometry()
                # 计算位置：水平居中，垂直方向向上偏移20%
                x = parent_geometry.x() + (parent_geometry.width() - dialog_geometry.width()) // 2
                y = parent_geometry.y() + (parent_geometry.height() - dialog_geometry.height()) // 3
                self.move(x, y)
            else:
                # 如果没有父窗口，在屏幕中央偏上显示
                screen = QApplication.desktop().screenGeometry()
                dialog_geometry = self.geometry()
                x = (screen.width() - dialog_geometry.width()) // 2
                y = (screen.height() - dialog_geometry.height()) // 3
                self.move(x, y)
        init_dialog()

        # 提示消息标签
        self.message_label = QLabel(self.message)
        self.message_label.setWordWrap(True)  # 自动换行
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setMinimumHeight(60)

        # 输入框
        self.input_edit = QLineEdit()
        self.input_edit.setText(self.default_text)
        self.input_edit.setMinimumHeight(45)
        self.input_edit.setPlaceholderText("请输入内容...")

        # 设置输入框焦点
        self.input_edit.setFocus()

        # 按回车键触发确定
        self.input_edit.returnPressed.connect(self.accept)

        # 确定按钮
        self.ok_button = QPushButton("确定")
        self.ok_button.setFixedSize(120, 45)
        self.ok_button.clicked.connect(self.accept)

        # 取消按钮
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setFixedSize(120, 45)
        self.cancel_button.clicked.connect(self.reject)

    def init_layout(self):
        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        # 按钮居中
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()

        # 添加到主布局
        main_layout.addWidget(self.message_label)
        main_layout.addWidget(self.input_edit)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def init_CSS(self):
        """设置样式"""
        # 设置窗口背景色
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(43, 45, 48))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

        # 设置提示消息标签样式
        self.message_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                background-color: #2D2D2D;
                border-radius: 8px;
                padding: 15px;
                font-weight: 500;
            }
        """)

        # 设置输入框样式
        self.input_edit.setStyleSheet("""
            QLineEdit {
                background-color: #2D2D2D;
                border: 2px solid #4D4D4D;
                border-radius: 8px;
                color: white;
                font-size: 26px;
                padding: 10px 15px;
                selection-background-color: #3574F0;
            }
            QLineEdit:focus {
                border: 2px solid #3574F0;
            }
        """)

        # 设置确定按钮样式
        self.ok_button.setStyleSheet("""
            QPushButton {
                background-color: #3574F0;
                border: none;
                border-radius: 8px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4A8CF7;
            }
            QPushButton:pressed {
                background-color: #2A5FD0;
            }
        """)

        # 设置取消按钮样式
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                border: none;
                border-radius: 8px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
        """)

    def get_input_text(self):
        return self.input_value if self.input_value else ''

    def accept(self):
        """重写accept方法，保存输入内容"""
        self.input_value = self.input_edit.text()
        super().accept()

    @staticmethod
    def show_input_box(message, title="输入", parent=None, default_text=""):
        """
        静态方法：显示输入窗口
        :param message: 提示消息
        :param title: 窗口标题
        :param parent: 父窗口
        :param default_text: 默认输入文本
        :return: 如果用户点击确定返回输入的文本，否则返回None
        """
        dialog = InputDialog(message, title, parent, default_text)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            return dialog.get_input_text()
        else:
            return None


class EditListsDialog(QDialog):
    def __init__(self, origin_path, parent=None):
        super().__init__(parent)
        self.origin_path = origin_path
        self.init_UI()
        self.init_layout()
        self.init_DARK_CSS()
        self.update_lists()

    def init_UI(self):
        def init_dialog():
            # 设置窗口标题
            self.setWindowTitle('歌单管理')

            # 获取屏幕的宽度和高度
            screen = QApplication.desktop().screenGeometry()
            screen_width = screen.width()
            screen_height = screen.height()

            # 设置窗口的宽度和高度值
            window_width = int(screen_width / 4.5)
            window_height = int(screen_height / 2)

            # 设置窗口大小
            self.resize(window_width, window_height)
            self.setMinimumSize(window_width, window_height)

            # 设置窗口标志
            self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint)

            # 设置主窗口背景色
            palette = QPalette()
            if COLOR_MODE == 'LIGHT':
                palette.setColor(QPalette.Window, QColor(255, 255, 255))
            else:
                palette.setColor(QPalette.Window, QColor(43, 45, 48))
            self.setPalette(palette)

            # 窗口居中
            screen = QApplication.desktop().screenGeometry()
            size = self.geometry()
            self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
        init_dialog()

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)  # 单选模式

        # 创建底部按钮
        self.btn_confirm = QPushButton('新增')
        self.btn_confirm.clicked.connect(self.create_new_list)
        self.btn_rename = QPushButton('重命名')
        self.btn_rename.clicked.connect(self.rename_list)
        self.btn_cancel = QPushButton('删除')
        self.btn_cancel.clicked.connect(self.delete_list)

    def init_layout(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 添加列表控件
        main_layout.addWidget(self.list_widget, 1)

        # 底部按钮布局
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(20, 15, 20, 15)
        button_layout.addWidget(self.btn_confirm)
        button_layout.addWidget(self.btn_rename)
        button_layout.addWidget(self.btn_cancel)

        bottom_widget = QWidget()
        bottom_widget.setLayout(button_layout)
        bottom_widget.setFixedHeight(75)
        main_layout.addWidget(bottom_widget)

        self.setLayout(main_layout)

    def init_DARK_CSS(self):
        """初始化样式"""
        # 列表控件样式
        self.list_widget.setStyleSheet("""
                    QListWidget {
                        background-color: #2D2D2D;
                        border: none;
                        outline: none;
                    }
                    QListWidget::item {
                        border-bottom: 2px solid #3D3D3D;
                        padding: 0px;
                        min-height: 50px;
                        color: white;
                    }
                    QListWidget::item:hover {
                        background-color: #3D3D3D;
                    }
                    QListWidget::item:selected {
                        background-color: #3574F0;
                    }
                    QScrollBar:vertical {
                        background-color: #2D2D2D;
                        width: 12px;
                        border-radius: 6px;
                    }
                    QScrollBar::handle:vertical {
                        background-color: #555555;
                        border-radius: 6px;
                        min-height: 20px;
                    }
                    QScrollBar::handle:vertical:hover {
                        background-color: #666666;
                    }
                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                        border: none;
                        background: none;
                    }
                    QScrollBar:horizontal {
                        background-color: #2D2D2D;
                        height: 12px;
                        border-radius: 6px;
                    }
                    QScrollBar::handle:horizontal {
                        background-color: #555555;
                        border-radius: 6px;
                        min-width: 20px;
                    }
                    QScrollBar::handle:horizontal:hover {
                        background-color: #666666;
                    }
                    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                        border: none;
                        background: none;
                    }
                """)

        # 底部容器样式
        bottom_widget = self.layout().itemAt(1).widget()
        if bottom_widget:
            bottom_widget.setStyleSheet("""
                        QWidget {
                            background-color: #3D3D3D;
                            border-top: 2px solid #4D4D4D;
                        }
                    """)

        # 确定按钮样式
        self.btn_confirm.setStyleSheet("""
                    QPushButton {
                        background-color: #3574F0;
                        border: none;
                        border-radius: 8px;
                        color: white;
                        font-size: 16px;
                        font-weight: bold;
                        padding: 10px 20px;
                        min-width: 100px;
                    }
                    QPushButton:hover {
                        background-color: #4A8CF7;
                    }
                    QPushButton:pressed {
                        background-color: #2A5FD0;
                    }
                """)

        # 重命名按钮样式
        self.btn_rename.setStyleSheet('''
                    QPushButton {
                        background-color: #3574F0;
                        border: none;
                        border-radius: 8px;
                        color: white;
                        font-size: 16px;
                        font-weight: bold;
                        padding: 10px 20px;
                        min-width: 100px;
                    }
                    QPushButton:hover {
                        background-color: #4A8CF7;
                    }
                    QPushButton:pressed {
                        background-color: #2A5FD0;
                    }
                ''')

        # 取消按钮样式
        self.btn_cancel.setStyleSheet("""
                    QPushButton {
                        background-color: #555555;
                        border: none;
                        border-radius: 8px;
                        color: white;
                        font-size: 16px;
                        font-weight: bold;
                        padding: 10px 20px;
                        min-width: 100px;
                    }
                    QPushButton:hover {
                        background-color: #666666;
                    }
                    QPushButton:pressed {
                        background-color: #444444;
                    }
                """)

    def update_lists(self):
        """加载歌单列表"""
        self.list_widget.clear()
        lists = check_lists()

        for list_name in lists:
            item = QListWidgetItem(list_name)
            item.setSizeHint(QtCore.QSize(0, 50))  # 设置每项高度
            self.list_widget.addItem(item)

            # 标记当前歌单
            if list_name == self.origin_path:
                # 设置不同样式或添加标记
                item.setForeground(QColor(76, 175, 80))  # 绿色文字

        # 滚动到当前歌单
        if self.origin_path in lists:
            items = self.list_widget.findItems(self.origin_path, QtCore.Qt.MatchExactly)
            if items:
                self.list_widget.setCurrentItem(items[0])
                self.list_widget.scrollToItem(items[0])

    def get_selected_list(self):
        """获取选中的歌单"""
        current_item = self.list_widget.currentItem()
        return current_item.text() if current_item else None

    def create_new_list(self):
        input_text = InputDialog.show_input_box("请输入新歌单名称:", "创建新歌单", self)
        if input_text:
            if input_text in check_lists():
                MessageDialog.show_message("歌单已存在，请选择其他名称。", "提示", self)
            else:
                # 创建新歌单文件
                add_list(input_text)
                self.update_lists()

    def delete_list(self):
        selected_list = self.list_widget.currentItem().text()
        num_of_musics = len(check(selected_list))
        if selected_list == 'main':
            MessageDialog.show_message('主歌单无法删除', title='提示', parent=self)
        else:
            # 选择的不是主歌单 允许删除 检查如果歌单不为空则提示确认删除
            if check(selected_list) != {}:
                if MessageDialog.show_message(f'此歌单内含{num_of_musics}首歌曲，是否删除?', "提示", self, show_cancel=True):
                    delete_list(selected_list)
                    self.update_lists()
            else:
                delete_list(selected_list)
                self.update_lists()

    def rename_list(self):
        old_name = self.list_widget.currentItem().text()
        if old_name == 'main':
            MessageDialog.show_message('主歌单无法重命名', '提示', self)
            return
        new_name = InputDialog.show_input_box('请输入新名称:','重命名',self, default_text=old_name)
        if new_name is None: # 用户关闭窗口
            return
        if new_name == 'main':
            MessageDialog.show_message('名称不可与主歌单重复', '提示', self)
            self.rename_list()
            return
        if old_name == new_name:
            MessageDialog.show_message('新名称与原名称相同，请重新输入。', '提示', self)
            self.rename_list()
            return
        if new_name == '' or new_name.isspace():
            MessageDialog.show_message('名称不能为空，请重新输入。', '提示', self)
            self.rename_list()
            return
        message = rename_list(old_name, new_name)
        if message == '重命名成功':
            self.update_lists()
        elif message == '新歌单已存在':
            MessageDialog.show_message('命名重复，请选择其他名称。', '提示', self)
            self.rename_list()  # 递归继续重命名
        elif message == '原歌单不存在':
            raise Exception(f'EditListsDialog中重命名失败: 原歌单不存在: {old_name}')
        else:
            raise Exception(f'EditListsDialog中重命名失败: 未知错误: {message}')


class EditDialog(QDialog):
    def __init__(self, origin_path, parent=None):
        super().__init__(parent)

        def init_dialog():
            # 设置窗口标题
            self.setWindowTitle('歌单管理')

            # 获取屏幕的宽度和高度
            screen = QApplication.desktop().screenGeometry()
            screen_width = screen.width()
            screen_height = screen.height()

            # 设置窗口的宽度和高度值
            window_width = int(screen_width / 3.5)
            window_height = int(screen_height / 1.5)

            # 设置窗口大小
            self.resize(window_width, window_height)
            self.setMinimumSize(window_width, window_height)

            # 设置窗口标志
            self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint)

            # 设置主窗口背景色
            palette = QPalette()
            if COLOR_MODE == 'LIGHT':
                palette.setColor(QPalette.Window, QColor(255, 255, 255))
            else:
                palette.setColor(QPalette.Window, QColor(43, 45, 48))
            self.setPalette(palette)

            # 窗口居中
            screen = QApplication.desktop().screenGeometry()
            size = self.geometry()
            self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
        init_dialog()

        self.origin_path = origin_path
        self.origin_dict = check(self.origin_path)
        if self.origin_dict is None:
            self.origin_path = 'main'
            self.origin_dict = check('main') # 如果指定路径的歌单不存在，尝试读取主歌单

        self.init_UI()
        self.init_layout()
        self.init_DARK_CSS()
        self.update_list()  # 添加数据到列表

    def init_UI(self):
        self.switch_button = QPushButton('切换歌单,' + f'当前:{self.origin_path}', self)
        self.switch_button.clicked.connect(self.read_file)  # 连接按钮点击事件到读取文件的方法

        self.edit_lists_button = QPushButton('编辑歌单', self)
        self.edit_lists_button.clicked.connect(self.run_edit_lists_dialog)

        self.list_widget = QListWidget()  # 创建列表控件

        # 创建页脚按钮
        self.move_button = QPushButton('移动')
        self.delete_button = QPushButton('删除')

        # 连接删除按钮的点击事件
        self.delete_button.clicked.connect(self.delete_selected_playlist)
        self.move_button.clicked.connect(self.move_playlist)

    def init_layout(self):
        # 使用垂直布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 顶部横向布局
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.switch_button,stretch=5)
        top_layout.addSpacing(1)
        top_layout.addWidget(self.edit_lists_button, stretch=1)
        main_layout.addLayout(top_layout)

        # 添加列表控件
        main_layout.addWidget(self.list_widget)

        # 创建页脚水平布局
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(15, 10, 15, 10)
        footer_layout.setSpacing(15)

        # 添加弹簧，使按钮靠右
        footer_layout.addStretch()

        # 添加移动按钮
        footer_layout.addWidget(self.move_button)
        # 添加删除按钮
        footer_layout.addWidget(self.delete_button)

        # 创建页脚容器
        footer_widget = QWidget()
        footer_widget.setLayout(footer_layout)
        footer_widget.setFixedHeight(100)  # 设置页脚固定高度

        # 添加页脚
        main_layout.addWidget(footer_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setLayout(main_layout)

    def update_list(self):
        """刷新整个滚动区域"""
        if self.origin_path not in check_lists():  # 如果当前歌单不存在，切换到主歌单
            self.origin_path = 'main'
            self.origin_dict = check('main')

        self.switch_button.setText('切换歌单,' + f'当前:{self.origin_path}')
        # 清除现有项
        self.list_widget.clear()

        # 添加数据到列表中
        playlists = list(self.origin_dict.keys())

        for playlist_name in playlists:
            # 创建标签显示歌曲名称
            label = QLabel(playlist_name)
            label.setStyleSheet('''
                QLabel {
                    color: white;
                    font-size: 22px;
                    background: transparent;
                    font-weight: bold;
                    padding-left: 15px;
                }
            ''')

            # 创建列表项
            list_item = QListWidgetItem(self.list_widget)
            # 设置项高度
            list_item.setSizeHint(QtCore.QSize(0, 70))

            # 将标签添加到列表项
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, label)

    def delete_selected_playlist(self):
        """删除选中的歌曲"""
        current_item = self.list_widget.currentItem()
        if current_item is not None:
            # 获取当前选中项中的标签控件
            label_widget = self.list_widget.itemWidget(current_item)
            if label_widget:
                playlist_name = label_widget.text()

                # 执行删除操作(如果是主歌单)
                if playlist_name in self.origin_dict and self.origin_path == 'main':
                    if MessageDialog.show_message("删除主歌单中的歌曲将把它从数据库移除，是否继续？",
                                                     title="警告",
                                                     parent=self,
                                                     show_cancel=True
                                                     ):
                        del self.origin_dict[playlist_name] # 从UI删除
                        self.update_list() # 刷新列表
                        for n in check_lists(): # 从所有歌单中删除
                            if playlist_name in list(check(n).keys()):
                                delete(n, playlist_name)
                        delete_from_db(playlist_name) # 从数据库中删除
                # 删除非主歌单中的歌曲
                elif playlist_name in self.origin_dict and self.origin_path != 'main':
                    del self.origin_dict[playlist_name] # 从UI删除
                    self.update_list() # 刷新列表
                    delete(self.origin_path, playlist_name) # 从歌单删除
                else:
                    print(f"歌曲不存在: {playlist_name}")
        else:
            MessageDialog.show_message('请选中要删除的歌曲', title='提示', parent=self)

    def move_playlist(self):
        """移动歌曲"""
        current_item = self.list_widget.currentItem()
        if current_item is not None: # 确保有选中项
            label_widget = self.list_widget.itemWidget(current_item)
            if label_widget:
                playlist_name = label_widget.text()
                # 让用户选择目标歌单
                dialog = SwitchListDialog(self.origin_path,self)
                if dialog.exec_() == QDialog.Accepted:
                    if dialog.selected_list != self.origin_path: # 确保目标歌单与当前歌单不同
                        if playlist_name in check(dialog.selected_list):
                            MessageDialog.show_message('此歌曲已在此歌单中', title='提示', parent=self)
                        else:
                            add(dialog.selected_list, playlist_name)  # 添加到目标歌单
                            MessageDialog.show_message(f'歌曲已成功移动到 {dialog.selected_list}', title='成功',
                                                       parent=self)
                    else:
                        MessageDialog.show_message('目标歌单与当前歌单相同，请选择不同的歌单', title='提示', parent=self)
                        self.move_playlist() # 递归重选
        else:
            MessageDialog.show_message('请选中要移动的歌曲', title='提示', parent=self)

    def init_DARK_CSS(self):
        self.switch_button.setStyleSheet('''
            QPushButton {
                background-color: #3574F0;
                border: none;
                font-size: 30px;
                color: white;
                min-height: 60px;
            }
            QPushButton:hover {
                background-color: darkblue;
            }
            QPushButton:pressed {
                background-color: darkblue;
                border: 10px groove darkblue;
            }
        ''')
        self.edit_lists_button.setStyleSheet('''
            QPushButton {
                background-color: #3574F0;
                border: none;
                font-size: 30px;
                color: white;
                min-height: 60px;
            }
            QPushButton:hover {
                background-color: darkblue;
            }
            QPushButton:pressed {
                background-color: darkblue;
                border: 10px groove darkblue;
            }
        ''')

        # 列表控件的样式
        self.list_widget.setStyleSheet('''
            QListWidget {
                background-color: #2D2D2D;
                border: none;
                outline: none;
            }
            QListWidget::item {
                border-bottom: 2px solid #3D3D3D;
                padding: 0px;
            }
            QListWidget::item:hover {
                background-color: #3D3D3D;
            }
            QListWidget::item:selected {
                background-color: #3574F0;
            }
        ''')

        # 页脚按钮样式 - 移动按钮
        self.move_button.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                border: none;
                border-radius: 8px;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 10px 20px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        ''')

        # 页脚按钮样式 - 删除按钮
        self.delete_button.setStyleSheet('''
            QPushButton {
                background-color: #FF4444;
                border: none;
                border-radius: 8px;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 10px 20px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #FF6666;
            }
            QPushButton:pressed {
                background-color: #CC3333;
            }
        ''')

        # 页脚背景色
        footer_style = """
            QWidget {
                background-color: #3D3D3D;
                border-top: 2px solid #4D4D4D;
            }
        """
        # 获取页脚控件并设置样式
        footer_widget = self.layout().itemAt(2).widget()
        if footer_widget:
            footer_widget.setStyleSheet(footer_style)

    def read_file(self):
        """点击顶部切换歌单按钮时调用"""
        try:
            dialog = SwitchListDialog(self.origin_path, self)
            if dialog.exec_() == QDialog.Accepted:
                print(f"用户选择了歌单: {dialog.selected_list}")
                self.origin_path = dialog.selected_list
                self.origin_dict = check(self.origin_path)
                self.update_list()  # 刷新列表显示新的歌单数据
            else:
                print("用户取消了选择")
        except Exception as e:
            MessageDialog.show_message(f"读取歌单失败: {str(e)}", title="错误", parent=self)

    def run_edit_lists_dialog(self):
        """点击编辑歌单按钮时调用"""
        try:
            dialog = EditListsDialog(self.origin_path, self)
            dialog.destroyed.connect(self.update_list)  # 当编辑歌单窗口关闭时刷新列表
            dialog.exec_()  # 显示编辑歌单的模态对话框
        except Exception as e:
            MessageDialog.show_message(f"打开编辑歌单窗口失败: {str(e)}", title="错误", parent=self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = EditDialog('main')
    dialog.exec_()  # 使用 exec_() 显示模态对话框
    sys.exit(app.exec_())