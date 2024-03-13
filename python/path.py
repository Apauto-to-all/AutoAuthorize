import sys

version = 'v2.2.3'  # 当前程序版本号

main_have_open = 0  # 全局变量：是否已经打开主界面

have_save_account = 0  # 全局变量：是否已经保存账号

wait_time = 120  # 全局变量：等待时间

path_base = r'personalData'  # 保存数据的文件夹

path_private = path_base + r'/data/private'  # 保存私人数据的文件夹

path_header = path_base + r'/data/private/post_header.json'  # 保存header数据的文件

path_account = path_base + r'/data/private/account.json'  # 保存账号密码的文件

path_settings = path_base + r'/data/settings.ini'  # 保存设置的文件

path_announcement = path_base + r'/data/announcement.txt'  # 保存公告的文件

path_stats = path_base + r'/data/stats.json'  # 保存统计数据的文件

github_url = 'https://github.com/Apauto-to-all/AutoAuthorize'  # github地址

dr_url = "http://172.16.2.100/"  # 校园网地址

baidu_url = 'https://www.baidu.com/'  # 百度地址

announcement_url = 'https://raw.githubusercontent.com/Apauto-to-all/AutoAuthorize/main/announcement.txt'  # 公告地址

version_url = 'https://raw.githubusercontent.com/Apauto-to-all/AutoAuthorize/main/version.txt'  # 版本号地址

path_program = sys.executable  # 程序路径

lzy_url = 'https://www.lanzoub.com/b052h91gb'  # 蓝奏云地址
lzy_password = 'ecjt'  # 蓝奏云密码
