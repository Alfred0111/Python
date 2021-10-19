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
#16.1.5/Feature Test-SSID And Security/Enhance Open
#Verify the Enhance Open configuration push to DAP properly.
#Verify the Enhance Open configuration push to DAP properly.

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
   
        #---------------------------------Go to Profile1 edit page---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Profile Settings')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Auto_Site1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Access Point')]"))).click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'SSID')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "ssid")))

        #---------------------------------Change mode to (Enhance Open)---------------------------------#
        #Click primary edit button
        time.sleep(5)
        driver.find_element_by_xpath("//span/a").click()
        time.sleep(5)
        
        #Change security to Enhance Open
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[3]/div/div/div/div/div/span/span[2]/span"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[4]/span/span"))).click()
 
        driver.find_element_by_xpath("//button[contains(.,'Save')]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Confirm')]")))
        driver.find_element_by_xpath("//button[contains(.,'Yes')]").click()
        
        #--------------------------------------Push config to device--------------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Apply')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration has uploaded successfully')]")))
        #Wait push success
        WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        #Wait DAP1 apply the setting
        time.sleep(180)

    def test2_disable_nuclias_setting(self):
        driver = self.driver
        driver.get(self.dapurl)
        driver.maximize_window()

        #------------------------------------------------Login to DAP------------------------------------------------# 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "LOGIN_USER")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "LOGIN_PASSWD")))
        driver.find_element_by_name("LOGIN_USER").send_keys(self.account)
        driver.find_element_by_name("LOGIN_PASSWD").send_keys(self.password)
        driver.find_element_by_name("login").click()
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//b[contains(.,'DAP-2680   ')]")))
            print(f"{bcolors.INFO_WARNING_YELLOW}Login to DAP - OK{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Unable to login to DAP, stop the test{bcolors.ENDC}")
            driver.save_screenshot('./DAP Login failed.png')   
            sys.exit(1)  

        #---------------------------------Disable Nuclias Connect Setting---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "banner_tool"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Administration Settings"))).click()
       
        #SWitch frame
        driver.switch_to.frame(driver.find_element_by_name("ifrMain"))

        #Check Nuclias Connect Setting
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='swctrl_setting']"))).click()
 
        #Change to disable
        Select(driver.find_element_by_id("sw_enable")).select_by_visible_text("Disable")
        
        #Click save button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='save_a_lable']/img"))).click()
        time.sleep(5)

        #SWitch frame
        driver.switch_to.default_content()

    def test3_checkvalue(self):
        driver = self.driver
        driver.get(self.dapurl)
        driver.maximize_window()

        #------------------------------------------------Login to DAP------------------------------------------------# 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "LOGIN_USER")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "LOGIN_PASSWD")))
        driver.find_element_by_name("LOGIN_USER").send_keys(self.account)
        driver.find_element_by_name("LOGIN_PASSWD").send_keys(self.password)
        driver.find_element_by_name("login").click()
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//b[contains(.,'DAP-2680   ')]")))
            print(f"{bcolors.INFO_WARNING_YELLOW}Login to DAP - OK{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Unable to login to DAP, stop the test{bcolors.ENDC}")
            driver.save_screenshot('./DAP Login failed.png')   
            sys.exit(1)  

        #---------------------------------Test1 - Verify the Enhance Open configuration push to DAP properly---------------------------------#
        #---------------------------------Check primary ssid encryption---------------------------------#
        #Go to multi-ssid page and check primary ssid encryption
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Advanced Settings')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,' Multi-SSID')]"))).click()
        time.sleep(5)
        
        #SWitch frame
        driver.switch_to.frame(driver.find_element_by_name("ifrMain"))

        #Get primary ssid Encryption
        enc_type = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div/table/tbody/tr/td[4]"))).text
        print(f"{bcolors.HEADER_PURPLE}Primary SSID encryption type is {enc_type}{bcolors.ENDC}")
        
        #SWitch frame
        driver.switch_to.default_content()
  
        try:
            self.assertEqual("Enhanced Open", enc_type)
            print(f"{bcolors.PASS_GREEN}Test1 - Verify the Enhance Open configuration push to DAP properly -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test1 - Verify the Enhance Open configuration push to DAP properly -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test1.png')
            code = 1


        if 'code' in locals():
            sys.exit(code) 
        

    def test4_enable_nuclias_setting(self):
        driver = self.driver
        driver.get(self.dapurl)
        driver.maximize_window()

        #------------------------------------------------Login to DAP------------------------------------------------# 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "LOGIN_USER")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "LOGIN_PASSWD")))
        driver.find_element_by_name("LOGIN_USER").send_keys(self.account)
        driver.find_element_by_name("LOGIN_PASSWD").send_keys(self.password)
        driver.find_element_by_name("login").click()
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//b[contains(.,'DAP-2680   ')]")))
            print(f"{bcolors.INFO_WARNING_YELLOW}Login to DAP - OK{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Unable to login to DAP, stop the test{bcolors.ENDC}")
            driver.save_screenshot('./DAP Login failed.png')   
            sys.exit(1)  

        #---------------------------------Enable Nuclias Connect Setting---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "banner_tool"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Administration Settings"))).click()
       
        #SWitch frame
        driver.switch_to.frame(driver.find_element_by_name("ifrMain"))

        #Check Nuclias Connect Setting
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='swctrl_setting']"))).click()
 
        #Change to disable
        Select(driver.find_element_by_id("sw_enable")).select_by_visible_text("Enable")
        
        #Click save button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='save_a_lable']/img"))).click()
        time.sleep(10)

        #SWitch frame
        driver.switch_to.default_content()    

    def test5(self):
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
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'SSID')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "ssid")))

        #---------------------------------Change mode to (Open System)---------------------------------#
        #Click primary edit button
        time.sleep(5)
        driver.find_element_by_xpath("//span/a").click()
        time.sleep(5)
        
        #Change security to Open System
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[3]/div/div/div/div/div/span/span[2]/span"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[3]/span/span"))).click()
 
        driver.find_element_by_xpath("//button[contains(.,'Save')]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Confirm')]")))
        driver.find_element_by_xpath("//button[contains(.,'Yes')]").click()
        
        #--------------------------------------Push config to device--------------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Apply')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration has uploaded successfully')]")))
        #Wait push success
        WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        #Wait DAP1 apply the setting
        time.sleep(180)
  


if __name__ == "__main__":
    unittest.main()
      