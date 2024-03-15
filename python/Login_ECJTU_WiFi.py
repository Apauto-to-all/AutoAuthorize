import configparser
import json
import os
import sys

import path

from PySide2.QtCore import QRegExp, Qt, QTimer
from PySide2.QtGui import QRegExpValidator, QFont
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QLineEdit,
    QDialog,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
)

from login import (
    verify_wifi,
    save_account,
    change_settings,
    link_wifi,
    link_github,
    link_dr,
    open_lzy,
    logout,
)
from path import (
    path_announcement,
    path_account,
    path_stats,
    path_base,
    version,
    lzy_url,
    lzy_password,
)
from settings_functions import (
    desktop,
    check_version,
    create_regedit,
    del_regedit,
    del_desktop,
)
from ui import Ui_MainWindow
from update import update_announcement, update_app_version, update_settings_ini
from palletRun import TrayIcon, show_message


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.trayIcon = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # 初始显示
        self.show_start()
        update_settings_ini(self)  # 设置文件的显示
        # 功能
        self.ui.dr_button.clicked.connect(self.save_account)  # 保存账户按钮

        self.ui.username.setValidator(
            QRegExpValidator(QRegExp("[A-Za-z0-9]+"))
        )  # 限制学号输入

        self.ui.password.setValidator(
            QRegExpValidator(QRegExp("^((?![\u4E00-\u9FFF]).)*$"))
        )  # 限制密码输入

        self.ui.private_mm.toggled.connect(self.private_click)  # 是否显示密码

        self.ui.dr_yz_pushButton.clicked.connect(self.yz_dr)  # 点击验证按钮

        self.ui.change_account_pushButton.clicked.connect(
            self.restore_line_edit
        )  # 可以修改账户

        self.ui.login_button.clicked.connect(self.link_wifi_dialog)  # 立即登入校园网

        self.ui.desktop_button.clicked.connect(self.create_desktop)  # 创建快捷方式

        self.ui.upadte_announcement_now.clicked.connect(
            self.update_announcement_now
        )  # 立即更新公告

        self.ui.stu_box.toggled.connect(self.show_chose_wifi_stu)  # 连接网络选择设置

        self.ui.free_box.toggled.connect(self.show_chose_wifi_free)  # 连接网络选择设置

        self.ui.auto_box.toggled.connect(self.show_chose_wifi_auto)  # 连接网络选择设置

        self.ui.auto_start.toggled.connect(self.update_auto_start)  # 是否自动启动

        self.ui.button_del_all.clicked.connect(
            self.del_data
        )  # 初始化程序，删除所有数据

        self.ui.link_github.clicked.connect(link_github)  # 打开github开源地址

        self.ui.up_v.clicked.connect(self.up_version)  # 检测版本更新

        self.ui.link_dr.clicked.connect(link_dr)  # 打开校园网登入页面

        self.ui.lzy_pushButton.clicked.connect(open_lzy)  # 打开蓝奏云网盘

        self.ui.logout_pushButton.clicked.connect(self.logout_account)  # 注销校园网账户

        self.ui.tuo.clicked.connect(self.pallet_run)  # 托盘运行程序，监测校园网连接状态

        self.ui.wait_time.valueChanged.connect(self.wait_time_change)  # 修改等待时间

        self.ui.wait_time_Button.clicked.connect(
            self.wait_time_explain
        )  # 对等待时间的说明按钮

    # 修改等待时间
    def wait_time_change(self):
        change_settings("settings", "wait_time", str(self.ui.wait_time.value()))
        set_ini = configparser.ConfigParser()
        set_ini.read(path.path_settings)
        path.wait_time = float(set_ini["settings"]["wait_time"])

    # 对等待时间的说明
    def wait_time_explain(self):
        QMessageBox.information(
            self,
            "说明",
            f"在托盘运行时，间隔一定时间检测校园网是否断开，用于修改间隔时间\n单位为：分钟\n目前设置：{path.wait_time}分钟检测一次校园网是否断开",
            QMessageBox.Ok,
        )

    # 托盘运行
    def pallet_run(self):
        setting = configparser.ConfigParser()
        setting.read(path.path_settings)
        if setting["login"]["verify_account"] == "1":
            # 获取当前的 QApplication 实例
            app = QApplication.instance()
            # 将 quitOnLastWindowClosed 属性设置为 False。即使所有的窗口都被关闭，应用程序也不会退出。
            app.setQuitOnLastWindowClosed(False)

            show_message(
                "提示",
                "程序已经在托盘处运行，持续为你监测校园网……\n右键点击图标可以进行相关操作",
            )
            # 已经验证账户，可以使用此功能
            self.hide()
            # 创建托盘运行程序
            path.monitor_num = path.run_mun = 0
            self.trayIcon = TrayIcon(self)
        else:
            if setting["login"]["save_account"] == "1":
                QMessageBox.warning(
                    self, "警告", "未验证账户，无法使用此功能", QMessageBox.Ok
                )
            else:
                QMessageBox.warning(
                    self, "警告", "账户不存在，无法使用此功能", QMessageBox.Ok
                )

    # 更新公告
    def update_announcement_now(self):  # 立即更新公告
        # 创建一个对话框窗口
        dialog = QDialog(self)
        dialog.setWindowTitle("更新……")
        # 在对话框中添加按钮和标签
        label = QLabel("公告更新中……\n更新时间较长，请耐心等候", dialog)
        label.setAlignment(Qt.AlignCenter)
        # 隐藏问号
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()
        layout.addWidget(label)
        dialog.setLayout(layout)

        def up():
            update_announcement()
            if os.path.exists(path_stats):
                with open(path_stats) as f:
                    stats_data = json.load(f)
                self.ui.up_announcement_day.setText(stats_data["announcement_day"])
            with open(path_announcement, "r", encoding="utf-8") as f:
                announcement = f.read()
            self.ui.textBrowser_gg.setPlainText(announcement)
            dialog.close()

        QTimer.singleShot(100, up)
        dialog.exec_()
        # 创建一个对话框窗口
        dialog = QDialog(self)
        dialog.setWindowTitle("确认窗口")
        # 在对话框中添加按钮和标签
        label = QLabel("公告更新完成")
        label.setAlignment(Qt.AlignCenter)
        button1 = QPushButton("确定", dialog)
        # 隐藏问号
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button1)
        dialog.setLayout(layout)
        button1.clicked.connect(dialog.close)
        dialog.exec_()

    # 修改账户，数据初始化
    def restore_line_edit(self):
        self.change_and_update_settings("login", "save_account", "0")
        self.change_and_update_settings("login", "verify_account", "0")
        self.ui.nc.setReadOnly(False)
        self.ui.username.setReadOnly(False)
        self.ui.password.setReadOnly(False)
        self.ui.operator_box.setDisabled(False)

    # 注销校园网账户
    def logout_account(self):
        try:
            logout()
            QMessageBox.information(self, "提示", "注销成功", QMessageBox.Ok)
        except Exception:
            QMessageBox.warning(self, "提示", "无需注销", QMessageBox.Ok)

    # 选择“自动选择”
    def show_chose_wifi_auto(self):
        if self.ui.auto_box.isChecked():
            self.ui.stu_box.setEnabled(False)
            self.ui.free_box.setEnabled(False)
        else:
            self.ui.stu_box.setEnabled(True)
            self.ui.free_box.setEnabled(True)
        self.update_chose_wifi()

    # 选择Stu
    def show_chose_wifi_stu(self):
        if self.ui.stu_box.isChecked():
            self.ui.auto_box.setEnabled(False)
            self.ui.free_box.setEnabled(False)
        else:
            self.ui.auto_box.setEnabled(True)
            self.ui.free_box.setEnabled(True)
        self.update_chose_wifi()

    # 选择Free
    def show_chose_wifi_free(self):
        if self.ui.free_box.isChecked():
            self.ui.stu_box.setEnabled(False)
            self.ui.auto_box.setEnabled(False)
        else:
            self.ui.stu_box.setEnabled(True)
            self.ui.auto_box.setEnabled(True)
        self.update_chose_wifi()

    # 更新选择的Stu或Free
    def update_chose_wifi(self):
        if self.ui.stu_box.isChecked():
            change_settings("settings", "wifi_auto", "0")
            change_settings("settings", "wifi_free", "0")
            change_settings("settings", "wifi_stu", "1")
        elif self.ui.free_box.isChecked():
            change_settings("settings", "wifi_auto", "0")
            change_settings("settings", "wifi_free", "1")
            change_settings("settings", "wifi_stu", "0")
        else:
            change_settings("settings", "wifi_auto", "1")
            change_settings("settings", "wifi_free", "0")
            change_settings("settings", "wifi_stu", "0")

    # 刚进入页面显示的数据
    def show_start(self):
        if os.path.exists(path_account):
            with open(path_account) as f:
                account = json.load(f)
            nc = list(account.keys())[0]
            self.ui.nc.setText(nc)
            self.ui.username.setText(account[nc][0])
            self.ui.password.setText(account[nc][1])
            self.ui.operator_box.setCurrentText(account[nc][2])
        if os.path.exists(path_stats):
            with open(path_stats) as f:
                stats_data = json.load(f)
            self.ui.days.setText(str(stats_data["stats_days"]) + "天")
            self.ui.times.setText(str(stats_data["stats_times"]) + "次")
            self.ui.up_announcement_day.setText(stats_data["announcement_day"])
        if os.path.exists(path_announcement):
            with open(path_announcement, "r", encoding="utf-8") as f:
                announcement = f.read()
            self.ui.textBrowser_gg.setPlainText(announcement)

    # 设置账户，密码为只读
    def set_edit_readonly(self):
        self.ui.nc.setReadOnly(True)
        self.ui.username.setReadOnly(True)
        self.ui.password.setReadOnly(True)
        self.ui.operator_box.setDisabled(True)

    # 修改设置文件
    def change_and_update_settings(self, section, option, value):
        change_settings(section, option, value)
        update_settings_ini(self)

    # 更新是否点击自动启动
    def update_auto_start(self):
        if self.ui.auto_start.isChecked():
            change_settings("settings", "auto_start", "1")
            create_regedit()
        else:
            change_settings("settings", "auto_start", "0")
            del_regedit()

    # 保存账户，按钮用
    def save_account(self):
        warning = ""
        nc = self.ui.nc.text()
        username = self.ui.username.text()
        password = self.ui.password.text()
        operator = self.ui.operator_box.currentText()
        if operator == "选择运营商":
            warning = "未选择运营商，请先选择运营商，后再保存"
        if warning != "":
            QMessageBox.warning(self, "警告", warning, QMessageBox.Ok)
        else:
            save_account(nc, username, password, operator)  # 保存账户
            path.have_save_account = 1  # 显示已经保存账户
            self.change_and_update_settings(
                "login", "save_account", "1"
            )  # 修改设置文件，已经保存账户
            self.set_edit_readonly()  # 设置账户，密码为只读
            QMessageBox.information(
                self,
                "接下来",
                "账户保存成功，请点击‘验证账户’，验证账户是否可用，通过后解锁自动登入校园网功能",
                QMessageBox.Ok,
            )

    # 是否显示密码
    def private_click(self):
        if self.ui.private_mm.isChecked():
            self.ui.password.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.password.setEchoMode(QLineEdit.Password)

    # 验证账户
    def yz_dr(self):
        # 创建一个对话框窗口
        dialog = QDialog(self)
        dialog.setWindowTitle("验证")
        # 在对话框中添加按钮和标签
        label = QLabel("请开始验证账户，诺账户验证成功，即可使用该账户登入校园网")
        label.setAlignment(Qt.AlignCenter)
        button1 = QPushButton("开始验证", dialog)
        button2 = QPushButton("取消验证", dialog)

        # 隐藏退出按钮
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowCloseButtonHint)
        # 隐藏问号
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button1)
        layout.addWidget(button2)
        dialog.setLayout(layout)

        # 将按钮的点击事件连接到对应的槽函数
        def verify_account():
            label.setText("检测中……请稍等")
            QApplication.processEvents()  # 强制处理待处理的事件，确保界面更新
            check_number = verify_wifi()
            if check_number == 3:
                label.setText("检测成功，验证中……请稍等")
                QApplication.processEvents()  # 强制处理待处理的事件，确保界面更新
                link_wifi()
                if verify_wifi() == 4:
                    self.change_and_update_settings("login", "verify_account", "1")
                    QMessageBox.information(self, "成功", "验证成功！欢迎你使用本程序")
                else:
                    QMessageBox.warning(
                        self,
                        "警告",
                        "验证失败，请重新检查学号、密码、运营商是否正确\nECJTU_Stu和EcjtuLib_Free网络的选择是否正确",
                        QMessageBox.Ok,
                    )
                dialog.close()
            elif check_number == 4:
                label.setText("检测到你已连接校园网，处于登入状态，正在登出校园网")
                QApplication.processEvents()  # 强制处理待处理的事件，确保界面更新
                from login import logout

                logout()
                label.setText("已注销校园网，正在重新验证账户")
                QApplication.processEvents()  # 强制处理待处理的事件，确保界面更新
                verify_account()
            else:
                if check_number == 1:
                    tx = "我们检测到您的网络未连接，请先手动连接校园网，然后再使用本程序。"
                elif check_number == 2:
                    tx = "我们检测到您已连接其他网络，请先切换到校园网后再使用本程序。"
                else:
                    tx = "出现未知问题"
                QMessageBox.warning(self, "警告", tx, QMessageBox.Ok)
                label.setText("检测失败，请重新点击“开始验证”")
                QApplication.processEvents()  # 强制处理待处理的事件，确保界面更新
            label.setText("检测失败，请重新点击“开始验证”")
            QApplication.processEvents()  # 强制处理待处理的事件，确保界面更新

        button1.clicked.connect(verify_account)
        button2.clicked.connect(dialog.close)

        # 显示对话框
        dialog.exec_()

    # 初始化程序，按钮用
    def del_data(self):
        # 创建一个对话框窗口
        dialog = QDialog(self)
        dialog.setWindowTitle("确认窗口")
        # 在对话框中添加按钮和标签
        label = QLabel(
            "该操作会删除储存在你电脑中的全部数据，并关闭设置中的所有功能，请考虑再三"
        )
        label.setAlignment(Qt.AlignCenter)
        button1 = QPushButton("我确认删除", dialog)
        button2 = QPushButton("取消", dialog)
        # 隐藏问号
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button1)
        layout.addWidget(button2)
        dialog.setLayout(layout)

        def sure():
            if button1.text() == "我确认删除":
                label.setText("请再次确实“删除所有数据”")
                button1.setText("我再次确认删除")
            elif button1.text() == "我再次确认删除":
                for root, dirs, files in os.walk(path_base, topdown=False):
                    for name in files:
                        file_path = os.path.join(root, name)
                        os.remove(file_path)
                    for name in dirs:
                        dir_path = os.path.join(root, name)
                        os.rmdir(dir_path)
                # 最后删除根文件夹
                os.rmdir(path_base)
                del_regedit()
                del_desktop()
                dialog.close()
                sys.exit()

        button1.clicked.connect(sure)
        button2.clicked.connect(dialog.close)
        dialog.exec_()

    # 检测版本更新，按钮用
    def up_version(self):  # 检测版本更新
        dialog1 = QDialog(self)
        dialog1.setWindowTitle("更新……")
        # 在对话框中添加按钮和标签
        label = QLabel("检查最新版本中……时间较长，请稍等", dialog1)
        label.setAlignment(Qt.AlignCenter)
        # 隐藏问号
        dialog1.setWindowFlags(dialog1.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # 隐藏退出按钮
        dialog1.setWindowFlags(dialog1.windowFlags() & ~Qt.WindowCloseButtonHint)
        layout = QVBoxLayout()
        layout.addWidget(label)
        dialog1.setLayout(layout)

        def ch():
            self.v = update_app_version()
            dialog1.close()

        QTimer.singleShot(100, ch)
        dialog1.exec_()

        dialog = QDialog(self)
        dialog.setWindowTitle("更新……")
        if check_version(self.v):
            number1 = int(version.replace("v", "").replace(".", ""))
            number2 = int(self.v.replace("v", "").replace(".", ""))
            if number1 < number2:
                v_t = (
                    version
                    + "-->"
                    + self.v
                    + "\n 有最新版本，请点击“打开源地址”以更新程序"
                )
            elif number1 == number2:
                v_t = version + "-->" + self.v + "\n 版本无变化，请关闭窗口"
            else:
                v_t = (
                    "???"
                    + version
                    + "-->"
                    + self.v
                    + "???\n出现问题，请点击“打开源地址”以手动检测最新版本"
                )
        else:
            v_t = self.v
        label = QLabel(v_t, dialog)
        label.setAlignment(Qt.AlignCenter)
        button1 = QPushButton("打开github开源项目地址", dialog)
        button2 = QPushButton(
            f"打开蓝奏云网盘以获取最新安装包，提取码：{lzy_password}\n（点击该按钮，程序会自动帮你复制提取码，在蓝奏云网盘界面可直接粘贴）",
            dialog,
        )
        button3 = QPushButton("关闭窗口", dialog)
        # 隐藏问号
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        dialog.setLayout(layout)

        def open_url():
            link_github()
            dialog.close()

        def open_lzy():
            command = "echo " + lzy_password.strip() + "|clip"
            os.system(command)
            os.system(f"start {lzy_url}")
            dialog.close()

        button1.clicked.connect(open_url)
        button2.clicked.connect(open_lzy)
        button3.clicked.connect(dialog.close)
        # 显示对话框
        dialog.exec_()

    def create_desktop(self):  # 创建桌面快捷方式
        desktop()
        QMessageBox.information(self, "提示", "桌面快捷方式创建成功", QMessageBox.Ok)

    # 用于登入校园网
    def link_wifi_dialog(self):
        # 创建一个对话框窗口
        dialog1 = QDialog(self)
        dialog1.setWindowTitle("自动登入")
        # 在对话框中添加按钮和标签
        label = QLabel("自动检测网络登入校园网中……请稍等", dialog1)
        label.setAlignment(Qt.AlignCenter)
        # 隐藏问号
        dialog1.setWindowFlags(dialog1.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()
        layout.addWidget(label)
        dialog1.setLayout(layout)
        check_number_f = 0
        tx = ""

        def lin():
            nonlocal check_number_f
            nonlocal tx
            try:
                check_number_f = verify_wifi()
                if check_number_f == 3:
                    link_wifi()
                    check_number_f = verify_wifi()
                    if check_number_f == 3:
                        tx = "登入失败，请检查学号、密码和运营商是否正确"
                    elif check_number_f == 4:
                        tx = "登入成功"
                    else:
                        tx = "出现未知问题"
                else:
                    if check_number_f == 1:
                        tx = "我们检测到您的网络未连接，请先手动连接校园网，然后再使用本程序。"
                    elif check_number_f == 2:
                        tx = "我们检测到您已连接其他网络，请先切换到校园网后再使用本程序。"
                    elif check_number_f == 4:
                        tx = "我们检测到您已成功登入校园网，请勿重复登入。"
                    else:
                        tx = "出现未知问题"
            except Exception:
                tx = "出现未知问题，请重新运行程序"
            dialog1.close()

        QTimer.singleShot(100, lin)
        dialog1.exec_()

        # 创建一个对话框窗口
        dialog = QDialog(self)
        dialog.setWindowTitle("自动登入")
        dialog.setWindowFlags(
            dialog.windowFlags() | Qt.WindowStaysOnTopHint
        )  # 设置为在最前端显示
        # 在对话框中添加按钮和标签
        label = QLabel(tx, dialog)
        label.setAlignment(Qt.AlignCenter)
        button1 = QPushButton("打开主界面", dialog)
        button2 = QPushButton("关闭窗口", dialog)

        # 隐藏问号
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # 隐藏退出按钮
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowCloseButtonHint)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button1)
        layout.addWidget(button2)
        dialog.setLayout(layout)

        def open_main():  # 打开主界面
            timer.stop()
            dialog.close()

        def close_dialog():  # 关闭窗口
            if path.main_have_open:
                timer.stop()
                dialog.close()
            else:
                sys.exit()

        button1.clicked.connect(open_main)
        button2.clicked.connect(close_dialog)

        # 创建一个 QTimer
        timer = QTimer(dialog)
        djs = 5  # 倒计时
        djs_text = f"自动退出倒计时：{djs}!"
        label1 = QLabel(djs_text, dialog)
        label1.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(16)  # 设置字体大小为 16
        label1.setFont(font)  # 设置标签的字体
        layout.addWidget(label1)

        pd = 0

        def update_label():
            nonlocal djs  # 使用外部变量
            nonlocal pd
            nonlocal check_number_f
            if pd == 0:
                if check_number_f == 3 or check_number_f == 1:
                    djs = 999
            pd = 1
            djs -= 1
            label1.setText(f"自动退出倒计时：{djs}!")
            dialog.update()  # 更新界面
            if djs == 0:
                close_dialog()

        timer.timeout.connect(update_label)  # 连接定时器的timeout信号到更新函数
        timer.start(1000)  # 每1000毫秒（1秒）触发一次定时器

        # 显示对话框
        dialog.exec_()
