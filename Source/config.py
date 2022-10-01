# Python Wheels Import
from json import dumps, loads
from traceback import format_exc
from requests import get

# My Files Import
from g import logging, app_config, file_tools


# End Import


class Config:
    def __init__(self, _app_config):
        self.__app_config = _app_config
        self.__file_tools = file_tools

        self.paths = _app_config.paths
        self.config_files = {}
        self.files = self.__app_config.__dict__.items()

        self.def_config = {
            "shutdown": "17:25",
            "timeout": 30,
        }

        self.now_config = {}

        self.config_files = self.load()
        self.set_config(self.load())
        req = self.req(self.__app_config.get_config_url)
        if req.get("error", None) != -1:
            self.set_config(req)
        self.write()

    def req(self, url):
        try:
            json_info = loads(get(url).text)
        except Exception as e:
            json_info = {"error": -1}
            logging.write_log("In Config.py ERROR: Requests Error: {}".format(repr(e)))

        return json_info

    def set_config(self, dic: dict):
        def_keys = list(self.def_config.keys())
        for k, i in self.files:
            if k in self.paths:
                config_keys = list(self.config_files[i].keys())
                for dic_k in dic.keys():
                    if dic_k in def_keys and dic_k not in config_keys:
                        self.config_files[i][dic_k] = dic.get(dic_k, None)

                for def_k in def_keys:
                    if def_k not in config_keys:
                        self.config_files[i][def_k] = self.def_config.get(def_k, None)

    def load(self):
        config_files = {}
        for k, i in self.files:
            if k in self.paths:
                res = file_tools.read_json(i)
                if res[0] == 0:
                    logging.write_log("In Config.py INFO: 读取 \"{}\" 成功".format(i))
                    config_files[i] = res[1]
                    if i[-4:] != ".old":
                        self.now_config = res[1]
                else:
                    logging.write_log(
                        "In Config.py ERROR: 读取 \"{}\" 发生错误: error: {}; info: \"{}\"".format(i, *res))
                    config_files[i] = {"error": res[1]}

        return config_files

    def write(self):
        for k, i in self.files:
            if k in self.paths:
                res = file_tools.write_json(i, self.config_files.get(i, {}))
                if res[0] == 0:
                    now_config = self.config_files.get(i, None)
                    logging.write_log("In Config.py INFO: 写入 \"{}\" 成功".format(i))
                else:
                    logging.write_log(
                        "In Config.py ERROR: 写入 \"{}\" 发生错误: error: {}; info: \"{}\"".format(i, *res))




config = Config(app_config)
