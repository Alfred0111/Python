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

#**********DEFINE ANSI COLOR CODE**********#
class bcolors():
    HEADER_PURPLE = '\033[0;35m'
    PASS_GREEN = '\033[92m'
    INFO_WARNING_YELLOW = '\033[93m'
    FAIL_RED = '\033[91m'
    ENDC = '\033[0m'

#----------CASE DESCRIPTION----------#
#16.8.5/Feature Test - Device Setting/Time Zone Test
#Verify the Time Zone configuration push to DAP
#1. Set Time Zone to 1st country, then apply to DAP. And check the system time on DAP UI.
#2. Set Time Zone to 2nd country, then apply to DAP. And check the system time on DAP UI.
#3. Set Time Zone to 3rd country, then apply to DAP. And check the system time on DAP UI.
#4. The System Time & Time Zone shall changed after apply new profile setting.

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
        
        #---------------------------------Go to profile1 device setting page---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Profile Settings')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Auto_Site1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Access Point')]"))).click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Device Settings')]"))).click()
        
        #---------------------------------Change time zone to (GMT-12:00) International Date Line West---------------------------------#
        time.sleep(5)
        pagedown = driver.find_element_by_tag_name('html')
        pagedown.click()
        pagedown.send_keys(Keys.PAGE_DOWN)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div/div/div/span/span[2]/span"))).click()
        time.sleep(3)
        driver.find_element_by_xpath("//div[2]/div/div/div/input").send_keys("(GMT-12:00) International Date Line West")
        driver.find_element_by_xpath("//div[2]/div/div/div/input").send_keys(Keys.ENTER)

        time.sleep(3)
        pagedown = driver.find_element_by_tag_name('html')
        pagedown.click()
        pagedown.send_keys(Keys.PAGE_DOWN)
              
        #Save the setting
        driver.find_element_by_xpath("//button[contains(.,'Save')]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Device configuration successfully saved')]")))
        
        #--------------------------------------Push config to device--------------------------------------#
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Apply')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration has uploaded successfully')]")))
        #Wait push success
        WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        #Wait DAP1 apply the setting
        time.sleep(180)

        #--------------------------------------Test1 - Set Time Zone to 1st country, and check the time zone on DAP--------------------------------------#
        #Telnet to DAP1 and check country is correct
        tn=Telnet(self.device_ip)
        tn.read_until(b"login:")
        tn.write("admin".encode('ascii') + b"\r\n")
        tn.read_until(b"Password:")
        tn.write("Aa123456".encode('ascii') + b"\r\n")
        tn.write("get tzonelist".encode('ascii') + b"\r\n")
        time.sleep(3)
        res = tn.read_very_eager().decode('ascii')
        tn.write("exit".encode('ascii') + b"\r\n")
        print(f"{bcolors.HEADER_PURPLE}********************{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}{res}{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}********************{bcolors.ENDC}")
      
        #Test1 - Verify the user can set to different Country & Time Zone on Wizard. Then Time Zone shall set into DAP apply profile into DAP
        if "SNTP/NTP Time Zone: 1" in res:
            print(f"{bcolors.PASS_GREEN}Test1 - Set Time Zone to 1st country, and check the time zone on DAP -- PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL_RED}Test1 - Set Time Zone to 1st country, and check the time zone on DAP -- FAIL{bcolors.ENDC}")
            code = 1
                              
        #---------------------------------Change time zone to (GMT-11:00) Midway Island---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Device Settings')]"))).click()
        time.sleep(5)
        pagedown = driver.find_element_by_tag_name('html')
        pagedown.click()
        pagedown.send_keys(Keys.PAGE_DOWN)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div/div/div/span/span[2]/span"))).click()
        time.sleep(3)
        driver.find_element_by_xpath("//div[2]/div/div/div/input").send_keys("(GMT-11:00) Midway Island")
        driver.find_element_by_xpath("//div[2]/div/div/div/input").send_keys(Keys.ENTER)

        time.sleep(3)
        pagedown = driver.find_element_by_tag_name('html')
        pagedown.click()
        pagedown.send_keys(Keys.PAGE_DOWN)
              
        #Save the setting
        driver.find_element_by_xpath("//button[contains(.,'Save')]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Device configuration successfully saved')]")))
        
        #--------------------------------------Push config to device--------------------------------------#
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Apply')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration has uploaded successfully')]")))
        #Wait push success
        WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        #Wait DAP1 apply the setting
        time.sleep(180)

        #--------------------------------------Test2 - Set Time Zone to 2st country, and check the time zone on DAP--------------------------------------#
        #Telnet to DAP1 and check country is correct
        tn=Telnet(self.device_ip)
        tn.read_until(b"login:")
        tn.write("admin".encode('ascii') + b"\r\n")
        tn.read_until(b"Password:")
        tn.write("Aa123456".encode('ascii') + b"\r\n")
        tn.write("get tzonelist".encode('ascii') + b"\r\n")
        time.sleep(3)
        res = tn.read_very_eager().decode('ascii')
        tn.write("exit".encode('ascii') + b"\r\n")
        print(f"{bcolors.HEADER_PURPLE}********************{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}{res}{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}********************{bcolors.ENDC}")
      
        #Test1 - Verify the user can set to different Country & Time Zone on Wizard. Then Time Zone shall set into DAP apply profile into DAP
        if "SNTP/NTP Time Zone: 2" in res:
            print(f"{bcolors.PASS_GREEN}Test2 - Set Time Zone to 2st country, and check the time zone on DAP -- PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL_RED}Test2 - Set Time Zone to 2st country, and check the time zone on DAP -- FAIL{bcolors.ENDC}")
            code = 1

        #---------------------------------Change time zone to (GMT-10:00) Hawaii---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Device Settings')]"))).click()
        time.sleep(5)
        pagedown = driver.find_element_by_tag_name('html')
        pagedown.click()
        pagedown.send_keys(Keys.PAGE_DOWN)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div/div/div/span/span[2]/span"))).click()
        time.sleep(3)
        driver.find_element_by_xpath("//div[2]/div/div/div/input").send_keys("(GMT-10:00) Hawaii")
        driver.find_element_by_xpath("//div[2]/div/div/div/input").send_keys(Keys.ENTER)

        time.sleep(3)
        pagedown = driver.find_element_by_tag_name('html')
        pagedown.click()
        pagedown.send_keys(Keys.PAGE_DOWN)
              
        #Save the setting
        driver.find_element_by_xpath("//button[contains(.,'Save')]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Device configuration successfully saved')]")))
        
        #--------------------------------------Push config to device--------------------------------------#
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Apply')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration has uploaded successfully')]")))
        #Wait push success
        WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        #Wait DAP1 apply the setting
        time.sleep(180)

        #--------------------------------------Test3 - Set Time Zone to 3st country, and check the time zone on DAP--------------------------------------#
        #Telnet to DAP1 and check country is correct
        tn=Telnet(self.device_ip)
        tn.read_until(b"login:")
        tn.write("admin".encode('ascii') + b"\r\n")
        tn.read_until(b"Password:")
        tn.write("Aa123456".encode('ascii') + b"\r\n")
        tn.write("get tzonelist".encode('ascii') + b"\r\n")
        time.sleep(3)
        res = tn.read_very_eager().decode('ascii')
        tn.write("exit".encode('ascii') + b"\r\n")
        print(f"{bcolors.HEADER_PURPLE}********************{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}{res}{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}********************{bcolors.ENDC}")
      
        #Test1 - Verify the user can set to different Country & Time Zone on Wizard. Then Time Zone shall set into DAP apply profile into DAP
        if "SNTP/NTP Time Zone: 3" in res:
            print(f"{bcolors.PASS_GREEN}Test3 - Set Time Zone to 3st country, and check the time zone on DAP -- PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL_RED}Test3 - Set Time Zone to 3st country, and check the time zone on DAP -- FAIL{bcolors.ENDC}")
            code = 1

        #---------------------------------Recover time zone to (GMT+08:00) Taipei---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Device Settings')]"))).click()
        time.sleep(5)
        pagedown = driver.find_element_by_tag_name('html')
        pagedown.click()
        pagedown.send_keys(Keys.PAGE_DOWN)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div/div/div/span/span[2]/span"))).click()
        time.sleep(3)
        driver.find_element_by_xpath("//div[2]/div/div/div/input").send_keys("(GMT+08:00) Taipei")
        driver.find_element_by_xpath("//div[2]/div/div/div/input").send_keys(Keys.ENTER)

        time.sleep(3)
        pagedown = driver.find_element_by_tag_name('html')
        pagedown.click()
        pagedown.send_keys(Keys.PAGE_DOWN)
              
        #Save the setting
        driver.find_element_by_xpath("//button[contains(.,'Save')]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Device configuration successfully saved')]")))

        #--------------------------------------Push config to device--------------------------------------#
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network1')]"))).click()
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
