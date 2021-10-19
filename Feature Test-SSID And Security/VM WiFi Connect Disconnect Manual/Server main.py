#**********IMPORT MODULE**********#
import os 
import time  
import sys
import glob
from shutil import copyfile
import re

#**********DEFINE ANSI COLOR CODE**********#
class bcolors():
    HEADER_PURPLE = '\033[0;35m'
    INFO_CYAN = '\033[36m'
    PASS_GREEN = '\033[92m'
    WARNING_YELLOW = '\033[93m'
    FAIL_RED = '\033[91m'
    ENDC = '\033[0m'
'''
print(f"{bcolors.HEADER_PURPLE}Text{bcolors.ENDC}")
print(f"{bcolors.INFO_CYAN}Text{bcolors.ENDC}")
print(f"{bcolors.PASS_GREEN}Text{bcolors.ENDC}")
print(f"{bcolors.WARNING_YELLOW}Text{bcolors.ENDC}")
print(f"{bcolors.FAIL_RED}Text{bcolors.ENDC}")
'''

#**********DEFINE VARIABLE**********#
action = sys.argv[1]
method = sys.argv[2]
vmnumber = sys.argv[3]
divide1 = '★－:+:－:+:－:+:－:+:－:+:－:+:－:+:－:+:－:+:－:+:－★'
divide2 = '◆*．◆*．◆*．◆*．◆*．◆*．◆*．◆*．◆*．◆*．'

print(f"{bcolors.HEADER_PURPLE}"+divide1+f"{bcolors.ENDC}")
print(f"{bcolors.WARNING_YELLOW}ACTION is "+action+f"{bcolors.ENDC}")
print(f"{bcolors.WARNING_YELLOW}METHOD is "+method+f"{bcolors.ENDC}")
print(f"{bcolors.WARNING_YELLOW}VMNUMBER is "+vmnumber+f"{bcolors.ENDC}")

if action == 'Connect':
    security = sys.argv[4]
    ssid = sys.argv[5]
    password = sys.argv[6]
    print(f"{bcolors.WARNING_YELLOW}SECURITY is "+security+f"{bcolors.ENDC}")
    print(f"{bcolors.WARNING_YELLOW}SSID is "+ssid+f"{bcolors.ENDC}")
    if security != 'none':
        print(f"{bcolors.WARNING_YELLOW}PASSWORD is "+password+f"{bcolors.ENDC}")

print(f"{bcolors.HEADER_PURPLE}"+divide1+f"{bcolors.ENDC}")

#**********CHECK VMNUMBER FORMAT**********#
#Continuity number
reg1 ='(^[0-9]{1,2})+(-[0-9]{1,2})$'
#Discontinuity number
reg2 ='(^[0-9]{1,2})+(,[0-9]{1,2})*$' 
 
#Check number format and value
if method == "Continuity":
    if re.match(reg1,vmnumber):
        match = re.match(reg1,vmnumber)
        print(f"{bcolors.PASS_GREEN}VM number format is correct{bcolors.ENDC}")
        vmn = vmnumber.split("-")
        vmn1 = int(vmn[0])
        vmn2 = int(vmn[1])
        if vmn1 < 1 or vmn1 > 90:
            print(f"{bcolors.FAIL_RED}First number must between 1 and 90{bcolors.ENDC}")
            sys.exit(999)
        if vmn2 < 1 or vmn2 > 90:
            print(f"{bcolors.FAIL_RED}Second number must between 1 and 90{bcolors.ENDC}") 
            sys.exit(999)
    else:
        print(f"{bcolors.FAIL_RED}VM number format is wrong{bcolors.ENDC}")
        sys.exit(999)
else:
    if re.match(reg2,vmnumber):
        match = re.match(reg2,vmnumber)
        print(f"{bcolors.PASS_GREEN}VM number format is correct{bcolors.ENDC}")
        vmn = vmnumber.split(",")
        a = 0
        b = len(vmn)
        while a < b:
            vmn3 = int(vmn[a])
            if vmn3 < 1 or vmn3 > 90:
                print(f"{bcolors.FAIL_RED}VM number must between 1 and 90{bcolors.ENDC}") 
                sys.exit(999)
            a += 1
    else:
        print(f"{bcolors.FAIL_RED}VM number format is wrong{bcolors.ENDC}")
        sys.exit(999)
   
