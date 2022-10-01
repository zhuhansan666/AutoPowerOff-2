from os import system
system("taskkill /im main.exe /f")
system("""pyinstaller -i ./Installer.Resource/icon.ico --runtime-hook="hook_dll.py" -y main.py""")

"""
base_library.zip
python38.dll
pythoncom38.dll
pywintypes38.dll
VCRUNTIME140.dll
psutil (Dir)
必须放在同目录
"""
