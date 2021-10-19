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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

#**********DEFINE ANSI COLOR CODE**********#
class bcolors():
    HEADER_PURPLE = '\033[0;35m'
    PASS_GREEN = '\033[92m'
    INFO_WARNING_YELLOW = '\033[93m'
    FAIL_RED = '\033[91m'
    ENDC = '\033[0m'

#----------CASE DESCRIPTION----------#
#16.8.1/Feature Test - Device Setting/Device Authentication Test
#Verify the Device Authentication configuration push to DAP
#1. Change UserName/ Password to 11111111/22222222 on profile, then upload to DAP.
#2. Log-In DAP UI with admin/admin, it shall be reject.
#3. Log-In DAP UI with 11111111/22222222, it shall be accept.

#----------MAIN----------#
class DNC_AUTOTEST(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe', chrome_options=options)
        self.url = "https://localhost:30001"
        self.dapurl = "http://172.17.192.230"
        self.account = "admin"
        self.password = "Aa123456"

    def tearDown(self):
        self.driver.quit()

    def test1(self):
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
    
        #---------------------------------Go to "Create Profile" profile1 edit page---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Create Profile')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[9]/div/button"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Edit Network')]")))   

        #Go to "Network Configurations" page
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Network Configurations')]")))   

        #Open AP setting paage
        driver.find_element_by_xpath("//h3[contains(.,'Access Point')]").click()
        
        #---------------------------------Change admin account/password---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "username")))
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("alfred")
        driver.find_element_by_xpath("//password-input/div/input").clear()
        driver.find_element_by_xpath("//password-input/div/input").send_keys("123456Aa")
       
        #Save the setting
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Discover Network Settings')]")))
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Discover Device')]")))
        driver.find_element_by_xpath("//button[contains(.,'Apply & Exit')]").click()
        
        #--------------------------------------Push config to device--------------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Profile Settings')]"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Auto_Site1')]"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Apply')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration has uploaded successfully')]")))
        #Wait push success
        WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        #Wait DAP1 apply the setting
        time.sleep(180)


    def test2_oldaccountlogin(self):
        driver = self.driver
        driver.get(self.dapurl)
        driver.maximize_window()

        #------------------------------------------------Log-In DAP UI with admin/Aa123456, it shall be reject------------------------------------------------# 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "LOGIN_USER")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "LOGIN_PASSWD")))
        driver.find_element_by_name("LOGIN_USER").send_keys("admin")
        driver.find_element_by_name("LOGIN_PASSWD").send_keys("Aa123456")
        driver.find_element_by_name("login").click()
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'DAP-2680')]")))
            print(f"{bcolors.FAIL_RED}Test1 - Log-In DAP UI with admin/Aa123456, it shall be reject -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test1.png')   
            code = 1
        except:
            print(f"{bcolors.PASS_GREEN}Test1 - Log-In DAP UI with admin/Aa123456, it shall be reject -- PASS{bcolors.ENDC}") 

        if 'code' in locals():
            sys.exit(code) 

 
    def test3_newaccountlogin(self):
        driver = self.driver
        driver.get(self.dapurl)
        driver.maximize_window()

        #------------------------------------------------Log-In DAP UI with alfred/123456Aa, it shall be accept------------------------------------------------# 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "LOGIN_USER")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "LOGIN_PASSWD")))
        driver.find_element_by_name("LOGIN_USER").send_keys("alfred")
        driver.find_element_by_name("LOGIN_PASSWD").send_keys("123456Aa")
        driver.find_element_by_name("login").click()
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'DAP-2680')]")))
            print(f"{bcolors.PASS_GREEN}Test2 - Log-In DAP UI with alfred/123456Aa, it shall be accept -- PASS{bcolors.ENDC}") 
        except:
            print(f"{bcolors.FAIL_RED}Test2 - Log-In DAP UI with alfred/123456Aa, it shall be accept -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test2.png')   
            code = 1

        if 'code' in locals():
            sys.exit(code) 


    def test4(self):
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
    
        #---------------------------------Go to "Create Profile" profile1 edit page---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Create Profile')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[9]/div/button"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Edit Network')]")))   

        #Go to "Network Configurations" page
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Network Configurations')]")))   

        #Open AP setting paage
        driver.find_element_by_xpath("//h3[contains(.,'Access Point')]").click()

        #---------------------------------Recover admin account/password---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "username")))
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("admin")
        driver.find_element_by_xpath("//password-input/div/input").clear()
        driver.find_element_by_xpath("//password-input/div/input").send_keys("Aa123456")
       
        #Save the setting
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Discover Network Settings')]")))
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Discover Device')]")))
        driver.find_element_by_xpath("//button[contains(.,'Apply & Exit')]").click()
        
        #--------------------------------------Push config to device--------------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Profile Settings')]"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Auto_Site1')]"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Apply')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration has uploaded successfully')]")))
        #Wait push success
        WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        #Wait DAP1 apply the setting
        time.sleep(180)



if __name__ == "__main__":
    unittest.main()

      