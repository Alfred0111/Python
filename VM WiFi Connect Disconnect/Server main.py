import time
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

if action == "Connect":
    security = sys.argv[4]
    ssid = sys.argv[5]
    password = sys.argv[6]
    print(f"{Bcolors.PARM_YELLOW}SECURITY is {security}{Bcolors.ENDC}")
    print(f"{Bcolors.PARM_YELLOW}SSID is {ssid}{Bcolors.ENDC}")
    if security != 'none':
        print(f"{Bcolors.PARM_YELLOW}PASSWORD is {password}{Bcolors.ENDC}")

mode = sys.argv[7]
print(f"{Bcolors.PARM_YELLOW}MODE is {mode}{Bcolors.ENDC}")

bat_copy = "D:\Dropbox\WiFi Test Automation\VM WiFi Connect Disconnect\Server call VM to copy file.bat"
py_exe = "C:\Python36\python.exe"
py_main = "C:/Auto_Test_Folder/VM WiFi Connect Disconnect.py"


# VM NUMBER FORMAT CHECK
Format_check.vmnum_check(method, vmnumber)


# SSID FORMAT CHECK
if action == "Connect":
    Format_check.ssid_check(ssid)


# MODIFY WIFI PROFILE
if action == "Connect" and (security == "WPA2" or security == "WPA3") and mode =="Auto":
    WiFi_control.profile_edit_auto_pwd(security, ssid, password)
elif action == "Connect" and (security == "WPA2" or security == "WPA3") and mode == "Manual":
    WiFi_control.profile_edit_manual_pwd(security, ssid, password)
elif action == "Connect" and mode == "Auto":
    WiFi_control.profile_edit_auto(security, ssid)
elif action == "Connect" and mode == "Manual":
    WiFi_control.profile_edit_manual(security, ssid)


# PRE ACTION
# Server_A copy python script to C:
copyfile("D:\Dropbox\WiFi Test Automation\VM WiFi Connect Disconnect\VM WiFi Connect Disconnect.py","C:\wifi_python\VM WiFi Connect Disconnect.py")
#Clear Server_A report file in wifi_report folder
System.server_rep_clear()


# MAIN
if method == "Continuity":
    vmn = vmnumber.split("-")
    if action == "Connect":
        for i in range(int(vmn[0]), int(vmn[1])+1):
            System.copyfile(i, bat_copy)
            System.callvm_py(i, py_exe, py_main, action, ssid, security, mode)
    else:
        for i in range(int(vmn[0]), int(vmn[1])+1):
            print(f"{Bcolors.INFO_BLUE}VM {str(i)} disconnect to wifi{Bcolors.ENDC}")
            WiFi_control.wifi_disconnect(i)
else:
    vmn = vmnumber.split(",")
    count = 0
    listlen = len(vmn)
    if action == "Connect":
        while count < listlen:
            System.copyfile(int(vmn[count]), bat_copy)
            System.callvm_py(int(vmn[count]), py_exe, py_main, action, ssid, security, mode)
            count += 1
    else:
        while count < listlen:
            print(f"{Bcolors.INFO_BLUE}VM {str(vmn[count])} disconnect to wifi{Bcolors.ENDC}")
            WiFi_control.wifi_disconnect(int(vmn[count]))
            count += 1

# POST ACTION
#Check if the VM connected to wifi successfully
if action == "Connect":
    time.sleep(30)
    System.connection_check(method, vmnumber)
