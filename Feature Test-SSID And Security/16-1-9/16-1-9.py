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

#**********DEFINE ANSI COLOR CODE**********#
class bcolors():
    HEADER_PURPLE = '\033[0;35m'
    PASS_GREEN = '\033[92m'
    INFO_WARNING_YELLOW = '\033[93m'
    FAIL_RED = '\033[91m'
    ENDC = '\033[0m'

#----------CASE DESCRIPTION----------#
#16.1.9/Feature Test-SSID And Security/WPA3 - Encryption Type
#Verify the WPA3 option push to DAP properly 
#1. If choose "WPA2 or WPA3", the encryption type menu only provide "AES". --- (Not implemented)
#2. The Mobile Phone (support WPA3) shall connected, and browse Internet smoothly.
#3. The Beacon shall embed the WAPA3 information. --- (Not implemented)

#----------MAIN----------#
class DNC_AUTOTEST(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe', chrome_options=options)
        self.url = "https://172.17.192.201:30001"
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

        #---------------------------------Change mode to (WPA-Personal,WPA3 only)---------------------------------#
        #Click primary edit button
        time.sleep(5)
        driver.find_element_by_xpath("//span/a").click()
        time.sleep(5)
        
        #Change security to WPA-Personal
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[3]/div/div/div/div/div/span/span[2]/span"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[6]/span/span"))).click()
        
        #Pagedown
        pagedown = driver.find_element_by_tag_name('html')
        pagedown.click()
        pagedown.send_keys(Keys.PAGE_DOWN)

        #Change WPA mode to WPA3 only
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div/div[2]/div/div/div/div/div/span/span[2]/span"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[6]/span/span"))).click()

        #Set Passphrase as 12345678
        driver.find_element_by_xpath("//password-input/div/input").clear()
        driver.find_element_by_xpath("//password-input/div/input").send_keys("12345678")
        
        #Pagedown
        pagedown = driver.find_element_by_tag_name('html')
        pagedown.click()
        pagedown.send_keys(Keys.PAGE_DOWN)
 
        driver.find_element_by_xpath("//button[contains(.,'Save')]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Confirm')]")))
        driver.find_element_by_xpath("//button[contains(.,'Yes')]").click()
        
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

        #---------------------------------Test1 - Wi-Fi client shall associate to Auto_SSID1 using WPA3 wifi profile---------------------------------#
        #Delete wifi profile
        os.system('netsh wlan delete profile name=*') 
        time.sleep(2)
        #Import wifi profile
        os.system(r'netsh wlan add profile filename="D:\Dropbox\DNC Automation\Feature Test-SSID And Security\16-1-9\16-1-9-Auto_SSID1_WAP3.xml"') 
        time.sleep(3)
        #Connect to wifi
        os.system('netsh wlan connect name=16-1-9-Auto_SSID1_WAP3 ssid=Auto_SSID1 interface=WLAN')  
        time.sleep(30)

        #Get connection status
        os.system('netsh wlan show interface > "D:\\Dropbox\\DNC Automation\\Feature Test-SSID And Security\\16-1-9\\connect.txt"') 
        text = open(r"D:\Dropbox\DNC Automation\Feature Test-SSID And Security\16-1-9\connect.txt",'r') 
        connectres = text.read()
        text.close()
        time.sleep(10)

        #Delete wifi profile
        os.system('netsh wlan delete profile name=*') 

        #Delete connection status file
        connect_file = r"D:\Dropbox\DNC Automation\Feature Test-SSID And Security\16-1-9\connect.txt"
        if os.path.exists(connect_file):
            os.remove(connect_file)
        
        print(f"{bcolors.HEADER_PURPLE}Wifi connection status.....{bcolors.ENDC}")
        print(f"{bcolors.INFO_WARNING_YELLOW}{connectres}{bcolors.ENDC}")

        if '連線' in connectres and 'Auto_SSID1' in connectres and 'WPA3-個人' in connectres and '16-1-9-Auto_SSID1_WAP3' in connectres and 'CCMP' in connectres:
            print(f"{bcolors.PASS_GREEN}Test1 - Wi-Fi client shall associate to Auto_SSID1 using AES wifi profile -- PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL_RED}Test1 - Wi-Fi client shall associate to Auto_SSID1 using AES wifi profile -- FAIL{bcolors.ENDC}")
            code = 1
       

        #---------------------------------Go to Profile1 edit page---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'SSID')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "ssid")))

        #---------------------------------Recover setting---------------------------------#
        #Click primary edit button
        time.sleep(5)
        driver.find_element_by_xpath("//span/a").click()
        time.sleep(5)

        #Change security to open
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[3]/div/div/div/div/div/span/span[2]/span"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[3]/span/span"))).click()
       
        #Pagedown
        pagedown = driver.find_element_by_tag_name('html')
        pagedown.click()
        pagedown.send_keys(Keys.PAGE_DOWN)
 
        driver.find_element_by_xpath("//button[contains(.,'Save')]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Confirm')]")))
        driver.find_element_by_xpath("//button[contains(.,'Yes')]").click()
        
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
      