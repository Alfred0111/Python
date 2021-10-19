import re
import sys
import os
import glob
import time


# ANSI COLOR CODE
class Bcolors():
    PARM_YELLOW = '\033[93m'
    INFO_BLUE = '\033[34m'
    PASS_GREEN = '\033[92m'
    FAIL_RED = '\033[91m'
    ENDC = '\033[0m'


# DEFINE PARAMETER
EC = 999
vm_min = 1
vm_max = 90
chrome_exe = "\"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe\""


# REGULAR EXPRESSION CHECK
class Format_check():
    def vmnum_check(method, vmnumber):
        reg1 = '(^[0-9]{1,2})+(-[0-9]{1,2})$' # Continuity number
        reg2 = "(^[0-9]{1,2})+(,[0-9]{1,2})*$" # Discontinuity number
        if method == "Continuity" and re.match(reg1, vmnumber):
            vmn = vmnumber.split("-"); vmn1 = int(vmn[0]); vmn2 = int(vmn[1])
            if vmn1 < vm_min or vmn1 > vm_max:
                print(f"{Bcolors.FAIL_RED}First number must between 1 and 90{Bcolors.ENDC}")
                sys.exit(EC)
            elif vmn2 < vm_min or vmn2 > vm_max:
                print(f"{Bcolors.FAIL_RED}Second number must between 1 and 90{Bcolors.ENDC}")
                sys.exit(EC)
            elif vmn1 > vmn2:
                print(f"{Bcolors.FAIL_RED}The first number is greater than the second number{Bcolors.ENDC}")
                sys.exit(EC)
            else:
                print(f"{Bcolors.PASS_GREEN}VM number format and range are correct{Bcolors.ENDC}")
        elif method == "Discontinuity" and re.match(reg2, vmnumber):
            vmn = vmnumber.split(","); x = 0; y = len(vmn)
            while x < y:
                vmn3 = int(vmn[x])
                if vmn3 < 1 or vmn3 > 90:
                    print(f"{Bcolors.FAIL_RED}VM number must between 1 and 90{Bcolors.ENDC}")
                    sys.exit(EC)
                x += 1
            print(f"{Bcolors.PASS_GREEN}VM number format and range are correct{Bcolors.ENDC}")
        else:
            print(f"{Bcolors.FAIL_RED}VM number is incorrect{Bcolors.ENDC}")
            sys.exit(EC)

    def ssid_check(ssid):
        reg = "^[A-Za-z0-9@#!_-]*$"
        if re.match(reg, ssid):
            print(f"{Bcolors.PASS_GREEN}SSID format is correct{Bcolors.ENDC}")
        else:
            print(f"{Bcolors.FAIL_RED}SSID format is wrong{Bcolors.ENDC}")
            sys.exit(EC)



# WIFI CONTROL
class WiFi_control():
    def profile_clear(num):
        os.system(rf'C:\PSTools\psexec \\10.0.200.{str(num)} -u WIN7VM-1 -p sassd -d -nobanner netsh wlan delete profile name=* > NUL 2>&1')
        print(f"{Bcolors.INFO_BLUE}Clear VM {str(num)} wifi profile{Bcolors.ENDC}")

    def profile_edit_auto_pwd(security, ssid, password):
        os.system(r'cd "D:\Dropbox\WiFi Test Automation\@ascii_to_hex"')
        os.system(rf'call "D:\Dropbox\WiFi Test Automation\@ascii_to_hex\convert_{security}_personal.bat" {ssid}')
        os.system(rf'C:\SED\bin\sed.exe -i "7s/name>.*</name>{ssid}</" "C:\wifi_profile\WLAN-{security}_personal.xml"')
        os.system(rf'C:\SED\bin\sed.exe -i "22s/keyMaterial>.*</keyMaterial>{password}</" "C:\wifi_profile\WLAN-{security}_personal.xml"')
        os.system('del sed*')
        print(f"{Bcolors.INFO_BLUE}Modify wifi profile ({security}) successfully{Bcolors.ENDC}")

    def profile_edit_manual_pwd(security, ssid, password):
        os.system(r'cd "D:\Dropbox\WiFi Test Automation\@ascii_to_hex"')
        os.system(rf'call "D:\Dropbox\WiFi Test Automation\@ascii_to_hex\convert_{security}_personal_manual.bat" {ssid}')
        os.system(rf'C:\SED\bin\sed.exe -i "7s/name>.*</name>{ssid}</" "C:\wifi_profile\WLAN-{security}_personal_manual.xml"')
        os.system(rf'C:\SED\bin\sed.exe -i "24s/keyMaterial>.*</keyMaterial>{password}</" "C:\wifi_profile\WLAN-{security}_personal_manual.xml"')
        os.system('del sed*')
        print(f"{Bcolors.INFO_BLUE}Modify wifi profile ({security} manual) successfully{Bcolors.ENDC}")

    def profile_edit_auto(security, ssid):
        os.system(r'cd "D:\Dropbox\WiFi Test Automation\@ascii_to_hex"')
        os.system(rf'call "D:\Dropbox\WiFi Test Automation\@ascii_to_hex\convert_{security}.bat" {ssid}')
        os.system(rf'C:\SED\bin\sed.exe -i "7s/name>.*</name>{ssid}</" "C:\wifi_profile\WLAN-{security}.xml"')
        os.system('del sed*')
        print(f"{Bcolors.INFO_BLUE}Modify wifi profile ({security}) successfully{Bcolors.ENDC}")

    def profile_edit_manual(security, ssid):
        os.system(r'cd "D:\Dropbox\WiFi Test Automation\@ascii_to_hex"')
        os.system(rf'call "D:\Dropbox\WiFi Test Automation\@ascii_to_hex\convert_{security}_manual.bat" {ssid}')
        os.system(rf'C:\SED\bin\sed.exe -i "7s/name>.*</name>{ssid}</" "C:\wifi_profile\WLAN-{security}_manual.xml"')
        os.system('del sed*')
        print(f"{Bcolors.INFO_BLUE}Modify wifi profile ({security} manual) successfully"f"{Bcolors.ENDC}")

    def wifi_disconnect(num):
        os.system(rf'C:\PSTools\psexec \\10.0.200.{str(num)} -u WIN7VM-1 -p sassd -d netsh wlan disconnect interface="WLAN" > NUL 2>&1')


