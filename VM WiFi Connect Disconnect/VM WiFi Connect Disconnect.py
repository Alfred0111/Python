import os
import time
import sys


# DEFINE PARM
action = sys.argv[1]
num = sys.argv[2]
ssid = sys.argv[3]
security = sys.argv[4]
mode = sys.argv[5]
vm_report = rf"C:\Auto_Test_Folder\Report\report{str(num)}.txt"


# CHECK SECURITY TYPE AND DEFINE VARIABLE
if security == "none":
    secname = "none"
    status = "開啟"
    pfname = "AutoTest_none"
elif security == "WPA2":
    secname = "WPA2_personal"
    status = "WPA2-Personal"
    pfname = "AutoTest_WPA2_personal"
else:
    secname = "WPA3_personal"
    status = "WPA3-個人"
    pfname = "AutoTest_WPA3_personal"

# PRE ACTION
# Clear VM report
if os.path.exists(vm_report):
    os.remove(vm_report)

# DEFINE FUNCTION
def log(message):
    with open(vm_report, "a+") as text_file:
        print(message, file=text_file)

def connect():
    os.system("netsh wlan delete profile name=*") #0 - delete wifi profile
    time.sleep(2)
    if mode == "auto":
        os.system(rf"netsh wlan add profile filename=C:\Auto_Test_Folder\WLAN-{secname}.xml") #1 - Import wifi profile(auto)
    else:
        os.system(rf"netsh wlan add profile filename=C:\Auto_Test_Folder\WLAN-{secname}_manual.xml") #1 - Import wifi profile(manual)
    time.sleep(3)
    os.system(rf"netsh wlan connect name=AutoTest_{secname} ssid={ssid} interface=WLAN") #2 - Connect to wifi
    time.sleep(20)
    os.system(r"netsh wlan show interface > C:\Auto_Test_Folder\connect.txt") #3 - Confirm status and return status
    text = open(r"C:\Auto_Test_Folder\connect.txt",'r') #4 - Read the status
    connectres = text.read()
    text.close()
    return connectres

# MAIN
connectres = connect()
if "連線" in connectres and ssid in connectres and status in connectres and pfname in connectres:
    print("Connect to Wifi successfully!")
    log(f"VM {str(num)} connect to Wifi successfully!")
    time.sleep(5)
else:
    print("Connect to Wifi failed!")
    log(f"VM {str(num)} connect to Wifi failed!")
    os.system(r'net use z: \\10.0.200.200\wifi_report test@1234 /user:Administrator /persistent:NO')
    os.system(rf'copy {vm_report} z:\ ')
