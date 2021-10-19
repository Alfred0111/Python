#----------MODULE IMPORT----------#
import unittest
import time
import sys
import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#**********DEFINE ANSI COLOR CODE**********#
class bcolors():
    HEADER_PURPLE = '\033[0;35m'
    PASS_GREEN = '\033[92m'
    INFO_WARNING_YELLOW = '\033[93m'
    FAIL_RED = '\033[91m'
    ENDC = '\033[0m'

#----------CASE DESCRIPTION----------#
#16.1.2/Feature Test-SSID And Security/Guest SSID Test
#Verify the Guest SSID configuration push to DAP
#1. Create 1st~7th Guest SSID as valid string length (0~32 characters), and different security mode as Open/ WPA-PSK/ WPA2-PSK.
#2. Wi-Fi clients shall associate to these 7 Guest SSIDs.
#3. Create 8th Guest SSID, system shall reject.
#4. SSID can not contain unicode and special symbol " ' ` & \

#----------MAIN----------#
class DNC_AUTOTEST(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe', chrome_options=options)
        self.url = "https://localhost:30001"
        self.account = "admin"
        self.password = "Aa123456"

    def tearDown(self):
        self.driver.quit()

    def test(self):
                        
        #---------------------------------Test1 - Wi-Fi client shall associate to DNC_SSID1_Guest1---------------------------------#
        #Delete wifi profile
        os.system('netsh wlan delete profile name=*') 
        time.sleep(2)
        #Import wifi profile
        os.system(r'netsh wlan add profile filename="D:\Dropbox\DNC Automation\Feature Test-SSID And Security\16-1-2\16-1-2-DNC_SSID1_Guest1.xml"') 
        time.sleep(3)
        #Connect to wifi
        os.system('netsh wlan connect name=16-1-2-DNC_SSID1_Guest1 ssid=DNC_SSID1_Guest1 interface=WLAN')  
        time.sleep(30)

        #Get connection status
        os.system('netsh wlan show interface > "D:\\Dropbox\\DNC Automation\\Feature Test-SSID And Security\\16-1-2\\connect.txt"') 
        text = open(r"D:\Dropbox\DNC Automation\Feature Test-SSID And Security\16-1-2\connect.txt",'r') 
        connectres = text.read()
        text.close()
        time.sleep(10)

        #Delete wifi profile
        os.system('netsh wlan delete profile name=*') 

        #Delete connection status file
        connect_file = r"D:\Dropbox\DNC Automation\Feature Test-SSID And Security\16-1-2\connect.txt"
        if os.path.exists(connect_file):
            os.remove(connect_file)
        
        print(f"{bcolors.HEADER_PURPLE}Wifi connection status.....{bcolors.ENDC}")
        print(f"{bcolors.INFO_WARNING_YELLOW}{connectres}{bcolors.ENDC}")

        if '連線' in connectres and 'DNC_SSID1_Guest1' in connectres and '開啟' in connectres and '16-1-2-DNC_SSID1_Guest1' in connectres:
            print(f"{bcolors.PASS_GREEN}Test1 - Wi-Fi client shall associate to DNC_SSID1_Guest1 -- PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL_RED}Test1 - Wi-Fi client shall associate to DNC_SSID1_Guest1 -- FAIL{bcolors.ENDC}")
            code = 1

        #---------------------------------Test2 - Wi-Fi client shall associate to DNC_SSID1_Guest2---------------------------------#
        #Delete wifi profile
        os.system('netsh wlan delete profile name=*') 
        time.sleep(2)
        #Import wifi profile
        os.system(r'netsh wlan add profile filename="D:\Dropbox\DNC Automation\Feature Test-SSID And Security\16-1-2\16-1-2-DNC_SSID1_Guest2.xml"') 
        time.sleep(3)
        #Connect to wifi
        os.system('netsh wlan connect name=16-1-2-DNC_SSID1_Guest2 ssid=DNC_SSID1_Guest2 interface=WLAN')  
        time.sleep(30)

        #Get connection status
        os.system('netsh wlan show interface > "D:\\Dropbox\\DNC Automation\\Feature Test-SSID And Security\\16-1-2\\connect.txt"') 
        text = open(r"D:\Dropbox\DNC Automation\Feature Test-SSID And Security\16-1-2\connect.txt",'r') 
        connectres = text.read()
        text.close()
        time.sleep(10)

        #Delete wifi profile
        os.system('netsh wlan delete profile name=*') 

        #Delete connection status file
        connect_file = r"D:\Dropbox\DNC Automation\Feature Test-SSID And Security\16-1-2\connect.txt"
        if os.path.exists(connect_file):
            os.remove(connect_file)
        
        print(f"{bcolors.HEADER_PURPLE}Wifi connection status.....{bcolors.ENDC}")
        print(f"{bcolors.INFO_WARNING_YELLOW}{connectres}{bcolors.ENDC}")

        if '連線' in connectres and 'DNC_SSID1_Guest2' in connectres and 'WPA2-Personal' in connectres and '16-1-2-DNC_SSID1_Guest2' in connectres:
            print(f"{bcolors.PASS_GREEN}Test2 - Wi-Fi client shall associate to DNC_SSID1_Guest2 -- PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL_RED}Test2 - Wi-Fi client shall associate to DNC_SSID1_Guest2 -- FAIL{bcolors.ENDC}")
            code = 1

        #---------------------------------Test3 - Wi-Fi client shall associate to DNC_SSID1_Guest3---------------------------------#
        #Delete wifi profile
        os.system('netsh wlan delete profile name=*') 
        time.sleep(2)
        #Import wifi profile
        os.system(r'netsh wlan add profile filename="D:\Dropbox\DNC Automation\Feature Test-SSID And Security\16-1-2\16-1-2-DNC_SSID1_Guest3.xml"') 
        time.sleep(3)
        #Connect to wifi
        os.system('netsh wlan connect name=16-1-2-DNC_SSID1_Guest3 ssid=DNC_SSID1_Guest3 interface=WLAN')  
        time.sleep(30)

        #Get connection status
        os.system('netsh wlan show interface > "D:\\Dropbox\\DNC Automation\\Feature Test-SSID And Security\\16-1-2\\connect.txt"') 
        text = open(r"D:\Dropbox\DNC Automation\Feature Test-SSID And Security\16-1-2\connect.txt",'r') 
        connectres = text.read()
        text.close()
        time.sleep(10)

        #Delete wifi profile
        os.system('netsh wlan delete profile name=*') 

        #Delete connection status file
        connect_file = r"D:\Dropbox\DNC Automation\Feature Test-SSID And Security\16-1-2\connect.txt"
        if os.path.exists(connect_file):
            os.remove(connect_file)
        
        print(f"{bcolors.HEADER_PURPLE}Wifi connection status.....{bcolors.ENDC}")
        print(f"{bcolors.INFO_WARNING_YELLOW}{connectres}{bcolors.ENDC}")

        if '連線' in connectres and 'DNC_SSID1_Guest3' in connectres and 'WPA2-Personal' in connectres and '16-1-2-DNC_SSID1_Guest3' in connectres:
            print(f"{bcolors.PASS_GREEN}Test3 - Wi-Fi client shall associate to DNC_SSID1_Guest3 -- PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL_RED}Test3 - Wi-Fi client shall associate to DNC_SSID1_Guest3 -- FAIL{bcolors.ENDC}")
            code = 1

       
        if 'code' in locals():
            sys.exit(code)


if __name__ == "__main__":
    unittest.main()
      