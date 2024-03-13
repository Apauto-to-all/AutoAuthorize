import sys
import time

from PySide2.QtCore import QTimer, QThread
import path

from login import verify_wifi, link_wifi

# 托盘运行程序，监测校园网连接状态
from PySide2 import QtWidgets, QtGui, QtCore


class Worker(QThread):
    def __init__(self, func):
        super().__init__()
        self.func = func

    def run(self):
        self.func()


class TrayIcon(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.icon = None
        self.trayIcon = None
        self.trayMenu = None
        self.open_main = None  # 打开主界面
        self.show_info = None  # 显示相关信息
        self.timer = QTimer()  # 创建一个 QTimer
        self.worker = None  # 创建一个 QObject
        self.setup_tray()
        self.installEventFilter(self)
        self.begin_link_wifi()

    def start_worker(self):
        if not self.worker.isRunning():
            self.worker.start()

    # 开始监测校园网状态
    def begin_link_wifi(self):
        def is_link_wifi():
            try:
                k = verify_wifi()
                if k == 3:
                    link_wifi()
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
        self.timer.start(1000)  # 1000毫秒（1秒）

    def setup_tray(self):
        # 创建系统托盘图标
        self.trayIcon = QtWidgets.QSystemTrayIcon()
        self.icon = QtGui.QIcon("../k1.ico")
        self.trayIcon.setIcon(self.icon)
        self.trayIcon.show()
        self.trayIcon.setToolTip("监测校园网中……")  # 悬浮文本

        # 创建托盘菜单
        self.trayMenu = QtWidgets.QMenu()

        # 显示主界面
        self.open_main = QtWidgets.QAction()
        self.open_main.triggered.connect(self.open_main_f)  # 连接到对应的函数
        self.trayMenu.addAction(self.open_main)

        # 显示相关信息
        self.show_info = QtWidgets.QAction()
        self.show_info.triggered.connect(self.show_info_f)  # 连接到对应的函数
        self.trayMenu.addAction(self.show_info)

        # 创建退出托盘菜单项并添加到菜单
        self.trayExit = QtWidgets.QAction()
        self.trayExit.triggered.connect(lambda: sys.exit())
        self.trayMenu.addAction(self.trayExit)  # 添加退出菜单项

        self.trayIcon.setContextMenu(self.trayMenu)  # 设置托盘菜单
        self.menu_text()  # 设置托盘菜单项文本

    def menu_text(self):
        # 设置托盘菜单项文本
        self.open_main.setText(
            QtCore.QCoreApplication.translate("Notes", "打开主界面", None)
        )
        self.show_info.setText(
            QtCore.QCoreApplication.translate("Notes", "显示信息", None)
        )
        self.trayExit.setText(QtCore.QCoreApplication.translate("Notes", "退出", None))

    def open_main_f(self):  # 打开主界面
        pass

    def show_info_f(self):  # 显示信息
        pass

# 监测校园网连接状态
