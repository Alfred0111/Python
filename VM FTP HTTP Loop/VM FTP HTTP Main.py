import os
import time
import sys
import re
from shutil import copyfile
from auto_pkg.auto import Bcolors, Format_check, System


# DEFINE PARM
action = sys.argv[1]
method = sys.argv[2]
vmnumber = sys.argv[3]
print(f"{Bcolors.PARM_YELLOW}ACTION is {action}{Bcolors.ENDC}")
print(f"{Bcolors.PARM_YELLOW}METHOD is {method}{Bcolors.ENDC}")
print(f"{Bcolors.PARM_YELLOW}VMNUMBER is {vmnumber}{Bcolors.ENDC}")

if action == "Start":
    mode = sys.argv[4]
    value = sys.argv[5]
    url = sys.argv[6]
    print(f"{Bcolors.PARM_YELLOW}MODE is {mode}{Bcolors.ENDC}")
    if mode != "Loop":
        print(f"{Bcolors.PARM_YELLOW}VALUE is {value}{Bcolors.ENDC}")
    print(f"{Bcolors.PARM_YELLOW}URL is {url}{Bcolors.ENDC}")

bat_copy = "D:\Dropbox\WiFi Test Automation\VM FTP HTTP Loop\Server call VM to copy file.bat"
py_exe = "C:\Python36\python.exe"
py_main = "C:/Auto_Test_Folder/VM FTP HTTP Loop.py"


# VM NUMBER FORMAT CHECK
Format_check.vmnum_check(method, vmnumber)


# PRE ACTION
# Server_A copy python file to wilf_python folder
copyfile("D:\Dropbox\WiFi Test Automation\VM FTP HTTP Loop\VM FTP HTTP Loop.py", "C:\wifi_python\VM FTP HTTP Loop.py")

# MAIN
if method == "Continuity":
    vmn = vmnumber.split("-")
    if action == "Start":
        for i in range(int(vmn[0]), int(vmn[1])+1):
            print(f"{Bcolors.INFO_BLUE}VM {str(i)} start HTTP ping and FTP download loop{Bcolors.ENDC}")
            System.copyfile(i, bat_copy)
            System.fh_loop_start(i, action, mode, value, url)
    else:
        for i in range(int(vmn[0]), int(vmn[1])+1):
            print(f"{Bcolors.INFO_BLUE}VM {str(i)} stop HTTP ping and FTP download loop{Bcolors.ENDC}")
            System.loop_stop(i)
else:
    vmn = vmnumber.split(",")
    count = 0
    listlen = len(vmn)
    if action == "Start":
        while count < listlen:
            print(f"{Bcolors.INFO_BLUE}VM {str(vmn[count])} start HTTP ping and FTP download loop{Bcolors.ENDC}")
            System.copyfile(int(vmn[count]), bat_copy)
            System.fh_loop_start(int(vmn[count]), action, mode, value, url)
            count += 1
    else:
        while count < listlen:
            print(f"{Bcolors.INFO_BLUE}VM {str(vmn[count])} stop HTTP ping and FTP download loop{Bcolors.ENDC}")
            System.loop_stop(int(vmn[count]))
            count += 1

