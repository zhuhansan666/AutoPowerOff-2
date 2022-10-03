"""
作者: 爱和牛奶的涛哥
"""
# Python Wheels Import
from sys import argv
from threading import Thread
# from win32gui import *
from traceback import format_exc
from subprocess import run
from requests import get
from os import path as os_path
from time import sleep, strftime, localtime, time

# My Files Import
from g import logging, VERSION, app_config, tools, file_tools
from config import config, Config
from init import work_path, defend_thread
from ui import Ui, UiConfig

# End Import

Shutdown = False if os_path.splitext(argv[0])[-1] == ".py" else True


class RunTime:
    def __init__(self, _app_config):
        self.runtime_file = _app_config.runtime_file
        self.__file_tools = file_tools

        self.runtime = {"shutdown": False}

    def write(self):
        created = False

        res = self.__file_tools.create_file(self.runtime_file)
        if res[0] == 0:
            # logging.write_log("In Main.py RunTime.class INFO: 创建 \"{}\" 成功".format(self.runtime_file))
            created = True
        elif res[0] == -4:
            # logging.write_log("In Main.py RunTime.class INFO: \"{}\" 已存在, 无需创建".format(self.runtime_file))
            created = True
        else:
            logging.write_log("In Main.py RunTime.class ERROR: 创建 \"{}\" 发生错误: error: {}; info: "
                              "\"{}\"".format(self.runtime_file, *res))

        if created:
            res = self.__file_tools.write_json(self.runtime_file, self.runtime)
            if res[0] == 0:
                # logging.write_log("In Main.py RunTime.class INFO: 写入 \"{}\" 成功".format(self.runtime_file))
                pass
            else:
                logging.write_log("In Main.py RunTime.class ERROR: 写入 \"{}\" 发生错误: error: {}; info: "
                                  "\"{}\"".format(self.runtime_file, *res))


class Background:
    def __init__(self, _config: Config, _app_config, _runtime):
        self.__config = _config
        self.__app_config = _app_config
        self.__runtime = _runtime
        self.__tools = tools

        self.__runtime.write()

        self.utc_add_8 = 0
        self.get_time_wait = self.__app_config.get_time_wait
        self.proofread_time = True
        self.get_time_url = self.__app_config.get_time_url
        self.time_format = "%H:%M"
        self.time_string = ""

        self.proofread_time_thread = Thread(target=self.proofread_time_thread, daemon=True)
        self.proofread_time_thread.start()

        self.will_shutdown = False

        self.ui_config = UiConfig()

    def proofread_time_thread(self):
        while self.proofread_time:
            sleep(self.get_time_wait)
            try:
                res = get(self.get_time_url).text
                if self.__tools.is_num(res, "int"):
                    res = int(res)
                else:
                    res = 0
            except Exception as e:
                res = 0

            if res != 0:
                self.utc_add_8 = res / 1000
            else:
                self.utc_add_8 = time()

            self.time_string = strftime(self.time_format, localtime(self.utc_add_8))

    def format_time(self, string: str):
        _string = ""
        for c in string.split(":"):
            if self.__tools.is_num(c, "int"):
                c = "%.2d:" % int(c)
            else:
                return "17:25"
            _string += c
        return _string[:-1]

    def mainloop(self):
        while True:
            sleep(1)

            config_time = self.format_time(self.__config.now_config.get("shutdown", "17:25"))

            self.will_shutdown = self.time_string == config_time

            self.__runtime.runtime = {"shutdown": self.will_shutdown}
            self.__runtime.write()

            if self.will_shutdown:
                try:
                    ui = Ui(self.ui_config)
                    res = ui.mainloop(self.__config.now_config.get("timeout", 30))
                except Exception as e:
                    res = 1
                    logging.write_log("In main.py ERROR: load ui error: {}".format(e))
                if res == 0:
                    if Shutdown is not False:
                        run("shutdown /f /s /t 1")  # 关机
                        logging.write_log("In main.py INFO: Shut downing...")
                        return
                    else:
                        logging.write_log("In main.py DEBUG: Shut downing... (并不会真的关机)")
                        print("In the Debug mode.")
                        return
                else:
                    logging.write_log("In main.py INFO: Shutdown closed.")
                    return


runtime_file = "./" + os_path.splitext(os_path.split(argv[0])[1])[0] + ".runtime"  # 当前文件名 (无后缀) + .runtime

app_config.runtime_file = runtime_file

runtime = RunTime(app_config)

background = Background(config, app_config, runtime)
background.mainloop()

logging.write_log("In main.py INFO: 感谢使用 自动关机2.0 {}, GitHub: https://github.com/zhuhansan666/AutoPowerOff-2-client"
                  .format(VERSION))
