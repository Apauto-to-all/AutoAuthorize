import configparser
import json
import os
import sys

from PySide2.QtCore import QRegExp, Qt, QTimer
from PySide2.QtGui import QRegExpValidator
from PySide2.QtWidgets import QApplication, QMainWindow, QLineEdit, QDialog, QLabel, QVBoxLayout, QPushButton

from settings_functions import desktop, create_regedit, del_regedit, del_desktop, check_version
from update import update_now_stats_days, update_announcement, update_announcement_days, update_show_ds, get_today, \
    update_app_version
from login import verify_wifi, save_post_data_header, save_account, create_files, change_settings, link_wifi, get_nc, \
    link_github
from path import path_announcement, path_account, path_settings, path_stats, path_base, version, lzy_url, lzy_password
from ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tx = ""
        # 初始显示
        self.show_before_qty()
        self.show_start()
        self.update_settings_ini()  # 更新设置文件
        # 功能
        self.ui.dr_button.clicked.connect(self.save_account)  # 保存账户按钮
        self.ui.username.setValidator(QRegExpValidator(QRegExp("[A-Za-z0-9]+")))  # 限制学号输入
        self.ui.password.setValidator(QRegExpValidator(QRegExp("^((?![\u4E00-\u9FFF]).)*$")))  # 限制密码输入
        self.ui.private_mm.toggled.connect(self.private_click)  # 是否显示密码
        self.ui.dr_yz_pushButton.clicked.connect(self.yz_dr)  # 点击验证按钮
        self.ui.change_account_pushButton.clicked.connect(self.restore_line_edit)  # 可以修改账户
        self.ui.login_button.clicked.connect(self.link_wifi_ui)  # 立即登入校园网
        self.ui.save_settings.clicked.connect(self.save_settings)  # 保存设置
        self.ui.desktop_button.clicked.connect(desktop)  # 创建快捷方式
        self.ui.upadte_announcement_now.clicked.connect(self.update_announcement_now)  # 立即更新公告
        self.ui.stu_box.toggled.connect(self.show_chose_wifi_stu)
        self.ui.free_box.toggled.connect(self.show_chose_wifi_free)
        self.ui.auto_box.toggled.connect(self.show_chose_wifi_auto)
        self.ui.button_del_all.clicked.connect(self.del_data)  # 初始化程序
        self.ui.link_github.clicked.connect(link_github)  # 打开github开源地址
        self.ui.up_v.clicked.connect(self.up_version)  # 检测版本更新

    def update_announcement_now(self):
        # 创建一个对话框窗口
        dialog = QDialog(self)
        dialog.setWindowTitle("更新……")
        # 在对话框中添加按钮和标签
        label = QLabel('公告更新中……\n更新时间较长，请耐心等候', dialog)
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
                self.ui.up_announcement_day.setText(stats_data['announcement_day'])
            with open(path_announcement, 'r', encoding="utf-8") as f:
                announcement = f.read()
            self.ui.textBrowser_gg.setPlainText(announcement)
            self.ui.up_announcement_day.setText(get_today())
            dialog.close()

        QTimer.singleShot(100, up)
        dialog.exec_()
        # 创建一个对话框窗口
        dialog = QDialog(self)
        dialog.setWindowTitle("确认窗口")
        # 在对话框中添加按钮和标签
        label = QLabel("公告更新完成")
        button1 = QPushButton("确定", dialog)
        # 隐藏问号
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button1)
        dialog.setLayout(layout)
        button1.clicked.connect(dialog.close)
        dialog.exec_()

    def restore_line_edit(self):
        self.change_and_update_settings('login', 'save_account', '0')
        self.change_and_update_settings('login', 'verify_account', '0')
        self.ui.nc.setReadOnly(False)
        self.ui.username.setReadOnly(False)
        self.ui.password.setReadOnly(False)
        self.ui.operator_box.setDisabled(False)

    def show_chose_wifi_auto(self):
        if self.ui.auto_box.isChecked():
            self.ui.stu_box.setEnabled(False)
            self.ui.free_box.setEnabled(False)
        else:
            self.ui.stu_box.setEnabled(True)
            self.ui.free_box.setEnabled(True)
        self.update_chose_wifi()

    def show_chose_wifi_stu(self):
        if self.ui.stu_box.isChecked():
            self.ui.auto_box.setEnabled(False)
            self.ui.free_box.setEnabled(False)
        else:
            self.ui.auto_box.setEnabled(True)
            self.ui.free_box.setEnabled(True)
        self.update_chose_wifi()

    def show_chose_wifi_free(self):
        if self.ui.free_box.isChecked():
            self.ui.stu_box.setEnabled(False)
            self.ui.auto_box.setEnabled(False)
        else:
            self.ui.stu_box.setEnabled(True)
            self.ui.auto_box.setEnabled(True)
        self.update_chose_wifi()

    def update_chose_wifi(self):
        if self.ui.stu_box.isChecked():
            change_settings('settings', 'wifi_auto', '0')
            change_settings('settings', 'wifi_free', '0')
            change_settings('settings', 'wifi_stu', '1')
        elif self.ui.free_box.isChecked():
            change_settings('settings', 'wifi_auto', '0')
            change_settings('settings', 'wifi_free', '1')
            change_settings('settings', 'wifi_stu', '0')
        else:
            change_settings('settings', 'wifi_auto', '1')
            change_settings('settings', 'wifi_free', '0')
            change_settings('settings', 'wifi_stu', '0')

    def show_start(self):
        if os.path.exists(path_account):
            with open(path_account) as f:
                account = json.load(f)
            self.ui.dr_textBrowser.setText("")
            nc = list(account.keys())[0]
            self.ui.nc.setText(nc)
            self.ui.username.setText(account[nc][0])
            self.ui.password.setText(account[nc][1])
            self.ui.operator_box.setCurrentText(account[nc][2])
        if os.path.exists(path_stats):
            with open(path_stats) as f:
                stats_data = json.load(f)
            self.ui.days.setText(str(stats_data['stats_days']) + "天")
            self.ui.times.setText(str(stats_data['stats_times']) + "次")
            self.ui.up_announcement_day.setText(stats_data['announcement_day'])
        if os.path.exists(path_announcement):
            with open(path_announcement, 'r', encoding="utf-8") as f:
                announcement = f.read()
            self.ui.textBrowser_gg.setPlainText(announcement)

    def show_before_qty(self):
        if os.path.exists(path_stats):
            with open(path_stats) as f:
                s = json.load(f)
            if s['da_qty'] == 0:
                self.ui.tabWidget.setTabToolTip(5, "敬请期待")
                self.ui.image_ds.hide()
                self.ui.da_tet.hide()

    def set_edit_readonly(self):
        self.ui.nc.setReadOnly(True)
        self.ui.username.setReadOnly(True)
        self.ui.password.setReadOnly(True)
        self.ui.operator_box.setDisabled(True)
        # 设置LineEdit为只读

    def link_wifi_ui(self):
        self.ui.dr_textBrowser.setText("检测网络中……")
        QApplication.processEvents()  # 强制处理待处理的事件，确保界面更新
        check_number_f = verify_wifi()
        if check_number_f == 3:
            self.ui.dr_textBrowser.setText("检测完成，登入校园网中，请稍等……")
            QApplication.processEvents()  # 强制处理待处理的事件，确保界面更新
            link_wifi()
            check_number = verify_wifi()
            if check_number == 1:
                tx = "我们检测到您的网络未连接，请先手动连接校园网，然后再使用本程序。"
            elif check_number == 2:
                tx = "我们检测到您已连接其他网络，请先切换到校园网后再使用本程序。"
            elif check_number == 3:
                tx = "登入失败，请检查学号、密码和运营商是否正确"
            elif check_number == 4:
                tx = "登入成功"
            else:
                tx = "出现未知问题"
            self.ui.dr_textBrowser.setText(tx)
        else:
            if check_number_f == 1:
                tx = "我们检测到您的网络未连接，请先手动连接校园网，然后再使用本程序。"
            elif check_number_f == 2:
                tx = "我们检测到您已连接其他网络，请先切换到校园网后再使用本程序。"
            elif check_number_f == 4:
                tx = "我们检测到您已成功登入校园网，请勿重复登入。"
            else:
                tx = "出现未知问题"
            self.ui.dr_textBrowser.setText(tx)

    def link_wifi_dialog(self):
        # 创建一个对话框窗口
        dialog1 = QDialog(self)
        dialog1.setWindowTitle("自动登入")
        # 在对话框中添加按钮和标签
        label = QLabel('自动检测网络登入校园网中……请稍等', dialog1)
        # 隐藏问号
        dialog1.setWindowFlags(dialog1.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # 隐藏退出按钮
        dialog1.setWindowFlags(dialog1.windowFlags() & ~Qt.WindowCloseButtonHint)
        layout = QVBoxLayout()
        layout.addWidget(label)
        dialog1.setLayout(layout)

        def lin():
            check_number_f = verify_wifi()
            if check_number_f == 3:
                link_wifi()
                check_number = verify_wifi()
                if check_number == 1:
                    self.tx = "我们检测到您的网络未连接，请先手动连接校园网，然后再使用本程序。"
                elif check_number == 2:
                    self.tx = "我们检测到您已连接其他网络，请先切换到校园网后再使用本程序。"
                elif check_number == 3:
                    self.tx = "登入失败，请检查学号、密码和运营商是否正确"
                elif check_number == 4:
                    self.tx = "登入成功"
                else:
                    self.tx = "出现未知问题"
            else:
                if check_number_f == 1:
                    self.tx = "我们检测到您的网络未连接，请先手动连接校园网，然后再使用本程序。"
                elif check_number_f == 2:
                    self.tx = "我们检测到您已连接其他网络，请先切换到校园网后再使用本程序。"
                elif check_number_f == 4:
                    self.tx = "我们检测到您已成功登入校园网，请勿重复登入。"
                else:
                    self.tx = "出现未知问题"
            dialog1.close()

        QTimer.singleShot(50, lin)
        dialog1.exec_()

        # 创建一个对话框窗口
        dialog = QDialog(self)
        dialog.setWindowTitle("自动登入")
        # 在对话框中添加按钮和标签
        label = QLabel(self.tx, dialog)
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
        button1.clicked.connect(dialog.close)
        button2.clicked.connect(sys.exit)
        # 显示对话框
        dialog.exec_()

    def update_settings_ini(self):
        if os.path.exists(path_settings):
            set_ini = configparser.ConfigParser()
            set_ini.read(path_settings)

            if set_ini["login"]["save_account"] == "0":
                self.ui.dr_button.setEnabled(True)
                self.ui.change_account_pushButton.setEnabled(False)
                self.ui.dr_yz_pushButton.setEnabled(False)
            else:
                self.set_edit_readonly()
                if set_ini['login']['verify_account'] == '0':
                    self.ui.dr_textBrowser.setText('账户已保存，请先验证账户，通过验证后即可使用本程序')
                else:
                    self.ui.lineEdit_nc.setText(get_nc())
                self.ui.dr_button.setEnabled(False)
                self.ui.change_account_pushButton.setEnabled(True)
                self.ui.dr_yz_pushButton.setEnabled(True)
            if set_ini['login']['verify_account'] == '0':
                self.ui.login_button.setEnabled(False)
            else:
                self.ui.login_button.setEnabled(True)
            if set_ini['settings']['auto_start'] == '0':
                self.ui.auto_start.setChecked(False)
            else:
                self.ui.auto_start.setChecked(True)
            if set_ini['settings']['wifi_auto'] == '1':
                self.ui.auto_box.setChecked(True)
                self.ui.stu_box.setEnabled(False)
                self.ui.free_box.setEnabled(False)
            if set_ini['settings']['wifi_stu'] == '1':
                self.ui.stu_box.setChecked(True)
                self.ui.auto_box.setEnabled(False)
                self.ui.free_box.setEnabled(False)
            if set_ini['settings']['wifi_free'] == '1':
                self.ui.free_box.setChecked(True)
                self.ui.stu_box.setEnabled(False)
                self.ui.auto_box.setEnabled(False)

    def change_and_update_settings(self, section, option, value):
        change_settings(section, option, value)
        self.update_settings_ini()

    def save_settings(self):
        if self.ui.auto_start.isChecked():
            change_settings('settings', 'auto_start', '1')
            create_regedit()
        else:
            change_settings('settings', 'auto_start', '0')
            del_regedit()

        # 创建一个对话框窗口
        dialog = QDialog(self)
        dialog.setWindowTitle("确认窗口")
        # 在对话框中添加按钮和标签
        label = QLabel("设置已经保存")
        button1 = QPushButton("确定", dialog)
        # 隐藏问号
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button1)
        dialog.setLayout(layout)
        button1.clicked.connect(dialog.close)
        dialog.exec_()

        self.update_settings_ini()

    def save_account(self):
        warning = ""
        nc = self.ui.nc.text()
        username = self.ui.username.text()
        password = self.ui.password.text()
        operator = self.ui.operator_box.currentText()
        if operator == "选择运营商":
            warning = '未选择运营商，请先选择运营商，后再保存'
        if warning != "":
            QApplication.beep()
            self.ui.dr_textBrowser.setText(warning)
        else:
            save_account(nc, username, password, operator)
            save_post_data_header(username, password, operator)
            self.change_and_update_settings('login', 'save_account', '1')
            self.set_edit_readonly()
            warning = "账户保存成功，请点击‘验证账户’，验证账户是否可用，验证通过后即可使用该账户登入校园网"
            self.ui.dr_textBrowser.setText(warning)

    def private_click(self):
        if self.ui.private_mm.isChecked():
            self.ui.password.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.password.setEchoMode(QLineEdit.Password)

    def yz_dr(self):
        # 创建一个对话框窗口
        dialog = QDialog(self)
        dialog.setWindowTitle("验证")
        # 在对话框中添加按钮和标签
        label = QLabel("验证账户需要在未登入情况下连接校园网")
        button1 = QPushButton("已在未登入情况下连接校园网，开始验证", dialog)
        button2 = QPushButton("取消验证", dialog)
        button3 = QPushButton("确保账户信息无误，跳过验证", dialog)

        # 隐藏退出按钮
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowCloseButtonHint)
        # 隐藏问号
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        dialog.setLayout(layout)

        # 将按钮的点击事件连接到对应的槽函数
        def verify_account():
            label.setText('检测中……请稍等')
            QApplication.processEvents()  # 强制处理待处理的事件，确保界面更新
            check_number = verify_wifi()
            if check_number == 1:
                tx = "检测到网络未连接，请先连接校园网（勿登入）"
            elif check_number == 2:
                tx = "检测到已经连接其他网络，请先退出其他网络，再连接校园网（勿登入）"
            elif check_number == 3:
                label.setText('检测成功，验证中……请稍等')
                QApplication.processEvents()  # 强制处理待处理的事件，确保界面更新
                link_wifi()
                if verify_wifi() == 4:
                    self.change_and_update_settings('login', 'verify_account', '1')
                    tx = '验证成功！，你可以在设置里，设置开机自启功能'
                else:
                    tx = '验证失败，请重新检查学号、密码和运营商是否正确'
                self.ui.dr_textBrowser.setText(tx)
                dialog.close()
            elif check_number == 4:
                tx = "检测到你已连接校园网，并处于登入状态，请退出登入，以完成账户验证"
            else:
                tx = "出现未知问题"
            label.setText(tx)

        def skip_verify_account():
            self.change_and_update_settings('login', 'verify_account', '1')
            wra = '已跳过验证，请自行检测是否能登入校园网'
            self.ui.dr_textBrowser.setText(wra)
            dialog.close()

        button1.clicked.connect(verify_account)
        button2.clicked.connect(dialog.close)
        button3.clicked.connect(skip_verify_account)

        # 显示对话框
        dialog.exec_()

    def ds_qty(self):
        # 创建一个对话框窗口
        dialog = QDialog(self)
        dialog.setWindowTitle("窗口")
        # 在对话框中添加按钮和标签
        label = QLabel("非常感谢您使用本程序！")
        label.setAlignment(Qt.AlignCenter)
        button1 = QPushButton("下一步", dialog)
        # 隐藏问号
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # 隐藏退出按钮
        # dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowCloseButtonHint)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button1)
        dialog.setLayout(layout)

        def talk():
            tak = [
                '非常感谢您使用本程序！',
                '我们目前的宣传渠道比较有限，如果您喜欢我们的应用，请分享给您的朋友、同学。感谢您的支持！',
                '如果您有什么意见或建议，可在程序右下角找到我的联系方式',
                '如果你觉得这个程序对你有用，也可以考虑给予支持。这条提醒仅出现一次，无论你的选择如何。\n请按照自己的能力来决定是否打赏，你仍可以继续免费使用。',
            ]
            if label.text() == tak[-1]:
                dialog.close()
            else:
                llk = len(tak)
                for i in range(llk):
                    if label.text() == tak[i] and i != llk - 1:
                        label.setText(tak[i + 1])
                        QApplication.processEvents()  # 强制处理待处理的事件，确保界面更新
                        break
                if label.text() == tak[-1]:
                    button1.setText('我会考虑')
                    layout.addWidget(button2)

        button2 = QPushButton("不予考虑，我要白嫖到底")
        button1.clicked.connect(talk)
        button2.clicked.connect(dialog.close)
        dialog.exec_()

    def del_data(self):
        # 创建一个对话框窗口
        dialog = QDialog(self)
        dialog.setWindowTitle("确认窗口")
        # 在对话框中添加按钮和标签
        label = QLabel(
            '该操作会删除储存在你电脑中的全部数据，并关闭设置中的所有功能，请考虑再三')
        button1 = QPushButton('我确认删除', dialog)
        button2 = QPushButton('取消', dialog)
        # 隐藏问号
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button1)
        layout.addWidget(button2)
        dialog.setLayout(layout)

        def sure():
            if button1.text() == '我确认删除':
                label.setText('请再次确实“删除所有数据”')
                button1.setText('我再次确认删除')
            elif button1.text() == '我再次确认删除':
                for root, dirs, files in os.walk(path_base, topdown=False):
                    for name in files:
                        file_path = os.path.join(root, name)
                        os.remove(file_path)
                    for name in dirs:
                        dir_path = os.path.join(root, name)
                        os.rmdir(dir_path)
                # 最后删除根文件夹
                os.rmdir(path_base)
                del_desktop()
                del_regedit()
                dialog.close()
                sys.exit()

        button1.clicked.connect(sure)
        button2.clicked.connect(dialog.close)
        dialog.exec_()

    def up_version(self):
        dialog1 = QDialog(self)
        dialog1.setWindowTitle("更新……")
        # 在对话框中添加按钮和标签
        label = QLabel('检查最新版本中……时间较长，请稍等', dialog1)
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
                v_t = version + '-->' + self.v + '\n 有最新版本，请点击“打开源地址”以更新程序'
            elif number1 == number2:
                v_t = version + '-->' + self.v + '\n 版本无变化，请关闭窗口'
            else:
                v_t = '???' + version + '-->' + self.v + '???\n出现问题，请点击“打开源地址”以手动检测最新版本'
        else:
            v_t = self.v
        label = QLabel(v_t, dialog)
        label.setAlignment(Qt.AlignCenter)
        button1 = QPushButton("打开github开源项目地址", dialog)
        button2 = QPushButton(f"打开蓝奏云网盘以获取最新安装包，提取码：{lzy_password}（点击复制）", dialog)
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
            command = 'echo ' + lzy_password.strip() + '|clip'
            os.system(command)
            os.system(f'start {lzy_url}')
            dialog.close()

        button1.clicked.connect(open_url)
        button2.clicked.connect(open_lzy)
        button3.clicked.connect(dialog.close)
        # 显示对话框
        dialog.exec_()


def da_gty():
    if os.path.exists(path_stats):
        with open(path_stats) as f:
            s = json.load(f)
        if s['da_qty'] == 0 and update_show_ds() == 1:
            ppa = QApplication(sys.argv)
            do = MainWindow()
            do.link_wifi_ui()
            do.ds_qty()
            do.ui.tabWidget.setCurrentIndex(4)
            do.show()
            sys.exit(ppa.exec_())


if __name__ == "__main__":
    create_files()
    da_gty()
    app = QApplication(sys.argv)
    widget = MainWindow()
    if os.path.exists(path_settings):
        update_now_stats_days()
        setting = configparser.ConfigParser()
        setting.read(path_settings)
        if setting['login']['verify_account'] == '1':
            widget.link_wifi_dialog()
    widget.show()
    update_announcement_days()
    sys.exit(app.exec_())
