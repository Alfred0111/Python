import sys
from shutil import copyfile
from auto_pkg.auto import Bcolors, Format_check, WiFi_control, System


# DEFINE PARAMETER
action = sys.argv[1]
method = sys.argv[2]
vmnumber = sys.argv[3]
print(f"{Bcolors.PARM_YELLOW}ACTION is {action}{Bcolors.ENDC}")
print(f"{Bcolors.PARM_YELLOW}METHOD is {method}{Bcolors.ENDC}")
print(f"{Bcolors.PARM_YELLOW}VMNUMBER is {vmnumber}{Bcolors.ENDC}")
mode = sys.argv[4]
value = sys.argv[5]
security = sys.argv[6]
ssid = sys.argv[7]
password = sys.argv[8]

if action != 'Stop':
    print(f"{Bcolors.PARM_YELLOW}MODE is {mode}{Bcolors.ENDC}")
    if mode != 'Loop':
        print(f"{Bcolors.PARM_YELLOW}VALUE is {value}{Bcolors.ENDC}")
    print(f"{Bcolors.PARM_YELLOW}SECURITY is {security}{Bcolors.ENDC}")
    print(f"{Bcolors.PARM_YELLOW}SSID is {ssid}{Bcolors.ENDC}")
    if security != 'none':
        print(f"{Bcolors.PARM_YELLOW}PASSWORD is {password}{Bcolors.ENDC}")

bat_copy = "D:\Dropbox\WiFi Test Automation\VM WiFi Connect Loop\Server call VM to copy file.bat"
py_exe = "C:\Python36\python.exe"
py_main = "C:/Auto_Test_Folder/VM WiFi Connect Loop.py"


# VM NUMBER FORMAT CHECK
Format_check.vmnum_check(method, vmnumber)


# SSID FORMAT CHECK
if action == "Start":
    Format_check.ssid_check(ssid)


# MODIFY WIFI PROFILE
if action == "Start" and (security == "WPA2" or security == "WPA3"):
    WiFi_control.profile_edit_manual_pwd(security, ssid, password)
elif action == "Start" and security == "none":
    WiFi_control.profile_edit_manual(security, ssid)


# PRE ACTION
#Server_A copy python file to wilf_python folder
copyfile("D:\Dropbox\WiFi Test Automation\VM WiFi Connect Loop\VM WiFi Connect Loop.py","C:\wifi_python\VM WiFi Connect Loop.py")


# MAIN
if method == "Continuity":
    vmn = vmnumber.split("-")
    if action == "Start":
        for i in range(int(vmn[0]), int(vmn[1])+1):
            print(f"{Bcolors.INFO_BLUE}VM {str(i)} start wifi connect disconnect loop{Bcolors.ENDC}")
            System.copyfile(int(i), bat_copy)
            System.loop_start(int(i), action, ssid, security, mode, value)
    else:
        for i in range(int(vmn[0]), int(vmn[1])+1):
            print(f"{Bcolors.INFO_BLUE}VM {str(i)} stop wifi connect disconnect loop{Bcolors.ENDC}")
            System.loop_stop(int(i))
else:
    vmn = vmnumber.split(",")
    count = 0
    listlen = len(vmn)
    if action == "Start":
        while count < listlen:
            print(f"{Bcolors.INFO_BLUE}VM {str(vmn[count])} start wifi connect disconnect loop{Bcolors.ENDC}")
            System.copyfile(int(vmn[count]), bat_copy)
            System.loop_start(int(vmn[count]), action, ssid, security, mode, value)
            count += 1
    else:
        while count < listlen:
            print(f"{Bcolors.INFO_BLUE}VM {str(vmn[count])} stop wifi connect disconnect loop{Bcolors.ENDC}")
            System.loop_stop(int(vmn[count]))
            count += 1



