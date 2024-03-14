import configparser
import datetime
import json
import os
import path

import requests
from PySide2.QtWidgets import QMessageBox

from login import get_today, get_nc
from path import path_announcement, path_stats, announcement_url, version_url, path_settings


# 更新公告
def update_announcement():
    try:
        request = requests.get(announcement_url, timeout=5)
        with open(path_announcement, "wb") as f:
            f.write(request.content)  # 将公告内容写入文件
        # 更新公告时间
        with open(path_stats) as f:
            stats_f = json.load(f)
        stats_f["announcement_day"] = get_today()
        with open(path_stats, 'w') as f:
            json.dump(stats_f, f)
    except Exception:
        update_announcement_fail()


# 更新公告失败
def update_announcement_fail():
    if not os.path.exists(path_announcement):
        with open(path_announcement, 'w', encoding="utf-8") as f:
            text = '\n\n' + get_today() + ":更新公告失败，请检查网络，检测无误后，请再次点击以下“立即更新公告”按钮重新更新公告"
            f.write(text)
    else:
        with open(path_announcement, 'a', encoding="utf-8") as f:
            text = '\n\n' + get_today() + ":更新公告失败，请检查网络，检测无误后，请再次点击以下“立即更新公告”按钮重新更新公告"
            f.write(text)


# 更新统计天数
def update_now_stats_days():
    today_obj = datetime.datetime.strptime(get_today(), '%Y-%m-%d %H:%M:%S')
    with open(path_stats) as f:
        stats_f = json.load(f)
    begin_day = stats_f['begin_day']
    begin_day_obj = datetime.datetime.strptime(begin_day, '%Y-%m-%d %H:%M:%S')
    days = (today_obj - begin_day_obj).days
    stats_f["now_day"] = get_today()
    stats_f['stats_days'] = days
    with open(path_stats, 'w') as f:
        json.dump(stats_f, f)


# 检查版本
def update_app_version():
    try:
        response = requests.get(version_url, timeout=5)
        if response.status_code == 200:
            v = response.text
            return v
        else:
            return "检查失败，请注意检查网络连接，或点击“打开源地址”检查更新版本"
    except requests.exceptions.ConnectTimeout:
        return "超时，请注意检查网络连接，或重新检测，或点击“打开源地址”检查更新版本"
    except Exception:
        return "出现未知问题，请注意检查网络连接，或点击“打开源地址”检查更新版本"


# 初始显示账户界面信息
def update_settings_ini(self):
    if os.path.exists(path_settings):
        set_ini = configparser.ConfigParser()
        set_ini.read(path_settings)

        self.ui.wait_time.setValue(float(set_ini['settings']['wait_time']))
        path.wait_time = float(set_ini['settings']['wait_time'])

        if set_ini["login"]["save_account"] == "0":
            self.ui.dr_button.setEnabled(True)
            self.ui.dr_yz_pushButton.setText('验证账户')
            self.ui.change_account_pushButton.setEnabled(False)
            self.ui.dr_yz_pushButton.setEnabled(False)
        else:
            self.set_edit_readonly()
            if set_ini['login']['verify_account'] == '0':
                self.ui.dr_yz_pushButton.setText('验证账户')
                self.ui.dr_yz_pushButton.setEnabled(True)
                if not path.have_save_account:
                    QMessageBox.warning(self, "提示", "账户未验证，请验证账户", QMessageBox.Ok)
            else:
                self.ui.lineEdit_nc.setText(get_nc())
                self.ui.dr_yz_pushButton.setText('已验证')
                self.ui.dr_yz_pushButton.setEnabled(False)
            self.ui.dr_button.setEnabled(False)
            self.ui.change_account_pushButton.setEnabled(True)
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
