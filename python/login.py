import configparser
import datetime
import json
import os
import re
import subprocess

import requests

from path import (
    path_header,
    path_settings,
    path_account,
    path_private,
    path_stats,
    github_url,
    dr_url,
    lzy_password,
    lzy_url,
    baidu_url,
)


def open_lzy():  # 打开蓝奏云网盘
    command = "echo " + lzy_password.strip() + "|clip"
    os.system(command)
    os.system(f"start {lzy_url}")


def link_github():  # 打开github地址
    os.system(f"start {github_url}")


def link_dr():  # 打开校园网验证地址
    os.system(f"start {dr_url}")


def get_nc():  # 获取账号key（昵称）
    with open(path_account) as f:
        account = json.load(f)
    return list(account.keys())[0]


def get_post_url():  # 获取post地址
    html = requests.get(dr_url).text
    ip4_y = re.search("v4ip='(.*?)';", html, re.S)
    ip4_n = re.search("v46ip='(.*?)' ", html, re.S)
    if ip4_y is None:
        ip4 = ip4_n.group(1)
    else:
        ip4 = ip4_y.group(1)
    return (
        f"http://172.16.2.100:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=172.16.2.100&iTermType=1"
        f"&wlanuserip={ip4}&wlanacip=null&wlanacname=null&mac=00-00-00-00-00-00&ip={ip4}&enAdvert=0"
        f"&queryACIP=0&loginMethod=1"
    )


def get_post_data():  # 获取post数据
    nc = get_nc()
    with open(path_account, "r") as f_account:
        account = json.load(f_account)
    username = account[nc][0]
    password = account[nc][1]
    operator = account[nc][2]
    post_data = {
        "DDDDD": f",0,{username}{get_operator_last(operator)}",
        "upass": f"{password}",
        "R1": "0",
        "R2": "0",
        "R3": "0",
        "R6": "0",
        "para": "00",
        "0MKKey": "123456",
        "buttonClicked": "",
        "redirect_url": "",
        "err_flag": "",
        "username": "",
        "password": "",
        "user": "",
        "cmd": "",
        "Login": "",
    }
    return post_data


def get_post_data_free():  # 获取post数据，用于图书馆免费网络登入
    nc = get_nc()
    with open(path_account, "r") as f_account:
        account = json.load(f_account)
    username = account[nc][0]
    password = account[nc][1]
    post_data_free = {
        "DDDDD": f",0,{username}",
        "upass": f"{password}",
        "R1": "0",
        "R2": "0",
        "R3": "0",
        "R6": "0",
        "para": "00",
        "0MKKey": "123456",
        "buttonClicked": "",
        "redirect_url": "",
        "err_flag": "",
        "username": "",
        "password": "",
        "user": "",
        "cmd": "",
        "Login": "",
    }  # 用于图书馆免费网络登入
    print()
    return post_data_free


def get_post_header():  # 获取header
    with open(path_header) as f:
        post_header = json.load(f)
    return post_header


def get_operator_last(operator):
    if operator == "中国移动":
        kk = "@cmcc"
    elif operator == "中国电信":
        kk = "@telecom"
    elif operator == "中国联通":
        kk = "@unicom"
    else:
        kk = "没有选择运营商"
    return kk


# 保存post数据的header
def save_post_data_header():
    post_header = {  # 拿来的
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 "
        "Safari/537.36"
    }
    with open(path_header, "w") as f_h:
        json.dump(post_header, f_h)


def save_account(nc, username, password, operator):  # 保存账号密码
    if nc == "":
        nc = username
    with open(path_account, "w") as f_account:
        json.dump({nc: [username, password, operator]}, f_account)
    save_post_data_header()


# 检测当前连接的wifi名称
def get_connected_wifi_name():
    result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"]).decode(
        "gbk"
    )  # 执行命令并获取输出
    lines = result.split("\n")  # 将输出分割成行
    for line in lines:  # 遍历每一行
        if (
            "SSID" in line and "BSSID" not in line
        ):  # 如果这一行包含"SSID"但不包含"BSSID"
            return line.split(":")[1].strip()  # 返回这一行的第二部分（即WiFi名称）
    return None  # 如果没有找到WiFi名称，返回None


