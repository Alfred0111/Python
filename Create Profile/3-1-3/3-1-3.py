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
#12/Create Profile/Set Security Mode Test
#Verify the user can create new profile then set Security Mode, and the valid string length shall limited within 8~63 characters.
#1. Select Open System, Password column shall disappeared.
#2. Select WPA-Auto Personal, then 
#2-1. Input the SSID Password as 1~7 characters, system shall reject.
#2-2. Input the SSID Password as 64 characters or more, system shall reject.
#3. Choose sychronize to 5G, the 2G/ 5G SSID/ Security shall be the same. --- (Not implemented)

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
        
        #---------------------------------Go to Configuration-Create Profile-Add Network page--------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Create Profile')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Add Network')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Add Network')]")))

        #Input site and network name
        driver.find_element_by_name("newsite").send_keys("Test_Site")
        driver.find_element_by_name("netName").clear()
        driver.find_element_by_name("netName").send_keys("Test_Network")
        
        #Click next button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Next')]"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Network Configurations')]")))
        
        #Test1 - Select open system, password column shall disappeared
        #Select device type as AP
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(.,'Access Point')]"))).click()

        #page down
        pagedown = driver.find_element_by_tag_name('html')
        pagedown.click()
        pagedown.send_keys(Keys.PAGE_DOWN)
        time.sleep(5)
        
        #Select security as open system
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[4]/div/div/div/div/span/span[2]/span"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[3]/span/span"))).click()
        
        try:
            WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.XPATH, "//div[5]/div/label")))
            print(f"{bcolors.PASS_GREEN}Test1 - Select open system, password column shall disappeared -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test1 - Select open system, password column shall disappeared -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test1.png')
            code = 1

        #Change security mode to WPA-Personal
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[4]/div/div/div/div/span/span[2]/span"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[4]/span/span"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//input[@type='password'])[2]")))
           
        #Test2 - Input the SSID Password as 1~7 characters, system shall reject
        num = 1
        key = "1"
        for i in range(1, 7):
            num += 1
            key += str(num)
            driver.find_element_by_xpath("(//input[@type='password'])[2]").clear()
            driver.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(key)
            try:
                #Check GUI pop up warning message
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'8-63 in ASCII or 64 in Hex.')]")))
                print(f"{bcolors.PASS_GREEN}Test2 - Input the SSID Password as 1~7 characters, system shall reject(key is {key}) -- PASS{bcolors.ENDC}")
            except:
                print(f"{bcolors.FAIL_RED}Test2 - Input the SSID Password as 1~7 characters, system shall reject(key is {key}) -- FAIL{bcolors.ENDC}")
                driver.save_screenshot('./Test2.png')
                code = 1

        #Test3 - Check key character limit is 64
        driver.find_element_by_xpath("(//input[@type='password'])[2]").clear()
        driver.find_element_by_xpath("(//input[@type='password'])[2]").send_keys("A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789")
        key_len = driver.find_element_by_xpath("(//input[@type='password'])[2]")
        try:
            self.assertEqual("A123456789A123456789A123456789A123456789A123456789A123456789A123", key_len.get_attribute('value'))
            WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'8-63 in ASCII or 64 in Hex.')]")))
            print(f"{bcolors.PASS_GREEN}Test3 - Check key character limit is 64 -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test3 - Check key character limit is 64 -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test3.png')
            code = 1

        if 'code' in locals():
            sys.exit(code)
          


if __name__ == "__main__":
    unittest.main()