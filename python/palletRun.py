import sys
import time
from datetime import timedelta

from PySide2.QtCore import QTimer, QThread
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QSystemTrayIcon, QMessageBox, QApplication
from login import verify_wifi, link_wifi

import path

# 托盘运行程序，监测校园网连接状态
from PySide2 import QtWidgets, QtGui, QtCore


# 创建一个线程类
class Worker(QThread):
    def __init__(self, func):
        super().__init__()
        self.func = func

    def run(self):
        self.func()


# 在桌面右下角显示通知
def show_message(title, text):
    icon = QIcon()
    icon.addFile(u":/image/image/k1.ico")
    tray = QSystemTrayIcon(icon)  # 使用你的图标文件
    tray.show()
    tray.showMessage(title, text, QSystemTrayIcon.Information)


class TrayIcon(QtWidgets.QWidget):
    def __init__(self, main_window) -> None:
        super().__init__()
        self.time1 = time.time()
        self.main_window = main_window  # 保存之前的主界面
        self.icon = None  # 创建一个 QIcon
        self.trayIcon = None  # 创建系统托盘图标
        self.trayMenu = None  # 创建托盘菜单
        self.open_main = None  # 打开主界面
        self.show_info = None  # 显示相关信息
        self.trayExit = None  # 退出托盘菜单项
        self.link_now = None  # 立即登入校园网
        self.timer = QTimer()  # 创建一个 QTimer
        self.worker = None  # 创建一个 QObject
        self.setup_tray()
        self.installEventFilter(self)
        self.begin_link_wifi()

    # 开始监测校园网状态
    def start_worker(self):
        if not self.worker.isRunning():
            self.worker.start()

    # 开始监测校园网状态
    def begin_link_wifi(self):
        # 监测校园网连接状态
        def is_link_wifi():
            try:
                k = verify_wifi()
                path.monitor_num += 1
                if k == 3:
                    link_wifi()
                    path.run_mun += 1
                    if verify_wifi() == 3:
                        for i in range(3):
                            time.sleep(10)
                            link_wifi()
                            if verify_wifi() == 4:
                                break
            except Exception:
                pass

        self.timer.timeout.connect(self.start_worker)  # 连接定时器的timeout信号到更新函数
        self.worker = Worker(is_link_wifi)
        self.timer.start(int(path.wait_time * 60) * 1000)  # 1000毫秒（1秒）

    def setup_tray(self):
        # 创建系统托盘图标
        self.trayIcon = QtWidgets.QSystemTrayIcon()
        icon = QtGui.QIcon()
        icon.addFile(u":/image/image/k1.ico")
        self.icon = icon
        self.trayIcon.setIcon(self.icon)
        self.trayIcon.show()
        self.trayIcon.setToolTip("监测校园网中……")  # 悬浮文本

        # 创建托盘菜单
        self.trayMenu = QtWidgets.QMenu()

        # 立即运行自动登入校园网功能
        self.link_now = QtWidgets.QAction()
        self.link_now.triggered.connect(self.main_window.link_wifi_dialog)  # 连接到对应的函数
        self.link_now.setToolTip("立即运行自动登入校园网功能")  # 悬浮文本
        self.trayMenu.addAction(self.link_now)

        # 显示主界面
        self.open_main = QtWidgets.QAction()
        self.open_main.triggered.connect(self.open_main_f)  # 连接到对应的函数
        self.open_main.setToolTip("退出托盘运行，返回主界面")  # 悬浮文本
        self.trayMenu.addAction(self.open_main)

        # 显示相关信息
        self.show_info = QtWidgets.QAction()
        self.show_info.triggered.connect(self.show_info_f)  # 连接到对应的函数
        self.show_info.setToolTip("显示一些监测信息")  # 悬浮文本
        self.trayMenu.addAction(self.show_info)

        # 创建退出托盘菜单项并添加到菜单
        self.trayExit = QtWidgets.QAction()
        self.trayExit.triggered.connect(lambda: sys.exit())
        self.trayExit.setToolTip("顾名思义，退出程序")  # 悬浮文本
        self.trayMenu.addAction(self.trayExit)  # 添加退出菜单项

        self.trayIcon.setContextMenu(self.trayMenu)  # 设置托盘菜单
        self.menu_text()  # 设置托盘菜单项文本

    def menu_text(self):
        # 设置托盘菜单项文本
        self.link_now.setText(
            QtCore.QCoreApplication.translate("Notes", "立刻登入", None)
        )
        self.open_main.setText(
            QtCore.QCoreApplication.translate("Notes", "打开主界面", None)
        )
        self.show_info.setText(
            QtCore.QCoreApplication.translate("Notes", "显示信息", None)
        )
        self.trayExit.setText(QtCore.QCoreApplication.translate("Notes", "退出", None))

    def open_main_f(self):  # 打开主界面
        # 还原设置
        QApplication.instance().setQuitOnLastWindowClosed(True)
        self.timer.stop()
        self.timer.deleteLater()
        self.main_window.show()
        self.trayIcon = None
        self.close()

    def show_info_f(self):  # 显示信息
        time2 = time.time()
        seconds = time2 - self.time1
        # 将运行时间转换为时、分、秒
        time_delta = timedelta(seconds=seconds)
        hours = time_delta.seconds // 3600
        minutes = (time_delta.seconds // 60) % 60
        seconds = time_delta.seconds % 60
        time_log = f"{hours}小时 {minutes}分钟 {seconds}秒"
        # 运行时间
        run_time = f"已运行:{time_log}"
        wait_log = f"{'%.2f' % path.wait_time}分钟（折合{int(path.wait_time * 60)}秒）检测一次校园网是否断开"
        mum = f"已经监测校园网：{path.monitor_num}次\n重新连接校园网：{path.run_mun}次"

        text = f"{run_time}\n{wait_log}\n{mum}"
        QMessageBox.information(self.main_window, '监测信息',
                                text,
                                QMessageBox.Ok)
