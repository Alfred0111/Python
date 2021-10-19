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
#16.1.3/Feature Test-SSID And Security/Broadcast SSID Test
#Verify the Broadcast SSID configuration push to DAP
#1. Enable "Broadcast SSID", then SSID shall be scannable, and embedded in Beacon frames.
#2. Disable "Broadcast SSID", then SSIDshall not scanned, and keep "blank" in Beacon frames.

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


        #---------------------------------Disable "Broadcast SSID"---------------------------------#
        #Click primary edit button
        time.sleep(5)
        driver.find_element_by_xpath("//span/a").click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div[2]/div/div/div/div/span/span[2]/span"))).click()
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

        #---------------------------------Test1 - Disable "Broadcast SSID", then SSIDshall not scanned---------------------------------#
        #Scan SSID
        os.system('netsh wlan show network > "D:\\Dropbox\\DNC Automation\\Command Line Test\\18-1-3\\scan.txt"') 
        text = open(r"D:\Dropbox\DNC Automation\Command Line Test\18-1-3\scan.txt",'r') 
        scanssid = text.read()
        text.close()
        time.sleep(10)

        #Delete scan ssid file
        connect_file = r"D:\Dropbox\DNC Automation\Command Line Test\18-1-3\scan.txt"
        if os.path.exists(connect_file):
            os.remove(connect_file)
        
        print(f"{bcolors.HEADER_PURPLE}Scan SSID.....{bcolors.ENDC}")
        print(f"{bcolors.INFO_WARNING_YELLOW}{scanssid}{bcolors.ENDC}")

        if 'Auto_SSID1' not in scanssid:
            print(f"{bcolors.PASS_GREEN}Test1 - Disable Broadcast SSID, then SSIDshall not scanned -- PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL_RED}Test1 - Disable Broadcast SSID, then SSIDshall not scanned -- FAIL{bcolors.ENDC}")
            code = 1

        #---------------------------------Go to Profile1 edit page---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'SSID')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "ssid")))

        #---------------------------------Enable "Broadcast SSID"---------------------------------#
        #Click primary edit button
        time.sleep(5)
        driver.find_element_by_xpath("//span/a").click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div[2]/div/div/div/div/span/span[2]/span"))).click()
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

        #---------------------------------Test2 - Enable "Broadcast SSID", then SSID shall be scannable---------------------------------#
        #Scan SSID
        os.system('netsh wlan show network > "D:\\Dropbox\\DNC Automation\\Command Line Test\\18-1-3\\scan.txt"') 
        text = open(r"D:\Dropbox\DNC Automation\Command Line Test\18-1-3\scan.txt",'r') 
        scanssid = text.read()
        text.close()
        time.sleep(10)

        #Delete scan ssid file
        connect_file = r"D:\Dropbox\DNC Automation\Command Line Test\18-1-3\scan.txt"
        if os.path.exists(connect_file):
            os.remove(connect_file)
        
        print(f"{bcolors.HEADER_PURPLE}Scan SSID.....{bcolors.ENDC}")
        print(f"{bcolors.INFO_WARNING_YELLOW}{scanssid}{bcolors.ENDC}")

        if 'Auto_SSID1' in scanssid:
            print(f"{bcolors.PASS_GREEN}Test2 - Enable Broadcast SSID, then SSID shall be scannable -- PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL_RED}Test2 - Enable Broadcast SSID, then SSID shall be scannable -- FAIL{bcolors.ENDC}")
            code = 1
        
        
        if 'code' in locals():
            sys.exit(code)


if __name__ == "__main__":
    unittest.main()
      