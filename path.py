import sys
import winshell

path_base = winshell.application_data() + r'\Auto_Login_ECJTU_WiFi'

path_private = path_base + r'/data/private'

path_data = path_base + r'/data/private/post_data.json'

path_data_free = path_base + r'/data/private/post_data_free.json'

path_header = path_base + r'/data/private/post_header.json'

path_account = path_base + r'/data/private/account.json'

path_settings = path_base + r'/data/settings.ini'

path_announcement = path_base + r'/data/announcement.txt'

path_stats = path_base + r'/data/stats.json'

path_version = path_base + r'/version.txt'

path_program = sys.executable


