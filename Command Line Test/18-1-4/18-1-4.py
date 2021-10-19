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
#18.1.4/Command Line Test/Authentication Fail Test (Server & DAP)
#Verify the system reject the log-in if input wrong User Name/ Password.
#1. Create profile then set Console as Telnet.
#2. Use Putty to log-in console via Telnet (Port 23), and input wrong User ID/ Password, system shall reject.
#3. Create profile then set Console as SSH.
#4. Use Putty to log-in console via SSH (Port 22), and input wrong User ID/ Password, system shall reject.

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
        driver = self.driver
        driver.get(self.url)
        driver.maximize_window()
        
        #------------------------------------------------Telnet to DAP1 using incorrect user id------------------------------------------------#   
        tn=Telnet(self.device_ip)
        tn.read_until(b"login:")
        tn.write("alfred".encode('ascii') + b"\r\n")
        time.sleep(10)
        res1 = tn.read_very_eager().decode('ascii')
        print(f"{bcolors.HEADER_PURPLE}********************{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}{res1}{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}********************{bcolors.ENDC}")
        tn.close()

        #Test1 - Log-in console via Telnet (Port 23), and input wrong User ID, system shall reject
        if "Login incorrect" in res1:
            print(f"{bcolors.PASS_GREEN}Test1 - Log-in console via Telnet (Port 23), and input wrong User ID, system shall reject -- PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL_RED}Test1 - Log-in console via Telnet (Port 23), and input wrong User ID, system shall reject -- FAIL{bcolors.ENDC}")
            code = 1

        #------------------------------------------------Telnet to DAP1 using incorrect password------------------------------------------------#   
        tn=Telnet(self.device_ip)
        tn.read_until(b"login:")
        tn.write("admin".encode('ascii') + b"\r\n")
        tn.read_until(b"Password:")
        tn.write("errorpwd".encode('ascii') + b"\r\n")
        time.sleep(10)
        res2 = tn.read_very_eager().decode('ascii')
        print(f"{bcolors.HEADER_PURPLE}********************{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}{res2}{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}********************{bcolors.ENDC}")
        tn.close()

        #Test2 - Log-in console via Telnet (Port 23), and input wrong password, system shall reject
        if "Login incorrect" in res2:
            print(f"{bcolors.PASS_GREEN}Test2 - Log-in console via Telnet (Port 23), and input wrong password, system shall reject -- PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL_RED}Test2 - Log-in console via Telnet (Port 23), and input wrong password, system shall reject -- FAIL{bcolors.ENDC}")
            code = 1

        #------------------------------------------------Login to DNC------------------------------------------------# 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inputEmail")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inputPass")))
        driver.find_element_by_id("inputEmail").send_keys(self.account)
        driver.find_element_by_id("inputPass").send_keys(self.password)
        driver.find_element_by_xpath("//button[contains(.,'Login')]").click()
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Dashboard')]")))
            print(f"{bcolors.INFO_WARNING_YELLOW}Login to DNC - OK{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Unable to login to DNC, stop the test{bcolors.ENDC}")
            driver.save_screenshot('./Login failed.png')   
            sys.exit(1)  
        
        #--------------------------------------Change console protocol to ssh--------------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Profile Settings')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Auto_Site1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Device Settings')]"))).click()
        #Change console protocol to ssh
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[2]/p"))).click()
        driver.find_element_by_xpath("//button[contains(.,'Save')]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Device configuration successfully saved')]")))

        #--------------------------------------Push config to device--------------------------------------#
        driver.find_element_by_xpath("//a[contains(.,'Auto_Network1')]").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Apply')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration has uploaded successfully')]")))
        WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Success')]")))
        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Success')]")))
        #------------------------------------------------Wait DAP aplly the setting------------------------------------------------#
        time.sleep(60)

        #------------------------------------------------SSH to DAP1 using incorrect user id------------------------------------------------#
        #Test3 - Log-in console via SSH (Port 22), and input wrong User ID, system shall reject       
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.close()
        try:
            client.connect(hostname=self.device_ip, port=22, username='erroruser', password='Aa123456')
            print(f"{bcolors.FAIL_RED}Test3 - Log-in console via SSH (Port 22), and input wrong User ID, system shall reject -- FAIL{bcolors.ENDC}")
            code = 1
        except:
            print(f"{bcolors.PASS_GREEN}Test3 - Log-in console via SSH (Port 22), and input wrong User ID, system shall reject -- PASS{bcolors.ENDC}")
        
        #------------------------------------------------SSH to DAP1 using incorrect password-------------------------------------------------#
        #Test4 - Log-in console via SSH (Port 22), and input wrong User password, system shall reject       
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.close()
        try:
            client.connect(hostname=self.device_ip, port=22, username='admin', password='errorpwd')
            print(f"{bcolors.FAIL_RED}Test4 - Log-in console via SSH (Port 22), and input wrong User password, system shall reject -- FAIL{bcolors.ENDC}")
            code = 1
        except:
            print(f"{bcolors.PASS_GREEN}Test4 - Log-in console via SSH (Port 22), and input wrong User password, system shall reject -- PASS{bcolors.ENDC}")


        #--------------------------------------Change console protocol to telnet--------------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Device Settings')]"))).click()
        #Enable console settings
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(.,'Telnet')]"))).click()
        driver.find_element_by_xpath("//button[contains(.,'Save')]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Device configuration successfully saved')]")))

        #--------------------------------------Push config to device--------------------------------------#
        driver.find_element_by_xpath("//a[contains(.,'Auto_Network1')]").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Apply')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration has uploaded successfully')]")))
        WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Success')]")))
        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Success')]")))
        #------------------------------------------------Wait DAP aplly the setting------------------------------------------------#
        time.sleep(60)

        if 'code' in locals():
            sys.exit(code)


if __name__ == "__main__":
    unittest.main()