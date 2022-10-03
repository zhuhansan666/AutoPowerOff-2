from os import system, chdir, rmdir, makedirs, listdir, remove
from shutil import move, copy
from os import path as os_path
from sys import argv
from threading import Thread
from time import sleep


def get_current_path():
    p = os_path.normpath(argv[0])
    p = os_path.split(p)[0]
    if len(p) > 0:
        return p
    else:
        return "./"


def move_in_dir(path, want):
    # i = 0
    # failed = 0
    # files = list(listdir(path))
    # while len(files) > 0:
    #     if i - 1 > len(files):
    #         print(f"move {path} to {want} success")
    #         return True
    #     if failed > 3:
    #         return False
    #     if os_path.isdir(os_path.join(path, files[i])):
    #         try:
    #             move_in_dir(os_path.join(path, files[i]), os_path.join(want, files[i]))
    #         except Exception as e:
    #             print(f"move dir err: {e}")
    #     else:
    #         try:
    #             copy(os_path.join(path, files[i]), os_path.join(want, files[i]))
    #             remove(os_path.join(path, files[i]))
    #             i += 1
    #         except Exception as e:
    #             failed += 1
    #             print(f"move err: {e}")
    # return False
    system(f"move /y {path} {want}")


def rm_in_dir(path):
    # i = 0
    # failed = 0
    # files = list(listdir(path))
    # while len(files) > 0:
    #     if i - 1 > len(files):
    #         break
    #     if failed > 3:
    #         return False
    #     try:
    #         remove(os_path.join(path, files[i]))
    #         i += 1
    #     except Exception as e:
    #         failed += 1
    #         print(f"rmdir files err: {e}")
    # try:
    #     rmdir(path)
    #     print(f"rm {path} success")
    # except Exception as e:
    #     print(f"rmdir err: {e}")
    system(f"rmdir /s /q {path}")


chdir(get_current_path())

inp = "y"
if os_path.exists("./dist/bin") and os_path.isdir("./dist/bin"):
    inp = input("存在bin文件夹, 是否覆盖? (y/n): ").lower()

if inp == "y":
    main_py_t = Thread(
        target=lambda: system(r"pyinstaller -y -w -i .\Source\Installer.Resource\icon.ico .\Source\main.py"),
        daemon=True)
    defend_py_t = Thread(target=lambda: system(r"pyinstaller -y -w -i "
                                               r"./Defend/Installer.Resource/icon.ico -w ./Defend/defend.py"),
                         daemon=True)

    main_py_t.start()
    defend_py_t.start()

    while main_py_t.is_alive() or defend_py_t.is_alive():
        print("installing...", end="\r")

    rm_in_dir(r".\build")

    if not os_path.exists("./dist/bin"):
        makedirs("./dist/bin")

    main_move_t = Thread(target=lambda: move_in_dir(r".\dist\defend\*.*", r".\dist\bin"), daemon=True)
    defend_move_t = Thread(target=lambda: move_in_dir(r".\dist\main\*.*", r".\dist\bin"), daemon=True)

    main_move_t.start()
    defend_move_t.start()

    while main_move_t.is_alive() or defend_py_t.is_alive():
        print("moving files...", end="\r")

    # rm_in_dir(r".\dist\main")
    # rm_in_dir(r".\dist\defend")

    system("del *.spec")

    system("pyinstaller -y -Fw ./Startup/Startup.py")
