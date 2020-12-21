#
import os
import sched
import threading
import time
import tkinter as tk
import traceback
from tkinter import filedialog

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QGridLayout, QLabel, QPushButton, QScrollArea, \
    QLineEdit, QComboBox, QCheckBox, QRadioButton

import adb_util
import util
from MyQDialog import MyQDialog
from MyQWidget import MyQLineEdit, MyQLineEWFileEdit
from apk_info import ApkInfo
from constant import KEY_CODE, KEY_CODE_FIRST_KEY
from event_bean import event_bean
from lang_util import Lang


class auto_event:
    popen_list = {}
    POPEN_CLICK_EVENT_NAME = "popen_click_event_name"
    apk_info = None
    edit_apk_path = None
    edit_config_path = None
    label_cmd_msg = None
    scroll_cmd = None
    scroll_config = None
    event_list = []
    old_apk_info = None
    cur_apk_info = None
    adb_state = False
    isDismiss = True
    scheduler = None
    isRecord = False
    isRun = False
    buttons = []
    key_code = KEY_CODE
    cur_key_code = key_code.get(KEY_CODE_FIRST_KEY)

    def __init__(self):
        super().__init__()
        self.scheduler = sched.scheduler()

    def set_adb_state(self, adb_state):
        self.adb_state = adb_state

    def show(self, old_apk_info=None):
        self.show_window("自动化事件", 1080, 850, old_apk_info)

    def dismiss(self, data):
        self.isRecord = False
        self.isDismiss = True
        self.isRun = False
        self.kill_popen()

    def show_window(self, title, width, height, old_apk_info=None):
        self.isDismiss = False
        self.old_apk_info = old_apk_info
        self.dialog = MyQDialog()
        self.dialog.signal_close.connect(self.dismiss)
        self.dialog.setWindowTitle(title)
        self.dialog.resize(width, height)
        self.dialog.setMaximumWidth(width)

        q_v_box_layout = QVBoxLayout()
        q_v_box_layout.setAlignment(Qt.AlignTop)
        q_v_box_layout.setContentsMargins(50, 30, 50, 60)
        q_v_box_layout.setSpacing(10)
        self.add_content_view(q_v_box_layout, width)

        self.dialog.setLayout(q_v_box_layout)
        # https://blog.csdn.net/u010058695/article/details/101011907
        self.dialog.setWindowModality(Qt.WindowModal)  # 该模式下，只有该dialog关闭，才可以关闭父界面
        self.dialog.exec_()

    # 加入全部子view
    def add_content_view(self, q_v_box_layout, width):
        self.add_apk_path_view(q_v_box_layout)
        self.add_config_path_view(q_v_box_layout)
        self.add_cmd_info_view(q_v_box_layout)
        self.add_config_info_view(q_v_box_layout, width)
        self.add_button_event_view(q_v_box_layout)
        self.add_click_event_view(q_v_box_layout)
        self.add_swipe_event_view(q_v_box_layout)
        self.add_input_event_view(q_v_box_layout)
        self.add_export_path_view(q_v_box_layout)
        self.add_export_type_view(q_v_box_layout)
        self.add_control_view(q_v_box_layout)

    # APK路径
    def add_apk_path_view(self, q_v_box_layout):
        q_grid_layout = QGridLayout()
        q_grid_layout.setSpacing(30)

        title_label = QLabel('APK路径')
        title_label.setMinimumWidth(60)
        title_label.setMinimumHeight(38)
        q_push_button = QPushButton('选择')
        q_push_button.setMinimumHeight(38)
        self.edit_apk_path = MyQLineEdit()
        self.edit_apk_path.setMinimumHeight(38)
        self.edit_apk_path.setText('')
        self.edit_apk_path.textChanged.connect(self.apk_path_change)

        q_grid_layout.addWidget(title_label, 1, 0)
        q_grid_layout.addWidget(self.edit_apk_path, 1, 1)
        q_grid_layout.addWidget(q_push_button, 1, 2)

        q_push_button.clicked.connect(self.click_select_apk_path)
        q_v_box_layout.addLayout(q_grid_layout)

    # 配置路径
    def add_config_path_view(self, q_v_box_layout):
        q_grid_layout = QGridLayout()
        q_grid_layout.setSpacing(30)

        title_label = QLabel('配置')
        title_label.setMinimumWidth(60)
        title_label.setMinimumHeight(38)
        q_push_button = QPushButton('选择')
        q_push_button.setMinimumHeight(38)
        self.buttons.append(q_push_button)

        self.edit_config_path = MyQLineEWFileEdit()
        self.edit_config_path.setMinimumHeight(38)
        self.edit_config_path.setText('')
        self.edit_config_path.textChanged.connect(self.config_path_change)
        self.buttons.append(self.edit_config_path)

        q_grid_layout.addWidget(title_label, 1, 0)
        q_grid_layout.addWidget(self.edit_config_path, 1, 1)
        q_grid_layout.addWidget(q_push_button, 1, 2)

        q_push_button.clicked.connect(self.click_select_config_path)
        q_v_box_layout.addLayout(q_grid_layout)

    # 信息输出
    def add_cmd_info_view(self, q_v_box_layout):
        self.scroll_cmd = QScrollArea()
        self.scroll_cmd.setWidgetResizable(True)
        self.scroll_cmd.setPalette(self.getColorPalette(Qt.white))
        self.scroll_cmd.setMaximumHeight(150)
        self.scroll_cmd.setMinimumHeight(150)

        self.label_cmd_msg = QLabel(" ")  # 空格占位，否则setTextInteractionFlags会报错
        self.label_cmd_msg.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        self.label_cmd_msg.setContentsMargins(10, 2, 10, 0)
        self.label_cmd_msg.setWordWrap(True)
        self.label_cmd_msg.setAlignment(Qt.AlignTop)
        # 四倍行距
        self.label_cmd_msg.setGeometry(QRect(328, 240, 800, 27 * 100000))

        self.scroll_cmd.setAlignment(Qt.AlignTop)
        self.scroll_cmd.setWidget(self.label_cmd_msg)

        vbox = QVBoxLayout()
        vbox.addWidget(self.scroll_cmd)
        vbox.setContentsMargins(0, 30, 0, 0)
        q_v_box_layout.addLayout(vbox)

    # 配置输出
    def add_config_info_view(self, q_v_box_layout, max_width):
        self.scroll_config = QScrollArea()
        self.scroll_config.setWidgetResizable(True)
        self.scroll_config.setPalette(self.getColorPalette(Qt.white))
        self.scroll_config.setMaximumHeight(150)
        self.scroll_config.setMinimumHeight(150)

        self.label_config_msg = QLabel(" ")  # 空格占位，否则setTextInteractionFlags会报错
        self.label_config_msg.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        self.label_config_msg.setContentsMargins(10, 2, 10, 0)
        self.label_config_msg.setWordWrap(True)
        self.label_config_msg.setAlignment(Qt.AlignTop)
        # # 四倍行距
        self.label_config_msg.setGeometry(QRect(328, 240, 800, 27 * 100000))

        self.scroll_config.setAlignment(Qt.AlignTop)
        self.scroll_config.setWidget(self.label_config_msg)

        vbox = QVBoxLayout()
        vbox.addWidget(self.scroll_config)
        vbox.setContentsMargins(0, 30, 0, 0)
        q_v_box_layout.addLayout(vbox)

    # 按键
    def add_button_event_view(self, q_v_box_layout):
        q_grid_layout = QGridLayout()
        q_grid_layout.setContentsMargins(0, 50, 0, 0)
        q_grid_layout.setSpacing(30)

        title_label = QLabel('按键事件')
        title_label.setMinimumWidth(60)
        title_label.setMinimumHeight(38)

        combo = self.get_btn_event_QComboBox()

        self.edit_btn_event_time = QLineEdit()
        self.edit_btn_event_time.setPlaceholderText("time(ms)")
        self.edit_btn_event_time.setText("1000")
        self.edit_btn_event_time.setAlignment(Qt.AlignCenter)
        self.edit_btn_event_time.setMinimumWidth(50)
        self.edit_btn_event_time.setMinimumHeight(38)

        q_push_button_1 = QPushButton('测试')
        q_push_button_1.setMinimumWidth(100)
        q_push_button_1.setMaximumWidth(100)
        q_push_button_1.setMinimumHeight(38)
        q_push_button_1.clicked.connect(self.click_test_button_event)
        self.buttons.append(q_push_button_1)

        q_push_button_2 = QPushButton('插入')
        q_push_button_2.setMinimumWidth(100)
        q_push_button_2.setMaximumWidth(100)
        q_push_button_2.setMinimumHeight(38)
        q_push_button_2.clicked.connect(self.click_insert_button_event)
        self.buttons.append(q_push_button_2)

        q_grid_layout.addWidget(title_label, 1, 0)
        q_grid_layout.addWidget(combo, 1, 1)
        q_grid_layout.addWidget(self.edit_btn_event_time, 1, 2)
        q_grid_layout.addWidget(q_push_button_1, 1, 3)
        q_grid_layout.addWidget(q_push_button_2, 1, 4)

        q_v_box_layout.addLayout(q_grid_layout)

    # 点击事件
    def add_click_event_view(self, q_v_box_layout):
        q_grid_layout = QGridLayout()
        q_grid_layout.setSpacing(30)

        title_label = QLabel('点击事件')
        title_label.setMinimumWidth(60)
        title_label.setMinimumHeight(38)

        self.edit_click_event_x = QLineEdit()
        self.edit_click_event_x.setPlaceholderText("x")
        self.edit_click_event_x.setAlignment(Qt.AlignCenter)
        self.edit_click_event_x.setMinimumWidth(50)
        self.edit_click_event_x.setMinimumHeight(38)

        self.edit_click_event_y = QLineEdit()
        self.edit_click_event_y.setAlignment(Qt.AlignCenter)
        self.edit_click_event_y.setPlaceholderText("y")
        self.edit_click_event_y.setMinimumWidth(50)
        self.edit_click_event_y.setMinimumHeight(38)

        self.edit_click_event_time = QLineEdit()
        # self.edit_click_event_time.setValidator(QIntValidator(0, 65535))
        self.edit_click_event_time.setPlaceholderText("time(ms)")
        self.edit_click_event_time.setText("1000")
        self.edit_click_event_time.setAlignment(Qt.AlignCenter)
        self.edit_click_event_time.setMinimumWidth(50)
        self.edit_click_event_time.setMinimumHeight(38)

        q_push_button_1 = QPushButton('测试')
        q_push_button_1.setMinimumWidth(100)
        q_push_button_1.setMaximumWidth(100)
        q_push_button_1.setMinimumHeight(38)
        q_push_button_1.clicked.connect(self.click_test_tap_event)
        self.buttons.append(q_push_button_1)

        q_push_button_2 = QPushButton('插入')
        q_push_button_2.setMinimumWidth(100)
        q_push_button_2.setMaximumWidth(100)
        q_push_button_2.setMinimumHeight(38)
        q_push_button_2.clicked.connect(self.click_insert_tap_event)
        self.buttons.append(q_push_button_2)

        q_grid_layout.addWidget(title_label, 1, 0)
        q_grid_layout.addWidget(self.edit_click_event_x, 1, 1)
        q_grid_layout.addWidget(self.edit_click_event_y, 1, 2)
        q_grid_layout.addWidget(self.edit_click_event_time, 1, 3)
        q_grid_layout.addWidget(q_push_button_1, 1, 4)
        q_grid_layout.addWidget(q_push_button_2, 1, 5)

        q_v_box_layout.addLayout(q_grid_layout)

    # 滑动事件
    def add_swipe_event_view(self, q_v_box_layout):
        q_grid_layout = QGridLayout()
        q_grid_layout.setSpacing(30)

        title_label = QLabel('滑动事件')
        title_label.setMinimumWidth(60)
        title_label.setMinimumHeight(38)

        self.edit_swipe_event_x = QLineEdit()
        self.edit_swipe_event_x.setPlaceholderText("x1")
        self.edit_swipe_event_x.setAlignment(Qt.AlignCenter)
        self.edit_swipe_event_x.setMinimumWidth(50)
        self.edit_swipe_event_x.setMinimumHeight(38)

        self.edit_swipe_event_y = QLineEdit()
        self.edit_swipe_event_y.setAlignment(Qt.AlignCenter)
        self.edit_swipe_event_y.setPlaceholderText("y1")
        self.edit_swipe_event_y.setMinimumWidth(50)
        self.edit_swipe_event_y.setMinimumHeight(38)

        self.edit_swipe_event_x_2 = QLineEdit()
        self.edit_swipe_event_x_2.setPlaceholderText("x2")
        self.edit_swipe_event_x_2.setAlignment(Qt.AlignCenter)
        self.edit_swipe_event_x_2.setMinimumWidth(50)
        self.edit_swipe_event_x_2.setMinimumHeight(38)

        self.edit_swipe_event_y_2 = QLineEdit()
        self.edit_swipe_event_y_2.setAlignment(Qt.AlignCenter)
        self.edit_swipe_event_y_2.setPlaceholderText("y2")
        self.edit_swipe_event_y_2.setMinimumWidth(50)
        self.edit_swipe_event_y_2.setMinimumHeight(38)

        self.edit_swipe_event_time = QLineEdit()
        # self.edit_click_event_time.setValidator(QIntValidator(0, 65535))
        self.edit_swipe_event_time.setPlaceholderText("time(ms)")
        self.edit_swipe_event_time.setText("1000")
        self.edit_swipe_event_time.setAlignment(Qt.AlignCenter)
        self.edit_swipe_event_time.setMinimumWidth(50)
        self.edit_swipe_event_time.setMinimumHeight(38)

        q_push_button_1 = QPushButton('测试')
        q_push_button_1.setMinimumWidth(100)
        q_push_button_1.setMinimumHeight(38)
        q_push_button_1.setMaximumWidth(100)
        q_push_button_1.clicked.connect(self.click_test_swipe_event)
        self.buttons.append(q_push_button_1)

        q_push_button_2 = QPushButton('插入')
        q_push_button_2.setMinimumWidth(100)
        q_push_button_2.setMaximumWidth(100)
        q_push_button_2.setMinimumHeight(38)
        q_push_button_2.clicked.connect(self.click_insert_swipe_event)
        self.buttons.append(q_push_button_2)

        q_grid_layout.addWidget(title_label, 1, 0)
        q_grid_layout.addWidget(self.edit_swipe_event_x, 1, 1)
        q_grid_layout.addWidget(self.edit_swipe_event_y, 1, 2)
        q_grid_layout.addWidget(self.edit_swipe_event_x_2, 1, 3)
        q_grid_layout.addWidget(self.edit_swipe_event_y_2, 1, 4)
        q_grid_layout.addWidget(self.edit_swipe_event_time, 1, 5)
        q_grid_layout.addWidget(q_push_button_1, 1, 6)
        q_grid_layout.addWidget(q_push_button_2, 1, 7)

        q_v_box_layout.addLayout(q_grid_layout)

    # 文本输入
    def add_input_event_view(self, q_v_box_layout):
        q_grid_layout = QGridLayout()
        q_grid_layout.setSpacing(30)

        title_label = QLabel('输入事件')
        title_label.setMinimumWidth(60)
        title_label.setMinimumHeight(38)

        self.edit_input_event = QLineEdit()
        self.edit_input_event.setPlaceholderText("文本")
        self.edit_input_event.setAlignment(Qt.AlignCenter)
        self.edit_input_event.setMinimumWidth(150)
        self.edit_input_event.setMinimumHeight(38)

        self.edit_input_event_time = QLineEdit()
        # self.edit_click_event_time.setValidator(QIntValidator(0, 65535))
        self.edit_input_event_time.setPlaceholderText("time(ms)")
        self.edit_input_event_time.setText("1000")
        self.edit_input_event_time.setAlignment(Qt.AlignCenter)
        self.edit_input_event_time.setMinimumWidth(50)
        self.edit_input_event_time.setMinimumHeight(38)

        q_push_button_1 = QPushButton('测试')
        q_push_button_1.setMinimumWidth(100)
        q_push_button_1.setMaximumWidth(100)
        q_push_button_1.setMinimumHeight(38)
        q_push_button_1.clicked.connect(self.click_test_input_event)
        self.buttons.append(q_push_button_1)

        q_push_button_2 = QPushButton('插入')
        q_push_button_2.setMinimumWidth(100)
        q_push_button_2.setMaximumWidth(100)
        q_push_button_2.setMinimumHeight(38)
        q_push_button_2.clicked.connect(self.click_insert_input_event)
        self.buttons.append(q_push_button_2)

        q_grid_layout.addWidget(title_label, 1, 0)
        q_grid_layout.addWidget(self.edit_input_event, 1, 1)
        q_grid_layout.addWidget(self.edit_input_event_time, 1, 2)
        q_grid_layout.addWidget(q_push_button_1, 1, 3)
        q_grid_layout.addWidget(q_push_button_2, 1, 4)

        q_v_box_layout.addLayout(q_grid_layout)

    # 配置导出路径
    def add_export_path_view(self, q_v_box_layout):
        q_grid_layout = QGridLayout()
        q_grid_layout.setContentsMargins(0, 30, 0, 0)
        q_grid_layout.setSpacing(30)

        title_label = QLabel('导出路径')
        title_label.setMinimumWidth(60)
        title_label.setMinimumHeight(38)

        q_push_button = QPushButton('选择')
        q_push_button.setMinimumWidth(100)
        q_push_button.setMaximumWidth(100)
        q_push_button.setMinimumHeight(38)

        q_push_button_2 = QPushButton('导出配置')
        q_push_button_2.setMinimumWidth(100)
        q_push_button_2.setMaximumWidth(100)
        q_push_button_2.setMinimumHeight(38)
        q_push_button_2.clicked.connect(self.export_config)

        self.edit_export_path = MyQLineEWFileEdit()
        self.edit_export_path.setMinimumHeight(38)
        self.edit_export_path.setText('')
        self.edit_export_path.setPlaceholderText("文件后缀以.ew结尾")
        # self.edit_export_path.textChanged.connect(self.apk_path_change)

        q_grid_layout.addWidget(title_label, 1, 0)
        q_grid_layout.addWidget(self.edit_export_path, 1, 1)
        q_grid_layout.addWidget(q_push_button, 1, 2)
        q_grid_layout.addWidget(q_push_button_2, 1, 3)

        q_push_button.clicked.connect(self.click_select_export_path)
        q_v_box_layout.addLayout(q_grid_layout)

    # 导出类型
    def add_export_type_view(self, q_v_box_layout):
        q_grid_layout = QGridLayout()
        q_grid_layout.setSpacing(30)

        title_label = QLabel('执行设置')
        title_label.setMinimumWidth(60)
        title_label.setMinimumHeight(38)

        self.edit_lang_wait_time = QLineEdit()
        # self.edit_click_event_time.setValidator(QIntValidator(0, 65535))
        self.edit_lang_wait_time.setPlaceholderText("启动等待time(ms)")
        self.edit_lang_wait_time.setText("3000")
        self.edit_lang_wait_time.setAlignment(Qt.AlignCenter)
        self.edit_lang_wait_time.setMinimumWidth(50)
        self.edit_lang_wait_time.setMinimumHeight(38)

        self.edit_run_count = QLineEdit()
        # self.edit_click_event_time.setValidator(QIntValidator(0, 65535))
        self.edit_run_count.setPlaceholderText("执行次数")
        self.edit_run_count.setText("1")
        self.edit_run_count.setAlignment(Qt.AlignCenter)
        self.edit_run_count.setMinimumWidth(50)
        self.edit_run_count.setMinimumHeight(38)

        self.lang_q_check_box = QRadioButton("语言")
        self.default_q_check_box = QRadioButton("默认")
        self.default_q_check_box.setChecked(True)

        q_grid_layout.addWidget(title_label, 1, 0)
        q_grid_layout.addWidget(self.lang_q_check_box, 1, 1)
        q_grid_layout.addWidget(self.default_q_check_box, 1, 2)
        q_grid_layout.addWidget(self.edit_lang_wait_time, 1, 3)
        q_grid_layout.addWidget(self.edit_run_count, 1, 4)

        q_v_box_layout.addLayout(q_grid_layout)

    # 控制区
    def add_control_view(self, q_v_box_layout):
        q_grid_layout = QGridLayout()
        q_grid_layout.setContentsMargins(0, 20, 0, 0)
        q_grid_layout.setSpacing(30)

        q_push_button = QPushButton('回退事件')
        q_push_button.setMinimumWidth(100)
        q_push_button.setMinimumHeight(50)
        q_push_button.clicked.connect(self.delete_last_event)
        self.buttons.append(q_push_button)

        self.q_push_button_record = QPushButton('读取坐标')
        self.q_push_button_record.setMinimumWidth(100)
        self.q_push_button_record.setMinimumHeight(50)
        self.q_push_button_record.clicked.connect(self.click_record_event)

        self.q_push_button_run = QPushButton('开始执行')
        self.q_push_button_run.setMinimumWidth(100)
        self.q_push_button_run.setMinimumHeight(50)
        self.q_push_button_run.clicked.connect(self.click_run)

        q_grid_layout.addWidget(q_push_button, 1, 0)
        q_grid_layout.addWidget(self.q_push_button_record, 1, 1)
        q_grid_layout.addWidget(self.q_push_button_run, 1, 2)

        q_v_box_layout.addLayout(q_grid_layout)

    def get_btn_event_QComboBox(self):
        combo = QComboBox()
        combo.setMaximumWidth(250)
        combo.setMinimumWidth(250)
        combo.setMinimumHeight(38)
        combo.setContentsMargins(30, 10, 10, 10)
        for name in self.key_code.keys():
            combo.addItem(name)
        combo.activated[str].connect(self.onActivatedBtnEvent)
        return combo

    def onActivatedBtnEvent(self, name):
        self.cur_key_code = self.key_code.get(name)

    # 路径改变
    def apk_path_change(self):
        path = self.edit_apk_path.text()
        if path.lower().endswith('.apk') or path.lower().endswith('.apks'):
            threading.Thread(target=self.resolve_apk, args=(path,)).start()

    # 解析apk
    def resolve_apk(self, path):
        self.cur_apk_info = None
        self.cur_apk_info = ApkInfo(path)
        self.add_msg('包名: ' + self.cur_apk_info.package)
        self.add_msg('版本号: ' + self.cur_apk_info.versionCode)
        self.add_msg('版本名: ' + self.cur_apk_info.versionName)

    # 选择apk路径事件
    def click_select_apk_path(self):
        # 打开选择文件夹对话框
        root = tk.Tk()
        root.withdraw()

        # path = filedialog.askdirectory()  # 获得选择好的文件夹
        path = filedialog.askopenfilename()  # 获得选择好的文件
        if path.lower().endswith('.apk') or path.lower().endswith('.apks'):
            self.edit_apk_path.setText(path)

    # 路径改变
    def config_path_change(self):
        path = self.edit_config_path.text()
        if path.lower().endswith('.ew'):
            threading.Thread(target=self.resolve_config, args=(path,)).start()

    # 解析config
    def resolve_config(self, path):
        if os.path.exists(path):
            self.event_list = []
            f = open(path, "r", encoding="utf-8")
            lines = f.readlines()
            f.close()
            try:
                length = len(lines)
                if length > 0:
                    for i in range(length):
                        content = lines[i].replace("\n", "")
                        if content is "":
                            continue
                        sp = content.split(' ')
                        bean = event_bean()
                        bean.event_type = int(sp[0])
                        bean.time = int(sp[1])
                        if bean.event_type is 0:
                            bean.key_code = sp[2]
                        elif bean.event_type is 1:
                            values = sp[2].split(',')
                            bean.event_pos = [int(values[0]), int(values[1])]
                        elif bean.event_type is 2:
                            values = sp[2].split(',')
                            bean.event_pos = [int(values[0]), int(values[1]), int(values[2]), int(values[3])]
                        elif bean.event_type is 3:
                            bean.text = sp[2]
                        self.event_list.append(bean)
                    self.add_msg("导入成功:" + path)
                    self.up_config_msg()
            except Exception as e:
                self.add_msg("解析配置异常")

    # 选择配置路径事件
    def click_select_config_path(self):
        # 打开选择文件夹对话框
        root = tk.Tk()
        root.withdraw()

        # path = filedialog.askdirectory()  # 获得选择好的文件夹
        path = filedialog.askopenfilename()  # 获得选择好的文件
        if path.endswith('.ew'):
            self.edit_config_path.setText(path)

    # 选择.ew路径事件
    def click_select_export_path(self):
        # 打开选择文件夹对话框
        root = tk.Tk()
        root.withdraw()

        # path = filedialog.askdirectory()  # 获得选择好的文件夹
        path = filedialog.askopenfilename()  # 获得选择好的文件
        if path.endswith('.ew'):
            self.edit_export_path.setText(path)

    def getColorPalette(self, qt_color):
        palette = QPalette()
        palette.setColor(QPalette.Button, qt_color)
        return palette

    def open_click_event_listener(self):
        def start():
            p = adb_util.get_click_event_popen()
            self.kill(self.POPEN_CLICK_EVENT_NAME)
            self.popen_list.setdefault(self.POPEN_CLICK_EVENT_NAME, p)
            while self.isRecord and self.popen_list.get(self.POPEN_CLICK_EVENT_NAME):
                content = p.stdout.readline().decode("gbk").strip()
                # 先去除每一行末尾的制表符和换行符，然后再加上换行符，使写入文件中的内容不会有空行
                if content.find("0035") is not -1:
                    value = content.split(' ')[3]  # 宽
                    self.edit_click_event_x.setText(str(int(value, 16)))
                elif content.find("0036") is not -1:
                    value = content.split(' ')[3]  # 高
                    self.edit_click_event_y.setText(str(int(value, 16)))
            p.kill()

        if self.adb_state:
            threading.Thread(target=start).start()

    def delete_last_event(self):
        length = len(self.event_list)
        if length > 0:
            bean = self.event_list.pop(length - 1)
            self.add_msg('删除事件 : ' + self.get_event_text(bean))
            self.up_config_msg()

    def click_record_event(self):
        if self.isRecord:
            self.isRecord = False
            self.kill(self.POPEN_CLICK_EVENT_NAME)
            self.q_push_button_record.setText("读取坐标")
            self.q_push_button_run.setEnabled(True)
        else:
            if self.adb_state is False:
                return
            self.isRecord = True
            self.q_push_button_record.setText("停止读取")
            self.open_click_event_listener()
            self.q_push_button_run.setEnabled(False)

    def kill_popen(self):
        for p in self.popen_list.values():
            p.kill()
        self.popen_list.clear()

    # kill popen通道
    def kill(self, name):
        if self.popen_list.get(name):
            self.popen_list.get(name).kill()
            self.popen_list.pop(name)

    # 输出信息
    def add_msg(self, msg):
        self.label_cmd_msg.setText(self.label_cmd_msg.text() + '\n' + msg)
        self.scheduler.enter(0.01, 0, self.up_scroll_cmd_view)
        self.scheduler.run()

    def up_scroll_cmd_view(self):
        self.scroll_cmd.verticalScrollBar().setValue(self.scroll_cmd.verticalScrollBar().maximum())

    def add_config_msg(self, msg, clear=False):
        if clear:
            self.label_config_msg.setText(msg)
        else:
            self.label_config_msg.setText(self.label_config_msg.text() + '\n' + msg)
        self.scheduler.enter(0.01, 0, self.up_scroll_config_view)
        self.scheduler.run()

    def up_scroll_config_view(self):
        self.scroll_config.verticalScrollBar().setValue(self.scroll_config.verticalScrollBar().maximum())

    def click_test_button_event(self):
        adb_util.click_keyevent(self.cur_key_code)
        self.add_msg("测试按键： " + str(self.cur_key_code))

    def click_insert_button_event(self):
        bean = event_bean()
        bean.event_type = 0
        bean.key_code = self.cur_key_code
        bean.time = self.get_edit_value(self.edit_btn_event_time)
        self.event_list.append(bean)
        self.add_msg("插入按键： " + str(self.cur_key_code))
        self.up_config_msg()

    def click_test_tap_event(self):
        x = self.get_edit_value(self.edit_click_event_x)
        y = self.get_edit_value(self.edit_click_event_y)
        msg = adb_util.click_tap(x, y)
        self.add_msg("测试点击： " + str(x) + ',' + str(y) + '  ' + msg)

    def click_insert_tap_event(self):
        x = self.get_edit_value(self.edit_click_event_x)
        y = self.get_edit_value(self.edit_click_event_y)
        bean = event_bean()
        bean.event_type = 1
        bean.event_pos = [x, y]
        bean.time = self.get_edit_value(self.edit_click_event_time)
        self.event_list.append(bean)
        self.add_msg("插入点击： " + str(x) + ',' + str(y))
        self.up_config_msg()

    def click_test_swipe_event(self):
        x = self.get_edit_value(self.edit_swipe_event_x)
        y = self.get_edit_value(self.edit_swipe_event_y)
        x2 = self.get_edit_value(self.edit_swipe_event_x_2)
        y2 = self.get_edit_value(self.edit_swipe_event_y_2)
        adb_util.click_swipe(x, y, x2, y2, 300)
        self.add_msg("测试滑动： " + str(x) + ',' + str(y) + ' ' + str(x2) + ',' + str(y2))

    def click_insert_swipe_event(self):
        x = self.get_edit_value(self.edit_swipe_event_x)
        y = self.get_edit_value(self.edit_swipe_event_y)
        x2 = self.get_edit_value(self.edit_swipe_event_x_2)
        y2 = self.get_edit_value(self.edit_swipe_event_y_2)
        bean = event_bean()
        bean.event_type = 2
        bean.event_pos = [x, y, x2, y2]
        bean.time = self.get_edit_value(self.edit_swipe_event_time)
        self.event_list.append(bean)
        self.add_msg("插入滑动： " + str(x) + ',' + str(y) + ' ' + str(x2) + ',' + str(y2))
        self.up_config_msg()

    def click_test_input_event(self):
        text = self.edit_input_event.text()
        adb_util.event_input(text)
        self.add_msg("测试输入： " + text)

    def click_insert_input_event(self):
        text = self.edit_input_event.text()
        bean = event_bean()
        bean.event_type = 3
        bean.text = text
        bean.time = self.get_edit_value(self.edit_input_event_time)
        self.event_list.append(bean)
        self.add_msg("插入输入： " + text)
        self.up_config_msg()

    def up_config_msg(self):
        self.label_config_msg.setText("")
        for bean in self.event_list:
            self.add_config_msg(self.get_event_text(bean))

    def get_event_text(self, bean):
        text = ''
        if bean.event_type is 0:
            text = "0 " + str(bean.time) + ' ' + str(bean.key_code)
        elif bean.event_type is 1:
            text = "1 " + str(bean.time) + ' ' + str(bean.event_pos[0]) + ',' + str(bean.event_pos[1])
        elif bean.event_type is 2:
            text = "2 " + str(bean.time) + ' ' + str(bean.event_pos[0]) + ',' + str(bean.event_pos[1]) + ',' + str(
                bean.event_pos[2]) + ',' + str(bean.event_pos[3])
        elif bean.event_type is 3:
            text = "3 " + str(bean.time) + ' ' + bean.text
        return text

    def export_config(self):
        path = self.edit_export_path.text()

        def start():
            util.delete_file(path)
            f = open(path, "w", encoding="utf-8")
            for bean in self.event_list:
                f.write(self.get_event_text(bean) + '\n')
            f.flush()
            f.close()
            self.add_msg("导出成功:" + path)

        if path is not "":
            threading.Thread(target=start).start()

    def click_run(self):
        if self.isRun:
            self.isRun = False
            self.kill(self.POPEN_CLICK_EVENT_NAME)
            self.q_push_button_run.setText("开始执行")
            self.q_push_button_record.setEnabled(True)
            self.fix_button_state(True)
        else:
            if self.adb_state is False:
                return
            self.isRun = True
            self.q_push_button_run.setText("停止执行")
            self.q_push_button_record.setEnabled(False)
            self.fix_button_state(False)
            self.run_auto_task()

    def run_auto_task(self):
        def start():
            pkg = None
            launchable = None
            start_wait_time = self.get_edit_value(self.edit_lang_wait_time, 3000)
            run_count = self.get_edit_value(self.edit_run_count, 1)

            cur_apk_path = self.edit_apk_path.text()
            focus_pkg = adb_util.get_focus_app_pkg()
            if cur_apk_path is None and self.cur_apk_info is not None:
                pkg = self.cur_apk_info.package
                launchable = self.cur_apk_info.launchable
            elif focus_pkg is not None:
                pkg = focus_pkg
                launchable = adb_util.get_launcher(pkg)
            elif self.old_apk_info is not None:
                pkg = self.old_apk_info.package
                launchable = self.old_apk_info.launchable

            if pkg is not None:
                is_default = self.default_q_check_box.isChecked()
                is_lang = self.lang_q_check_box.isChecked()
                if is_default:
                    self.run_default_task(pkg, launchable, start_wait_time, run_count)
                elif is_lang:
                    self.run_lang_task(pkg, launchable, start_wait_time, run_count)

            if self.isRun:
                self.add_msg("执行自动完成")
                self.click_run()

        if len(self.event_list) > 0:
            run_thread = threading.Thread(target=start)
            run_thread.start()
        elif self.isRun:
            self.add_msg("没有自动事件")
            self.click_run()

    def run_default_task(self, pkg, launchable, start_wait_time, run_count):
        for i in range(run_count):
            adb_util.stop_app(pkg)
            adb_util.start_App(pkg, launchable)
            self.is_focus_pkg(pkg)
            self.wait(start_wait_time)
            for bean in self.event_list:
                self.is_focus_pkg(pkg)
                if self.isRun is False:
                    return
                self.run_event_bean(bean)
                if self.isRun is False:
                    return

    def run_lang_task(self, pkg, launchable, start_wait_time, run_count):
        lang: Lang = Lang()
        lang_list = lang.get_lang_config()
        adb_util.startApp(lang.apk_path)
        self.wait(start_wait_time)
        for i in range(run_count):
            for lan in lang_list:
                if self.isRun is False:
                    return
                lang.change_language(lan.locale)
                self.add_msg("切换语言: " + lan.name)
                adb_util.stop_app(pkg)
                adb_util.start_App(pkg, launchable)
                self.is_focus_pkg(pkg)
                self.wait(start_wait_time)
                for bean in self.event_list:
                    self.is_focus_pkg(pkg)
                    if self.isRun is False:
                        return
                    self.run_event_bean(bean)
                    if self.isRun is False:
                        return

    def run_event_bean(self, bean):
        self.add_msg("执行: " + str(bean.event_type))
        if bean.event_type is 0:
            adb_util.click_keyevent(bean.key_code)
        elif bean.event_type is 1:
            adb_util.click_tap(bean.event_pos[0], bean.event_pos[1])
        elif bean.event_type is 2:
            adb_util.click_swipe(bean.event_pos[0], bean.event_pos[1], bean.event_pos[2], bean.event_pos[3], 300)
        elif bean.event_type is 3:
            adb_util.event_input(bean.text)
        self.wait(bean.time)

    def wait(self, ms):
        time_count = ms / 1000
        while time_count > 0 and self.isRun:
            time.sleep(0.01)
            time_count -= 0.01

    def is_focus_pkg(self, pkg):
        if pkg == adb_util.get_focus_app_pkg() or self.isRun is False:
            return True
        else:
            return self.is_focus_pkg(pkg)

    def fix_button_state(self, enable):
        for btn in self.buttons:
            btn.setEnabled(enable)

    def get_edit_value(self, edit, default=0):
        value_str = edit.text().replace(" ", "")
        if value_str is not "":
            try:
                return int(value_str)
            except Exception as e:
                traceback.format_exc()
        return default
