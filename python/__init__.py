import configparser
import os
import sys

from PySide2 import QtCore
from PySide2.QtWidgets import QApplication

from Login_ECJTU_WiFi import MainWindow
from login import verify_wifi, save_post_data_header, save_account, create_files, change_settings, link_wifi, get_nc, \
    link_github, link_dr
from path import path_announcement, path_account, path_settings, path_stats, path_base, version, lzy_url, lzy_password
from settings_functions import desktop, del_desktop, check_version, del_startup, create_regedit, del_regedit
from ui import Ui_MainWindow
from update import update_now_stats_days, update_announcement, get_today, update_app_version

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
widget.show()
sys.exit(app.exec_())
