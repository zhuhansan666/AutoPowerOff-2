# Python Wheels Import
from os import getenv
from os import path as os_path

# My Files Import
from Tools import FileTools


# End Import

class AppConfig:
    def __init__(self):
        self.paths = [
            "config_file",
            "config_file_old"
        ]

        self.__file_tools = FileTools()

        self.defend_exe = "./defend.exe -1 main.exe"

        self.app_dirname = "./AutoPowerOff"

        self.config_file_path = getenv("appdata")
        if self.config_file_path is None:
            self.config_file_path = "./Resource/Config/"
        else:
            self.config_file_path = os_path.join(self.config_file_path, os_path.join(self.app_dirname,
                                                                                     "./Config/"))

        self.config_file = os_path.join(self.config_file_path, "./Config.cfg.json")
        self.config_file_old = self.config_file + ".old"

        for _k, _i in self.__dict__.items():  # 格式化路径 并 创建文件
            if type(_i) == str and _k in self.paths and str(_i)[-1] != "/" and all(
                    self.__file_tools.is_true_path(os_path.normpath(_i),
                                                   create=True)):
                self.__dict__[_k] = os_path.normpath(_i)

        self.server_url = "https://Unknown"
        self.get_config_url = self.server_url + "/api/get/config"

        self.get_time_url = "https://www.tsa.cn/api/time/getCurrentTime"
        self.get_time_wait = 1

        self.runtime_file = "./.runtime"
