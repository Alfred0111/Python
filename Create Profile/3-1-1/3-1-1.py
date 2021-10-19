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
'''
print(f"{bcolors.HEADER_PURPLE}Text{bcolors.ENDC}")
print(f"{bcolors.PASS_GREEN}Text{bcolors.ENDC}")
print(f"{bcolors.INFO_WARNING_YELLOW}Text{bcolors.ENDC}")
print(f"{bcolors.FAIL_RED}Text{bcolors.ENDC}")
'''

#----------CASE DESCRIPTION----------#
#3.1.1/Create Profile/Add Network Test
#Verify the user can create new profile then set Site Name & Network Name, and the valid string length shall limited within 1~32 characters.
#1. Input the Site Name/ Network Name  as 1~32 characters, system shall accept.
#2. Input the Site Name/ Network Name as 0 or exceed 33 characters or more, system shall reject.

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
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(.,'Site')]")))
        
        #Test1 - When site name is empty, next button cannot be clicked
        try:
            self.assertFalse(driver.find_element_by_xpath("//button[contains(.,'Next')]").is_enabled())
            print(f"{bcolors.PASS_GREEN}Test1 - When site name is empty, next button cannot be clicked -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test1 - When site name is empty, next button cannot be clicked -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test1.png')
            code = 1

        #Test2 - Check site name character limit and next button status
        driver.find_element_by_name("newsite").send_keys("A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789")
        site_name = driver.find_element_by_name("newsite")
        try:
            self.assertEqual("A123456789A123456789A123456789A1", site_name.get_attribute('value'))
            self.assertTrue(driver.find_element_by_xpath("//button[contains(.,'Next')]").is_enabled())
            print(f"{bcolors.PASS_GREEN}Test2 - Check site name character limit and next button status -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test2 - Check site name character limit and next button status -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test2.png')
            code = 1
        
        #Test3 - Clear network name and check next button cannot be clicked
        driver.find_element_by_name("netName").clear()
        try:
            self.assertFalse(driver.find_element_by_xpath("//button[contains(.,'Next')]").is_enabled())
            print(f"{bcolors.PASS_GREEN}Test3 - Clear network name and check next button cannot be clicked -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test3 - Clear network name and check next button cannot be clicked -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test3.png')
            code = 1

        #Test4 - Check network name character limit and next button status
        driver.find_element_by_name("netName").send_keys("A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789")
        net_name = driver.find_element_by_name("netName")
        try:
            self.assertEqual("A123456789A123456789A123456789A1", net_name.get_attribute('value'))
            self.assertTrue(driver.find_element_by_xpath("//button[contains(.,'Next')]").is_enabled())
            print(f"{bcolors.PASS_GREEN}Test4 - Check network name character limit and next button status -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test4 - Check network name character limit and next button status -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test4.png')
            code = 1
        
        if 'code' in locals():
            sys.exit(code)


if __name__ == "__main__":
    unittest.main()
      