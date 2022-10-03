from os import startfile, getenv, remove, path, chdir
from subprocess import run
from log import Logging
import ctypes
from sys import argv, exit, executable

logging = Logging()
logging.write_log(None)
logging.write_log("In Startup.py INFO: Welcome to use the AutoPowerOff 2.0, this is the StartUp file.")

temp_dir = getenv("temp")


def get_current_path():
    p = path.normpath(argv[0])
    p = path.split(p)[0]
    if len(p) > 0:
        return p
    else:
        return "./"


chdir(get_current_path())


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin(), "Success"
    except Exception as e:
        return False, e


def startUp(reg_name: str, temp_file: str = "./startup.reg"):
    reg_info = r"""Windows Registry Editor Version 5.00    
[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run]
"{}"="{}"
""".format(reg_name, argv[0])

    try:
        with open(temp_file, "w+") as f:
            f.write(reg_info)
    except Exception as e:
        return -1, f"Reg 文件写入失败: {e}"

    try:
        run(f"regedit /s {temp_file}")
    except Exception as e:
        return -2, f"Reg 注册失败: {e}"

    try:
        remove(temp_file)
    except Exception as e:
        return -3, f"Reg 文件删除失败: {e}"

    return 0, "Success"


if is_admin()[0]:
    logging.write_log("In Startup.py INFO: 管理员权限获取成功")
    res = startUp("APO2", path.join(temp_dir, "Startup.reg"))
    if res[0] != 0:
        logging.write_log(f"In Startup.py ERROR: {res[1]} (err code: {res[0]})")
    else:
        logging.write_log("In Startup.py INFO: 自启动写入成功")

    chdir("./bin")  # 以免 main.exe 无法加载dll

    try:
        startfile("main.exe")
    except Exception as e:
        logging.write_log(f"In Startup.py ERROR: Start ./bin/main.exe error: {e}")
else:
    logging.write_log("In Startup.py INFO: 尝试获取管理员权限")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, __file__, None, 1)  # 申请管理员权限
    exit(-1)
