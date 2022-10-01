from os import path as os_path
from sys import path as sys_path
from sys import argv

sys_path.append(os_path.join(os_path.dirname(argv[0]), "libs"))  # For dll & pyd s
