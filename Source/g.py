# Python Wheels Import

# My Files Import
from log import Logging
from Tools import Tools, FileTools
from AppConfig import AppConfig
from VERSION import VERSION

# End Import

logging = Logging()
logging.write_log(None)
file_tools = FileTools()
tools = Tools()

app_config = AppConfig()

# from config import Config

# config = Config(app_config)