# SYSTEM CONTROL
class System():
    def connection_check(method, vmnumber): #Check if the VM connected to wifi successfully
        if method == "Continuity":
            vmn = vmnumber.split("-")
            for i in range(int(vmn[0]), int(vmn[1])+1):
                vm_report = 'C:\\wifi_report\\report'+str(i)+'.txt'
                if os.path.exists(vm_report):
                    print(f"{Bcolors.FAIL_RED}VM {str(i)} connect to wifi failed{Bcolors.ENDC}")
                else:
                    print(f"{Bcolors.INFO_BLUE}VM {str(i)} connect to wifi successfully{Bcolors.ENDC}")
        else:
            vmn = vmnumber.split(",")
            count = 0
            listlen = len(vmn)
            while count < listlen:
                vm_report = 'C:\\wifi_report\\report'+str(vmn[count])+'.txt'
                if os.path.exists(vm_report):
                    print(f"{Bcolors.FAIL_RED}VM {str(vmn[count])} connect to wifi failed{Bcolors.ENDC}")
                else:
                    print(f"{Bcolors.INFO_BLUE}VM {str(vmn[count])} connect to wifi successfully{Bcolors.ENDC}")
                count += 1

        #If any report file exists, jenkins will display failed
        exist = glob.glob("C:\\wifi_report\\report*.txt")
        length = len(exist)
        sys.exit(0) if length == 0 else sys.exit(EC)

    def server_rep_clear(): #Clear Server_A report file in wifi_report folder
        file = glob.glob("C:\\wifi_report\\report*.txt")
        for i in range (0, len(file)):
            os.remove(file[i])

    def reboot_shutdown(num, action):
        cmd = "-r" if action == "Reboot" else "-s"
        os.system(rf'C:\PSTools\psexec \\10.0.200.{str(num)} -u WIN7VM-1 -p sassd -d -nobanner shutdown {cmd} -t 10 > NUL 2>&1')
        print(f"{Bcolors.INFO_BLUE}{action} VM {str(num)}{Bcolors.ENDC}")

    def openchrome(num,url):
        os.system(rf'C:\PSTools\psexec \\10.0.200.{str(num)} -u WIN7VM-1 -p sassd -i -d {chrome_exe} "{url}" > NUL 2>&1')
        print(f"{Bcolors.INFO_BLUE}VM {str(num)} open URL {url}{Bcolors.ENDC}")

    def closechrome(num):
        os.system(rf'C:\PSTools\psexec \\10.0.200.{str(num)} -u WIN7VM-1 -p sassd -i -d taskkill /f /im chrome.exe > NUL 2>&1')
        print(f"{Bcolors.INFO_BLUE}VM {str(num)} close chrome{Bcolors.ENDC}")

    def copyfile(num, batpath):
        os.system(rf'C:\PSTools\psexec \\10.0.200.{str(num)} -u WIN7VM-1 -p sassd -nobanner -c -f "{batpath}" > NUL 2>&1')
        time.sleep(3)

    def callvm_py(num, exepath, filepath, action, ssid, security, mode):
        os.system(rf'C:\PSTools\psexec \\10.0.200.{str(num)} -u WIN7VM-1 -p sassd -i -d "{exepath}" "{filepath}" %s %i %s %s %s' "> NUL 2>&1" % (action,num,ssid,security,mode))

    def loop_start(num, action, ssid, security, mode, value):
        os.system('C:\\PSTools\\psexec \\\\10.0.200.'+str(num)+' -u WIN7VM-1 -p sassd -i -d "C:\\Python36\\python.exe" "C:/Auto_Test_Folder/VM WiFi Connect Loop.py" %i %s %s %s %s %s'" > NUL 2>&1"% (num,action,ssid,security,mode,value))

    def loop_stop(num):
        os.system(rf'C:\PSTools\psexec \\10.0.200.{str(num)} -u WIN7VM-1 -p sassd -nobanner taskkill /f /im python.exe > NUL 2>&1')

    def fh_loop_start(num, action, mode, value, url):
        os.system('C:\\PSTools\\psexec \\\\10.0.200.'+str(num)+' -u WIN7VM-1 -p sassd -i -d "C:\\Python36\\python.exe" "C:/Auto_Test_Folder/VM FTP HTTP Loop.py" %s %s %s %s'" > NUL 2>&1" % (action, mode, value, url))

    def fh_loop_stop(num, action):
        os.system('C:\\PSTools\\psexec \\\\10.0.200.'+str(num) +' -u WIN7VM-1 -p sassd -d -i "C:\\Python36\\python.exe" "C:/Auto_Test_Folder/VM FTP HTTP Loop.py" %s'" > NUL 2>&1" % (action))
