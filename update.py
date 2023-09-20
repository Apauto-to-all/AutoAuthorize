import datetime
import json
import os

import requests
from path import path_announcement, path_stats
from login import get_today


def update_announcement():
    announcement_url = 'https://ghproxy.com/https://raw.githubusercontent.com/Apauto-to-all/AutoAuthorize/main/announcement.json'
    request = requests.get(announcement_url)  # 此时在内存为response响应对象开辟空间，从服务器返回的数据也是一直存储在内存中中
    if request.status_code == 200:
        with open(path_announcement, "wb") as f:
            f.write(request.content)  # 调用write方法时将内存中的二进制数据写入硬盘
        with open(path_stats) as f:
            up_announcement_day = json.load(f)
        up_announcement_day['announcement_day'] = get_today()
        with open(path_stats, 'w') as f:
            json.dump(up_announcement_day, f)
    else:
        if not os.path.exists(path_announcement):
            with open(path_announcement, 'w') as f:
                json.dump({get_today(): "更新公告失败，请检查网络，检测无误后，请点击以下“立即更新公告”按钮重新更新公告"},
                          f)
        else:
            with open(path_announcement) as f:
                ac = json.load(f)
            ac[get_today()] = "更新公告失败，请检查网络，检测无误后，请点击以下“立即更新公告”按钮重新更新公告"
            with open(path_announcement, 'w') as f:
                json.dump(ac, f)


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


def update_stats_times():
    with open(path_stats) as f:
        stats_f = json.load(f)
    stats_f['stats_times'] += 1
    with open(path_stats) as f:
        json.dump(stats_f, f)


def update_announcement_days():
    with open(path_stats) as f:
        s = json.load(f)
    days = s['stats_days']
    times = s['times_update']
    if times * 7 < days:
        update_announcement()
        s['times_update'] += int(days / 7 - times + 1)
        with open(path_stats, 'w') as f:
            json.dump(s, f)


def update_app_version():
    version_url = ''


def update_show_ds():
    with open(path_stats) as f:
        s = json.load(f)
    days = s['stats_days']
    times = s['stats_times']
    if days > 7 and times > 7:
        s['da_qty'] = 1
        with open(path_stats, 'w') as f:
            json.dump(s, f)
        return 1
    else:
        return 0
