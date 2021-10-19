#----------MODULE IMPORT----------#
import unittest
import time
import sys
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
#3.1.2/Create Profile/Set Primary SSID Test
#Verify the user can create new profile then set SSID, and the valid string length shall limited within 0~32 characters.
#1. Input the SSID as 33 characters or more, system shall reject.
#2. Choose sychronize to 5G, the 2G/ 5G SSID/ Security shall be the same.

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
        
        #---------------------------------Go to Configuration-Create Profile-Add Network page---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Create Profile')]"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Add Network')]"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Add Network')]")))

        #---------------------------------------------Input site and network name---------------------------------------------#
        driver.find_element_by_name("newsite").send_keys("Test_Site")
        driver.find_element_by_name("netName").clear()
        driver.find_element_by_name("netName").send_keys("Test_Network")
        #Click next button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Next')]"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Network Configurations')]")))
        
        #---------------------------------------------Input security key and device key---------------------------------------------#
        #Select type as AP
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//p"))).click()
        time.sleep(3)

        #Input key
        driver.find_element_by_xpath("(//input[@type='password'])[2]").send_keys("12345678")
        driver.find_element_by_xpath("//input[@type='password']").send_keys("Aa123456")

        #Test1 - Check SSID name character limit and next button status
        driver.find_element_by_id("ssidName").clear()
        driver.find_element_by_id("ssidName").send_keys("A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789")
        time.sleep(3)
        ssid = driver.find_element_by_name("ssidName")
        try:
            self.assertEqual("A123456789A123456789A123456789A1", ssid.get_attribute('value'))
            self.assertTrue(driver.find_element_by_xpath("//button[contains(.,'Next')]").is_enabled())
            print(f"{bcolors.PASS_GREEN}Test1 - Check SSID name character limit and next button status -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test1 - Check SSID name character limit and next button status -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test1.png')
            code = 1
        

        if 'code' in locals():
            sys.exit(code)


if __name__ == "__main__":
    unittest.main()
      