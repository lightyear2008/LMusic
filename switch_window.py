from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QListWidget,
                             QListWidgetItem, QPushButton, QHBoxLayout, QLabel)
from PyQt5.QtCore import Qt

from dbcrudtool2 import check_lists


class SwitchListDialog(QDialog):
    def __init__(self, current_list_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("切换歌单")
        self.setModal(True)  # 设置为模态对话框
        self.setMinimumSize(500, 600)  # 使用最小尺寸
        self.resize(500, 600)  # 设置初始尺寸

        # 获取所有可用的歌单
        self.available_lists = self.get_available_lists()
        self.current_list = current_list_name
        self.selected_list = None

        self.initUI()
        self.initCSS()

    def get_available_lists(self):
        # 获取所有歌单名
        try:
            all_lists = check_lists()
            return all_lists
        except:
            # 如果出错，返回空列表或默认列表
            raise Exception('SwitchListDialog中获取歌单列表失败')

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # 提示标签
        tip_label = QLabel("请选择要切换的歌单：")
        tip_label.setObjectName("tip_label")
        tip_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(tip_label)

        # 歌单列表
        self.list_widget = QListWidget()
        self.list_widget.setObjectName("list_widget")
        for list_name in self.available_lists:
            item = QListWidgetItem(list_name)
            self.list_widget.addItem(item)
            # 标记当前使用的歌单
            if list_name == self.current_list:
                self.list_widget.setCurrentItem(item)
                item.setBackground(Qt.lightGray)

        self.list_widget.itemDoubleClicked.connect(self.accept_selection) # 双击项时直接确认选择
        layout.addWidget(self.list_widget)

        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        confirm_btn = QPushButton("确认")
        confirm_btn.setObjectName("confirm_btn")
        confirm_btn.clicked.connect(self.accept_selection)

        cancel_btn = QPushButton("取消")
        cancel_btn.setObjectName("cancel_btn")
        cancel_btn.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(confirm_btn)
        button_layout.addWidget(cancel_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def initCSS(self):
        self.setStyleSheet('''
            QDialog {
                background-color: #000000;
            }

            QLabel#tip_label {
                color: red;
                font-size: 20px;
                font-weight: bold;
                padding: 10px;
            }

            QListWidget#list_widget {
                background-color: #1a1a1a;
                border: 2px solid #333333;
                border-radius: 15px;
                color: lightblue;
                font-size: 18px;
                padding: 10px;
                outline: none;
            }

            QListWidget#list_widget::item {
                padding: 15px;
                border-radius: 8px;
                margin: 5px;
            }

            QListWidget#list_widget::item:selected {
                background-color: #3574F0;
                color: white;
            }

            QListWidget#list_widget::item:hover {
                background-color: #2a2a2a;
            }

            QPushButton#confirm_btn {
                background-color: #3574F0;
                border: none;
                border-radius: 25px;
                font-weight: bold;
                color: white;
                min-height: 50px;
                min-width: 120px;
                font-size: 18px;
            }

            QPushButton#confirm_btn:hover {
                background-color: #4584FF;
            }

            QPushButton#confirm_btn:pressed {
                background-color: #2564E0;
                border: 2px groove #0f172a;
            }

            QPushButton#cancel_btn {
                background-color: #555555;
                border: none;
                border-radius: 25px;
                font-weight: bold;
                color: white;
                min-height: 50px;
                min-width: 120px;
                font-size: 18px;
            }

            QPushButton#cancel_btn:hover {
                background-color: #666666;
            }

            QPushButton#cancel_btn:pressed {
                background-color: #444444;
                border: 2px groove #0f172a;
            }
        ''')

    def accept_selection(self):
        # 确认选择
        current_item = self.list_widget.currentItem()
        if current_item is not None:
            self.selected_list = current_item.text()
            self.accept()  # 关闭对话框并返回 QDialog.Accepted
        else:
            # 如果没有选择任何项，提示用户并返回，不关闭对话框
            from PyQt5.QtWidgets import QMessageBox
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("提示")
            msg_box.setText("请选择一个歌单")
            msg_box.setStyleSheet('''
                QMessageBox {
                    background-color: #000000;
                    color: white;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #3574F0;
                    border: none;
                    border-radius: 15px;
                    padding: 8px 25px;
                    color: white;
                    min-height: 35px;
                    min-width: 100px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #4584FF;
                }
            ''')
            msg_box.exec_()
            return


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = SwitchListDialog("list1")
    if dialog.exec_() == QDialog.Accepted:
        print(f"用户选择了歌单: {dialog.selected_list}")
    else:
        print("用户取消了选择")