import datetime
import datetime
import sys
import threading
import tkinter as tk
from tkinter import filedialog

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, \
    QGridLayout, QLabel, QPushButton, QVBoxLayout, QScrollArea

import adb_util
import util
from MyQWidget import MyQLineEdit
from apk_info import ApkInfo


class ApkTool:
    edit_apk_path: MyQLineEdit
    label_msg: QLabel
    label_control_msg: QLabel
    apk_info: ApkInfo = None
    buttons = []

    def __init__(self):
        super().__init__()
        self.show_window('Apk工具', 720, 580)

    def show_window(self, title, width, height):
        # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
        app = QApplication(sys.argv)
        # QWidget部件是pyqt5所有用户界面对象的基类。他为QWidget提供默认构造函数。默认构造函数没有父类。
        w = QWidget()
        # resize()方法调整窗口的大小
        w.resize(width, height)
        # 禁止窗体调整大小
        w.setFixedSize(width, height)
        # 获得窗口
        qr = w.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        w.move(qr.topLeft())

        # 设置窗口的标题
        w.setWindowTitle(title)

        self.add_content_view(w)

        # 显示在屏幕上
        w.show()
        # 系统exit()方法确保应用程序干净的退出
        # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
        sys.exit(app.exec_())

    # 加入全部子view
    def add_content_view(self, base_widget):
        q_v_box_layout = QVBoxLayout(base_widget)
        q_v_box_layout.setAlignment(Qt.AlignTop)
        q_v_box_layout.setContentsMargins(50, 60, 50, 60)
        q_v_box_layout.setSpacing(10)

        self.add_apk_path_view(q_v_box_layout)
        self.add_info_view(q_v_box_layout)
        self.add_control_info_view(q_v_box_layout)
        self.add_button(q_v_box_layout)

        base_widget.setLayout(q_v_box_layout)

    # APK路径
    def add_apk_path_view(self, q_v_box_layout):
        q_grid_layout = QGridLayout()
        q_grid_layout.setSpacing(30)

        title_label = QLabel('APK路径')
        q_push_button = QPushButton('选择')
        self.edit_apk_path = MyQLineEdit('.apk')
        self.edit_apk_path.setText('')
        self.edit_apk_path.textChanged.connect(self.apk_path_change)

        q_grid_layout.addWidget(title_label, 1, 0)
        q_grid_layout.addWidget(self.edit_apk_path, 1, 1)
        q_grid_layout.addWidget(q_push_button, 1, 2)

        q_push_button.clicked.connect(self.click_select_apk_path)
        q_v_box_layout.addLayout(q_grid_layout)

    def add_button(self, q_v_box_layout):
        q_grid_layout = QGridLayout()
        q_grid_layout.setSpacing(30)
        q_grid_layout.setContentsMargins(0, 50, 0, 0)

        q_push_button = QPushButton('启动ADB服务')
        self.buttons.append(q_push_button)
        q_push_button.setMinimumWidth(100)
        q_push_button.setMinimumHeight(58)
        q_push_button.clicked.connect(self.start_adb)
        q_grid_layout.addWidget(q_push_button, 1, 0)

        q_push_button = QPushButton('新安装APK')
        self.buttons.append(q_push_button)
        q_push_button.setMinimumWidth(100)
        q_push_button.setMinimumHeight(58)
        q_push_button.clicked.connect(self.new_install)
        q_grid_layout.addWidget(q_push_button, 1, 1)

        q_push_button = QPushButton('升级APK')
        self.buttons.append(q_push_button)
        q_push_button.setMinimumWidth(100)
        q_push_button.setMinimumHeight(58)
        q_push_button.clicked.connect(self.up_install)
        q_grid_layout.addWidget(q_push_button, 1, 2)

        q_push_button = QPushButton('卸载APP')
        self.buttons.append(q_push_button)
        q_push_button.setPalette(self.getColorPalette(Qt.red))
        q_push_button.setAutoFillBackground(True)
        q_push_button.setFlat(True)
        q_push_button.setMinimumWidth(100)
        q_push_button.setMinimumHeight(58)
        q_push_button.clicked.connect(self.delete_apk)
        q_grid_layout.addWidget(q_push_button, 2, 0)

        q_push_button = QPushButton('清APP数据')
        self.buttons.append(q_push_button)
        q_push_button.setPalette(self.getColorPalette(Qt.red))
        q_push_button.setAutoFillBackground(True)
        q_push_button.setFlat(True)
        q_push_button.setMinimumWidth(100)
        q_push_button.setMinimumHeight(58)
        q_push_button.clicked.connect(self.clear_app_data)
        q_grid_layout.addWidget(q_push_button, 2, 1)

        q_v_box_layout.addLayout(q_grid_layout)

    # 信息输出
    def add_info_view(self, q_v_box_layout):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setPalette(self.getColorPalette(Qt.white))
        scroll.setMaximumHeight(120)
        scroll.setMinimumHeight(120)

        self.label_msg = QLabel()
        self.label_msg.setContentsMargins(10, 2, 10, 0)
        self.label_msg.setWordWrap(True)
        self.label_msg.setAlignment(Qt.AlignTop)
        # 四倍行距
        self.label_msg.setGeometry(QRect(328, 240, 800, 27 * 100000))

        scroll.setAlignment(Qt.AlignTop)
        scroll.setWidget(self.label_msg)

        vbox = QVBoxLayout()
        vbox.addWidget(scroll)
        vbox.setContentsMargins(0, 30, 0, 0)
        q_v_box_layout.addLayout(vbox)

    # 操作信息输出
    def add_control_info_view(self, q_v_box_layout):
        self.label_control_msg = QLabel()
        q_v_box_layout.addWidget(self.label_control_msg)

    # 选择apk路径事件
    def click_select_apk_path(self):
        # 打开选择文件夹对话框
        root = tk.Tk()
        root.withdraw()

        # path = filedialog.askdirectory()  # 获得选择好的文件夹
        path = filedialog.askopenfilename()  # 获得选择好的文件
        if path.endswith('.apk'):
            self.edit_apk_path.setText(path)

    # 路径改变
    def apk_path_change(self):
        path = self.edit_apk_path.text()
        if path.lower().endswith('.apk'):
            threading.Thread(target=self.resolve_apk, args=(path,)).start()

    # 解析apk
    def resolve_apk(self, path):
        self.apk_info = None
        self.label_msg.setText('')
        self.apk_info = ApkInfo(path)
        self.add_msg('包名: ' + self.apk_info.package)
        self.add_msg('版本号: ' + self.apk_info.versionCode)
        self.add_msg('版本名: ' + self.apk_info.versionName)
        self.add_msg('\n')
        self.add_msg('详情: \n' + self.apk_info.text)

    def getColorPalette(self, qt_color):
        palette = QPalette()
        palette.setColor(QPalette.Button, qt_color)
        return palette

    def getTextPalette(self, qt_color):
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, qt_color)
        return palette

    # 输出信息
    def add_msg(self, msg):
        self.label_msg.setText(self.label_msg.text() + '\n' + msg)

    def set_control_msg(self, msg, state):
        now_time = datetime.datetime.now()
        time_str = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
        self.label_control_msg.setText('时间:' + time_str + ' , 操作: ' + msg + ' ,  状态: ' + state)

    def start_adb(self):
        def start():
            self.set_control_msg('启动ADB', '执行中')
            self.fix_button_state(False)
            adb_util.startAdbServer()
            self.fix_button_state(True)
            self.set_control_msg('启动ADB', '执行结束')

        threading.Thread(target=start).start()

    def new_install(self):
        if self.apk_info:
            def start():
                self.set_control_msg('安装应用', '执行中')
                self.fix_button_state(False)
                adb_util.installApk(self.apk_info.apk_path)
                adb_util.startApp(self.apk_info.apk_path)
                self.fix_button_state(True)
                self.set_control_msg('安装应用', '执行结束')

            threading.Thread(target=start).start()

    def up_install(self):
        if self.apk_info:
            def start():
                self.set_control_msg('升级应用', '执行中')
                self.fix_button_state(False)
                adb_util.reInstallApk(self.apk_info.apk_path)
                adb_util.startApp(self.apk_info.apk_path)
                self.fix_button_state(True)
                self.set_control_msg('升级应用', '执行结束')

            threading.Thread(target=start).start()

    def delete_apk(self):
        if self.apk_info:
            def start():
                self.set_control_msg('卸载应用', '执行中')
                self.fix_button_state(False)
                adb_util.uninstall(self.apk_info.package)
                self.fix_button_state(True)
                self.set_control_msg('卸载应用', '执行结束')

            threading.Thread(target=start).start()

    def clear_app_data(self):
        if self.apk_info:
            def start():
                self.set_control_msg('清除应用数据', '执行中')
                self.fix_button_state(False)
                adb_util.clear(self.apk_info.package)
                self.fix_button_state(True)
                self.set_control_msg('清除应用数据', '执行结束')

            threading.Thread(target=start).start()

    def fix_button_state(self, enable):
        for btn in self.buttons:
            btn.setEnabled(enable)


if __name__ == '__main__':
    ApkTool()
