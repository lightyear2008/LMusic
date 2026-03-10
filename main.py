from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea

class StyledWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)
        # ------------------------------------------------------
        # 创建一个QWidget作为容器
        container = QWidget()
        # 创建容器的布局
        layout = QVBoxLayout(container)

        # 添加一些控件到容器的布局
        layout.addWidget(QLabel("这是一个标签"))
        self.button = QPushButton('按钮')
        self.button.setStyleSheet('''
            QPushButton {
                background: #FFFFFF;
            }
        ''')
        layout.addWidget(self.button)

        # 设置容器的样式（背景颜色和圆角）
        container.setAutoFillBackground(True)
        container.setStyleSheet("""
            QWidget {
                border-radius: 10px;
                background: #505050;
            }
        """)
        # ------------------------------------------------------
        # 将容器添加到主布局
        main_layout.addWidget(container)

        self.setLayout(main_layout)
        self.setWindowTitle('设置布局背景颜色和圆角')
        self.setGeometry(300, 300, 300, 200)
def run_1():
    import sys
    app = QApplication(sys.argv)
    ex = StyledWidget()
    ex.show()
    sys.exit(app.exec_())


# ---------------------------------------------------------------------------------------------------


class ScrollableListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建主垂直布局
        main_layout = QVBoxLayout(self)

        # 创建一个QScrollArea作为可滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # 设置可调整大小

        # 创建一个QWidget作为滚动区域的内容
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # 添加一些横向布局到滚动区域的内容
        for i in range(20):  # 假设我们有20个元素
            # 创建一个横向布局
            horizontal_layout = QHBoxLayout()

            # 创建一个标签和一个按钮
            label = QLabel(f"标签 {i+1}")
            button = QPushButton(f"按钮 {i+1}")

            # 将标签和按钮添加到横向布局
            horizontal_layout.addWidget(label)
            horizontal_layout.addWidget(button)

            # 将横向布局添加到滚动区域的布局中
            scroll_layout.addLayout(horizontal_layout)

        # 将滚动区域的内容添加到滚动区域中
        scroll_area.setWidget(scroll_content)

        # 将滚动区域添加到主布局中
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        self.setWindowTitle('可滚动列表示例')
        self.setGeometry(300, 300, 300, 200)
def run_2():
    import sys
    app = QApplication(sys.argv)
    ex = ScrollableListWidget()
    ex.show()
    sys.exit(app.exec_())




def climber_test():
    from climber import download_music
    print(download_music('https://er-sycdn.kuwo.cn/975b814b66d99a572712ffcc93d085ab/69aa48de/resource/30106/trackmedia/M500001ZlkyT2V5ZLg.mp3?bitrate$128&from=vip',''))

if __name__ == '__main__':
    climber_test()