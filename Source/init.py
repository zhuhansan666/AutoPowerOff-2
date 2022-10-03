# Python Wheels Import
from threading import Thread
from os import chdir as set_work_path

# My Files Import
from defend import Defend
from g import tools
from g import app_config

# End Import
work_path = tools.get_current_path()
set_work_path(work_path)


# 使用defend保证defend.exe运行
defend = Defend(pid=-1, file=app_config.defend_exe)  # .exe file
defend_thread = Thread(target=defend.mainloop, daemon=True)
defend_thread.start()