def link_wifi():  # 登入校园网
    settings = configparser.ConfigParser()
    settings.read(path_settings)
    if settings["settings"]["wifi_free"] == "1":
        if get_connected_wifi_name() == "EcjtuLib_Free":
            requests.post(
                get_post_url(), data=get_post_data_free(), headers=get_post_header()
            )

    elif settings["settings"]["wifi_stu"] == "1":
        requests.post(get_post_url(), data=get_post_data(), headers=get_post_header())
    else:
        if get_connected_wifi_name() == "EcjtuLib_Free":
            requests.post(
                get_post_url(), data=get_post_data_free(), headers=get_post_header()
            )
        else:
            requests.post(
                get_post_url(), data=get_post_data(), headers=get_post_header()
            )

    with open(path_stats) as f:
        stats_f = json.load(f)
    stats_f["stats_times"] += 1
    with open(path_stats, "w") as f:
        json.dump(stats_f, f)


def logout():  # 注销校园网账户
    mac = re.findall("olmac='(.*?)'", requests.get("http://172.16.2.100/").text, re.S)[
        0
    ]
    url_out = (
        f"http://172.16.2.100:801/eportal/?c=ACSetting&a=Logout&wlanuserip=null&wlanacip=null&wlanacname=null"
        f"&port=&hostname=172.16.2.100&iTermType=1&session=null&queryACIP=0&mac={mac}"
    )
    post_data_out = {
        "c": "ACSetting",
        "a": "Logout",
        "wlanuserip": "null",
        "wlanacname": "null",
        "port": "",
        "hostname": "172.16.2.100",
        "iTermType": "1",
        "session": "null",
        "queryACIP": "0",
        "mac": f"{mac}",
    }
    requests.post(url_out, data=post_data_out, headers=get_post_header())


def create_files():  # 第一次运行，创建文件
    if not os.path.exists(path_private):
        os.makedirs(path_private)
    if not os.path.exists(path_settings):
        config = configparser.ConfigParser()
        config["login"] = {
            "save_account": "0",  # 是否保存账户
            "verify_account": "0",  # 是否验证账户
        }
        config["settings"] = {
            "auto_start": "0",  # 自启动
            "wifi_auto": "1",  # 选择WiFi，默认选择“自动选择”
            "wifi_free": "0",
            "wifi_stu": "0",
            "wait_time": 1,  # 等待时间
        }
        # 写入到文件
        with open(path_settings, "w") as config_file:
            config.write(config_file)
    if not os.path.exists(path_stats):
        dat = {
            "begin_day": get_today(),  # 开始使用时间
            "now_day": get_today(),  # 当前时间
            "announcement_day": "",  # 公告更新时间
            "stats_days": 0,  # 统计使用天数
            "stats_times": 0,  # 统计使用次数
        }
        with open(path_stats, "w") as f:
            json.dump(dat, f)


def change_settings(section, option, value):  # 快速修改设置的值
    settings = configparser.ConfigParser()
    settings.read(path_settings)
    settings.set(section, option, value)
    with open(path_settings, "w") as f_s:
        settings.write(f_s)


def get_today():  # 获取当前时间
    return datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")


def verify_wifi():  # 验证网络连接状态
    txt = """
    1: 网络未连接
    2: 已连接其他网络
    3: 连接了校园网，但未登入
    4: 连接了校园网，已登入
    """
    try:
        requests.get(baidu_url, timeout=0.5)
    except requests.exceptions.ConnectionError:
        try:
            requests.get(dr_url, timeout=0.5)
        except requests.exceptions.ConnectionError:
            return 1
    try:
        requests.get(dr_url, timeout=0.5)
    except requests.exceptions.Timeout:
        if requests.get(baidu_url).status_code == requests.codes.ok:
            return 2
    else:
        try:
            requests.get(baidu_url, timeout=0.5)
        except requests.exceptions.Timeout:
            return 3
        else:
            return 4