#**********DEFINE FUNCTION**********#         
def CONNECT(num):
    os.system('C:\\PSTools\\psexec \\\\10.0.200.'+str(num)+' -u WIN7VM-1 -p sassd -nobanner -c -f "D:\\Dropbox\\WiFi Test Automation\\VM WiFi Connect Disconnect Manual\\Server call VM to copy file.bat" > NUL 2>&1')
    time.sleep(3)
    os.system('C:\\PSTools\\psexec \\\\10.0.200.'+str(num)+' -u WIN7VM-1 -p sassd -i -d "C:\\Python36\\python.exe" "C:/Auto_Test_Folder/VM WiFi Connect Disconnect Manual.py" %s %i %s %s'"> NUL 2>&1"% (action,num,ssid,security))

def DISCONNECT(num):
    os.system('C:\\PSTools\\psexec \\\\10.0.200.'+str(num)+' -u WIN7VM-1 -p sassd -d netsh wlan disconnect interface="WLAN" > NUL 2>&1')

#**********PRE ACTION**********#
#Server_A copy python file to wilf_python folder
copyfile('D:\Dropbox\WiFi Test Automation\VM WiFi Connect Disconnect Manual\VM WiFi Connect Disconnect Manual.py','C:\wifi_python\VM WiFi Connect Disconnect Manual.py')

#Clear Server_A report file in wifi_report folder
file = glob.glob("C:\\wifi_report\\report*.txt")
for i in range (0,len(file)):
    os.remove(file[i])

#**********MAIN**********#        
if method == "Continuity":
    vmn = vmnumber.split("-")
    if action == 'Connect':
        for i in range(int(vmn[0]), int(vmn[1])+1):   
            CONNECT(i)
    else:
        print(f"{bcolors.HEADER_PURPLE}"+divide2+f"{bcolors.ENDC}")
        for i in range(int(vmn[0]), int(vmn[1])+1):
            print(f"{bcolors.PASS_GREEN}VM "+str(i)+" disconnect to wifi"f"{bcolors.ENDC}")
            DISCONNECT(i)
        print(f"{bcolors.HEADER_PURPLE}"+divide2+f"{bcolors.ENDC}")
else:
    vmn = vmnumber.split(",")
    i = 0
    b = len(vmn)
    if action == 'Connect':
        while i < b:
            CONNECT(int(vmn[i]))
            i += 1
    else:
        print(f"{bcolors.HEADER_PURPLE}"+divide2+f"{bcolors.ENDC}")
        while i < b:
            print(f"{bcolors.PASS_GREEN}VM "+str(vmn[i])+" disconnect to wifi"f"{bcolors.ENDC}")
            DISCONNECT(int(vmn[i]))
            i += 1
        print(f"{bcolors.HEADER_PURPLE}"+divide2+f"{bcolors.ENDC}")

#**********POST ACTION**********#
#Check if the VM connected to wifi successfully

if action == 'Connect':
    time.sleep(30)

if action == 'Connect':
    print(f"{bcolors.HEADER_PURPLE}"+divide2+f"{bcolors.ENDC}")
    if method == "Continuity":
        vmn = vmnumber.split("-")
        for i in range(int(vmn[0]), int(vmn[1])+1):   
            vm_report = 'C:\\wifi_report\\report'+str(i)+'.txt'
            if os.path.exists(vm_report):
                print(f"{bcolors.FAIL_RED}VM "+str(i)+" connect to wifi failed"f"{bcolors.ENDC}")
            else:
                print(f"{bcolors.PASS_GREEN}VM "+str(i)+" connect to wifi successfully"f"{bcolors.ENDC}")       
    else:
        vmn = vmnumber.split(",")
        i = 0
        b = len(vmn)
        while i < b:
            vm_report = 'C:\\wifi_report\\report'+str(vmn[i])+'.txt'
            if os.path.exists(vm_report):
                print(f"{bcolors.FAIL_RED}VM "+str(vmn[i])+" connect to wifi failed"f"{bcolors.ENDC}")
            else:
                print(f"{bcolors.PASS_GREEN}VM "+str(vmn[i])+" connect to wifi successfully"f"{bcolors.ENDC}")
            i += 1 
    print(f"{bcolors.HEADER_PURPLE}"+divide2+f"{bcolors.ENDC}") 

#If any report file exists, jenkins will display failed        
exist = glob.glob("C:\\wifi_report\\report*.txt")
length = len(exist)
if length == 0:
    sys.exit(0)
elif length > 0:
    sys.exit(999)
    
