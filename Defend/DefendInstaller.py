from os import system
system("taskkill /im defend.exe /f")
system("""pyinstaller -i ./Installer.Resource/icon.ico -w --runtime-hook="hook_dll.py" -y defend.py""")

"""
base_library.zip
python38.dll
pythoncom38.dll
pywintypes38.dll
VCRUNTIME140.dll
psutil (Dir)
必须放在同目录
"""
