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
#18.1.1/Command Line Test/Disable Console Test
#Verify the user can not log-in console if disable this feature.
#1. Create profile then set Console as Disable status.
#2. Use Putty to log-in console via SSH/ Telnet, system shall reject.

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
        
        #--------------------------------------Disalbe profile1 console settings--------------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Profile Settings')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Auto_Site1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Device Settings')]"))).click()
        #Disable console settings
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//p"))).click()
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


        #Test1 - Log-in console via SSH, system shall reject       
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=self.device_ip, port=22, username='admin', password='Aa123456')
            print(f"{bcolors.FAIL_RED}Test1 - Log-in console via SSH, system shall reject -- FAIL{bcolors.ENDC}")
            code = 1
        except:
            print(f"{bcolors.PASS_GREEN}Test1 - Log-in console via SSH, system shall reject -- PASS{bcolors.ENDC}")
            
        
        #Test2 - Log-in console via Telnet, system shall reject       
        try:
            tn=Telnet(self.device_ip)
            print(f"{bcolors.FAIL_RED}Test2 - Log-in console via Telnet, system shall reject -- FAIL{bcolors.ENDC}")
            code = 1
        except:
            print(f"{bcolors.PASS_GREEN}Test2 - Log-in console via Telnet, system shall reject -- PASS{bcolors.ENDC}")

        #--------------------------------------Enable profile1 console settings--------------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Device Settings')]"))).click()
        #Enable console settings
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//p"))).click()
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

        #Test3 - Reopen console settings and log-in console via Telnet, system shall accept     
        try:
            tn=Telnet(self.device_ip)
            print(f"{bcolors.PASS_GREEN}Test3 - Reopen console settings and log-in console via Telnet, system shall accept -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test3 - Reopen console settings and log-in console via Telnet, system shall accept -- FAIL{bcolors.ENDC}")
            code = 1

        
        if 'code' in locals():
            sys.exit(code)


if __name__ == "__main__":
    unittest.main()