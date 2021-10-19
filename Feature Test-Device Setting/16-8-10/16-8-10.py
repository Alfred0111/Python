#----------MODULE IMPORT----------#
import unittest
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telnetlib import Telnet

#**********DEFINE ANSI COLOR CODE**********#
class bcolors():
    HEADER_PURPLE = '\033[0;35m'
    PASS_GREEN = '\033[92m'
    INFO_WARNING_YELLOW = '\033[93m'
    FAIL_RED = '\033[91m'
    ENDC = '\033[0m'

#----------CASE DESCRIPTION----------#
#16.8.10/Feature Test - Device Setting/Telnet Test (DAP Only)
#Verify the user can login DAP kernal with Telnet connection.
#1. Create profile, enable Telnet Connection, Timeout=5 minutes, then push to DAP.
#2. After DAP enter On Line status, open the Putty and login to DAP IP address with Telnet connection.
#3. Input the username/ password of DAP, it shall login successfully.
#4. The Telnet connection of DAP shall dropped automatically once idle for over 5 minutes.
#5. Change TimeOut= Never, the connection shall keep alive forever.

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
        
        #---------------------------------Go to Profile1 edit page---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Profile Settings')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Auto_Site1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Access Point')]"))).click()
        time.sleep(5)
        #Go to device setting page
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Device Settings')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(.,'Console Settings')]")))

        #---------------------------------Change telnet idle time to 5min---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[2]/span"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[6]/span/span"))).click()

        #Save the setting
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Device configuration successfully saved')]")))
     
        #--------------------------------------Push config to device--------------------------------------#
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Apply')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration has uploaded successfully')]")))
        #Wait push success
        WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        #Wait DAP1 apply the setting
        time.sleep(180)

        #----------------------Test1 - The Telnet connection of DAP shall dropped automatically once idle for over 5 minutes----------------------#
        #Telnet to DAP1 and wait 5 min
        tn=Telnet(self.device_ip)
        tn.read_until(b"login:")
        tn.write("admin".encode('ascii') + b"\r\n")
        tn.read_until(b"Password:")
        tn.write("Aa123456".encode('ascii') + b"\r\n")
        #Wait for telnet session timeout(5 min)
        time.sleep(360)
        tn.write("get tzonelist".encode('ascii') + b"\r\n")
        time.sleep(10)
        
        #Test1 - The Telnet connection of DAP shall dropped automatically once idle for over 5 minutes
        try:
            res = tn.read_very_eager().decode('ascii')
            print(f"{bcolors.FAIL_RED}Test1 - The Telnet connection of DAP shall dropped automatically once idle for over 5 minutes -- FAIL{bcolors.ENDC}")    
            code = 1
        except:
            print(f"{bcolors.PASS_GREEN}Test1 - The Telnet connection of DAP shall dropped automatically once idle for over 5 minutes -- PASS{bcolors.ENDC}")
            
        #---------------------------------Go to device setting page---------------------------------#
        #Go to device setting page
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Device Settings')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(.,'Console Settings')]")))

        #---------------------------------Change telnet idle time to never---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[3]/div/div/div/div/span/span[2]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[3]/span/span"))).click()

        #Save the setting
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Device configuration successfully saved')]")))
     
        #--------------------------------------Push config to device--------------------------------------#
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Apply')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration has uploaded successfully')]")))
        #Wait push success
        WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        #Wait DAP1 apply the setting
        time.sleep(180)

        #----------------------Test2 - Change TimeOut= Never, the connection shall keep alive forever----------------------#
        #Telnet to DAP1 and wait 5 min
        tn=Telnet(self.device_ip)
        tn.read_until(b"login:")
        tn.write("admin".encode('ascii') + b"\r\n")
        tn.read_until(b"Password:")
        tn.write("Aa123456".encode('ascii') + b"\r\n")
        #Wait for telnet session timeout(5 min)
        time.sleep(360)
        tn.write("get tzonelist".encode('ascii') + b"\r\n")
        time.sleep(10)
        
        #Test2 - Change TimeOut= Never, the connection shall keep alive forever
        try:
            res = tn.read_very_eager().decode('ascii')
            print(f"{bcolors.PASS_GREEN}Test2 - Change TimeOut= Never, the connection shall keep alive forever -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test2 - Change TimeOut= Never, the connection shall keep alive forever -- FAIL{bcolors.ENDC}")    
            code = 1
        
        #---------------------------------Go to device setting page---------------------------------#
        #Go to device setting page
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Device Settings')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(.,'Console Settings')]")))

        #---------------------------------Recover telnet idle time to 3min---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[2]/span"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[5]/span/span"))).click()

        #Save the setting
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Device configuration successfully saved')]")))
     
        #--------------------------------------Push config to device--------------------------------------#
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Apply')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration has uploaded successfully')]")))
        #Wait push success
        WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        #Wait DAP1 apply the setting
        time.sleep(180)
           
        
        if 'code' in locals():
            sys.exit(code)





if __name__ == "__main__":
    unittest.main()
