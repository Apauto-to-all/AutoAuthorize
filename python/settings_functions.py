import os
import re
import winreg
import winshell
from path import path_program


def startup():
    # 获取自启动文件夹的路径
    startup_path = winshell.startup()
    # 连接文件名与自启动文件夹的路径
    lnk_path = startup_path + '\\' + ink_name + '.lnk'
    # 创建快捷方式，第一个Path为连接后的目标路劲，第二个Target为触发文件路径
    winshell.CreateShortcut(Path=lnk_path, Target=path_program)


def del_startup():
    # 获取自启动文件夹的路径
    startup_path = winshell.startup()
    # 连接文件名与自启动文件夹的路径
    lnk_path = startup_path + '\\' + ink_name + '.lnk'
    # 如果快捷方式存在，则删除之
    if os.path.isfile(lnk_path):
        os.remove(lnk_path)


def create_regedit():
    # 注册表项的路径及名称
    key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    # 创建要写入的键名
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
    # 设置键值数据，用于在开机时自动运行程序
    winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, path_program)
    # 关闭注册表项句柄
    winreg.CloseKey(key)


def del_regedit():
    # 注册表项的路径及名称
    key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    # 打开要修改的键
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
    try:
        # 删除指定键名的键值
        winreg.DeleteValue(key, key_name)
    except FileNotFoundError:
        pass
    # 关闭注册表项句柄
    winreg.CloseKey(key)


def desktop():
    desk_path = winshell.desktop()
    lnk_path = desk_path + '\\' + ink_name + '.lnk'
    winshell.CreateShortcut(lnk_path, path_program)


def del_desktop():
    desk_path = winshell.desktop()
    lnk_path = desk_path + '\\' + ink_name + '.lnk'
    if os.path.isfile(lnk_path):
        os.remove(lnk_path)


def check_version(version):
    pattern = r'^v\d+\.\d+\.\d+$'
    if not re.match(pattern, version):
        return False
    major, minor, patch = map(int, version[1:].split('.'))
    if major < 0 or minor < 0 or patch < 0:
        return False
    if major == 0 and minor == 0 and patch == 0:
        return False
    return True


key_name = "Auto_login_ECJTU_wifi"  # 注册表中自启动程序的键名

ink_name = "自动登入校园网2.0"
