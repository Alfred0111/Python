#----------MODULE IMPORT----------#
import unittest
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telnetlib import Telnet
import paramiko

#**********DEFINE ANSI COLOR CODE**********#
class bcolors():
    HEADER_PURPLE = '\033[0;35m'
    PASS_GREEN = '\033[92m'
    INFO_WARNING_YELLOW = '\033[93m'
    FAIL_RED = '\033[91m'
    ENDC = '\033[0m'
'''
print(f"{bcolors.HEADER_PURPLE}Text{bcolors.ENDC}")
print(f"{bcolors.PASS_GREEN}Text{bcolors.ENDC}")
print(f"{bcolors.INFO_WARNING_YELLOW}Text{bcolors.ENDC}")
print(f"{bcolors.FAIL_RED}Text{bcolors.ENDC}")
'''

#----------CASE DESCRIPTION----------#
#18.1.3/Command Line Test/Telnet Test (Server & DAP)
#Verify the user can log-in console if select Telnet feature.
#1. Create profile then set Console as Telnet.
#2. Use Putty to log-in console via Telnet (Port 23), system shall accept.
#3. Use Putty to log-in console via SSH (Port 22), system shall reject.

#----------MAIN----------#
class DNC_AUTOTEST(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe', chrome_options=options)
        self.url = "https://localhost:30001"
        self.account = "admin"
        self.password = "Aa123456"
        self.device_ip = "172.17.192.230"

    def tearDown(self):
        self.driver.quit()

    def test(self):

        #Test1 - Use Putty to log-in console via Telnet (Port 23), system shall accept       
        try:
            tn=Telnet(self.device_ip)
            print(f"{bcolors.PASS_GREEN}Test1 - Use Putty to log-in console via Telnet (Port 23), system shall accept -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test1 - Use Putty to log-in console via Telnet (Port 23), system shall accept -- FAIL{bcolors.ENDC}")
            code = 1

        #Test2 - Use Putty to log-in console via SSH (Port 22), system shall reject       
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=self.device_ip, port=22, username='admin', password='Aa123456')
            print(f"{bcolors.FAIL_RED}Test2 - Use Putty to log-in console via SSH (Port 22), system shall reject -- FAIL{bcolors.ENDC}")
            code = 1
        except:
            print(f"{bcolors.PASS_GREEN}Test2 - Use Putty to log-in console via SSH (Port 22), system shall reject -- PASS{bcolors.ENDC}")

        if 'code' in locals():
            sys.exit(code)


if __name__ == "__main__":
    unittest.main()