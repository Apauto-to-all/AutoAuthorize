import datetime
import json
import os
import re
import configparser
import wmi

from path import path_header, path_settings, path_data, path_account, path_private, path_stats, path_data_free, \
    github_url, dr_url
import requests


def link_github():
    os.system(f'start {github_url}')


def link_dr():
    os.system(f'start {dr_url}')


def get_nc():
    with open(path_account) as f:
        account = json.load(f)
    return list(account.keys())[0]


def get_post_url():
    url = "http://172.16.2.100/"
    html = requests.get(url).text
    ip4_y = re.search("v4ip='(.*?)';", html, re.S)
    ip4_n = re.search("v46ip='(.*?)' ", html, re.S)
    if ip4_y is None:
        ip4 = ip4_n.group(1)
    else:
        ip4 = ip4_y.group(1)
    return (f"http://172.16.2.100:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=172.16.2.100&iTermType=1"
            f"&wlanuserip={ip4}&wlanacip=null&wlanacname=null&mac=00-00-00-00-00-00&ip={ip4}&enAdvert=0"
            f"&queryACIP=0&loginMethod=1")


def get_post_data():
    with open(path_data) as f:
        post_data = json.load(f)
    return post_data


def get_post_data_free():
    with open(path_data_free) as f:
        post_data_free = json.load(f)
    return post_data_free


def get_post_header():
    with open(path_header) as f:
        post_header = json.load(f)
    return post_header


def get_operator_last(operator):
    if operator == '中国移动':
        kk = '@cmcc'
    elif operator == '中国电信':
        kk = '@telecom'
    elif operator == '中国联通':
        kk = '@unicom'
    else:
        kk = None
    return kk


def save_post_data_header(username, password, operator):
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
        "Login": ""
    }
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
        "Login": ""
    }  # 用于图书馆免费网络登入
    post_header = {  # 拿来的
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 "
                      "Safari/537.36"
    }
    with open(path_data, 'w') as f_d:
        json.dump(post_data, f_d)
    with open(path_data_free, 'w') as f_d_f:
        json.dump(post_data_free, f_d_f)
    with open(path_header, 'w') as f_h:
        json.dump(post_header, f_h)


def save_account(nc, username, password, operator):
    if nc == "":
        nc = username
    with open(path_account, 'w') as f_account:
        json.dump({nc: [username, password, operator]}, f_account)
    save_post_data_header(username, password, operator)


def link_wifi():
    settings = configparser.ConfigParser()
    settings.read(path_settings)
    if settings['settings']['wifi_free'] == '1':
        requests.post(get_post_url(), data=get_post_data_free(), headers=get_post_header())
    elif settings['settings']['wifi_stu'] == '1':
        requests.post(get_post_url(), data=get_post_data(), headers=get_post_header())
    else:
        requests.post(get_post_url(), data=get_post_data(), headers=get_post_header())
        if verify_wifi() == 3:
            logout()
            requests.post(get_post_url(), data=get_post_data_free(), headers=get_post_header())

    with open(path_stats) as f:
        stats_f = json.load(f)
    stats_f['stats_times'] += 1
    with open(path_stats, 'w') as f:
        json.dump(stats_f, f)


def get_mac_address():
    s = wmi.WMI()
    mac_addresses = []
    for nw in s.Win32_NetworkAdapterConfiguration(IPEnabled=1):
        mac = str(nw.MACAddress).replace(':', '').lower()
        mac_addresses.append(mac)
    mac_addresses = mac_addresses[0]
    return mac_addresses


def logout():
    mac = get_mac_address()
    url_out = f'http://172.16.2.100:801/eportal/?c=ACSetting&a=Logout&wlanuserip=null&wlanacip=null&wlanacname=null' \
              f'&port=&hostname=172.16.2.100&iTermType=1&session=null&queryACIP=0&mac={mac}'
    post_data_out = {
        'c': 'ACSetting',
        'a': 'Logout',
        'wlanuserip': 'null',
        'wlanacname': 'null',
        'port': '',
        'hostname': '172.16.2.100',
        'iTermType': '1',
        'session': 'null',
        'queryACIP': '0',
        'mac': f'{mac}'
    }
    requests.post(url_out, data=post_data_out, headers=get_post_header())


def create_files():
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
            "wifi_auto": "1",  # 选择WiFi
            "wifi_free": "0",
            "wifi_stu": "0",
        }
        # 写入到文件
        with open(path_settings, 'w') as config_file:
            config.write(config_file)
    if not os.path.exists(path_stats):
        dat = {
            "begin_day": get_today(),
            "now_day": get_today(),
            "announcement_day": "not updated",
            "stats_days": 0,
            "stats_times": 0,
            "times_update": 0,
            "da_qty": 0
        }
        with open(path_stats, 'w') as f:
            json.dump(dat, f)


def change_settings(section, option, value):
    settings = configparser.ConfigParser()
    settings.read(path_settings)
    settings.set(section, option, value)
    with open(path_settings, "w") as f_s:
        settings.write(f_s)


def get_today():
    return datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')


def verify_wifi():
    txt = """
    1: 网络未连接
    2: 已连接其他网络
    3: 连接了校园网，但未登入
    4: 连接了校园网，已登入
    """
    url1 = 'http://172.16.2.100'
    url2 = 'https://www.baidu.com/'
    try:
        requests.get(url2, timeout=0.5)
    except requests.exceptions.ConnectionError:
        try:
            requests.get(url1, timeout=0.5)
        except requests.exceptions.ConnectionError:
            return 1
    try:
        requests.get(url1, timeout=0.5)
    except requests.exceptions.Timeout:
        if requests.get(url2).status_code == requests.codes.ok:
            return 2
    else:
        try:
            requests.get(url2, timeout=0.5)
        except requests.exceptions.Timeout:
            return 3
        else:
            return 4
