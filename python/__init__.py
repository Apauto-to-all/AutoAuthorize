import configparser
import os
import sys
import path

from PySide2 import QtCore
from PySide2.QtWidgets import QApplication

from login import create_files
from path import path_settings
from update import update_now_stats_days
from Login_ECJTU_WiFi import MainWindow

create_files()  # 如果第一次运行程序，则创建文件
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # 支持高分辨率屏幕

app = QApplication(sys.argv)
widget = MainWindow()
if os.path.exists(path_settings):  # 如果设置文件存在
    update_now_stats_days()
    setting = configparser.ConfigParser()
    setting.read(path_settings)
    if setting['login']['verify_account'] == '1':
        widget.link_wifi_dialog()
path.main_have_open = 1  # 已经打开主界面
widget.show()
sys.exit(app.exec_())
