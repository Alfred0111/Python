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
#3.1.11/Create Profile/Delete Profile Test
#Verify the user can delete the existed profile.
#1.Create New Profile, then Delete, it shall disappeared from Profile list.
#2.After delete the existing profile which are using by DAP, The DAP shall disppeared on Monitor Page.
#3.DAP shall be Discovered by any profile.

#----------MAIN----------#
class DNC_AUTOTEST(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe', chrome_options=options)
        self.url = "https://localhost:30001"
        self.account = "admin"
        self.password = "Aa123456"
        self.devip = "172.17.193.249"

    def tearDown(self):
        self.driver.quit()

    def test(self):
        driver = self.driver
        driver.get(self.url)
        driver.maximize_window()
        
        #-----------------------------------Login to DNC-----------------------------------# 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inputEmail")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inputPass")))
        driver.find_element_by_id("inputEmail").send_keys(self.account)
        driver.find_element_by_id("inputPass").send_keys(self.password)
        driver.find_element_by_xpath("//button[contains(.,'Login')]").click()
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Dashboard')]")))
            print(f"{bcolors.INFO_WARNING_YELLOW}Login to DNC - OK{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Unable to login to DNC, stop the test{bcolors.ENDC}")
            driver.save_screenshot('./Login failed.png')   
            sys.exit(1)  
        
        #-----------------------------------Go to Configuration-Create Profile-Add Network page-----------------------------------# 
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Create Profile')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Add Network')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Add Network')]")))

        #-----------------------------------Input site and network name-----------------------------------#
        #Input site name
        driver.find_element_by_name("newsite").send_keys("Test_Site")

        #Input network name
        driver.find_element_by_name("netName").clear()
        driver.find_element_by_name("netName").send_keys("Test_Network")
        
        #Click next button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Next')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Network Configurations')]")))

        #-----------------------------------Configure network-----------------------------------#
        #Select device type as AP
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(.,'Access Point')]"))).click()
        
        #Input admin password
        driver.find_element_by_xpath("//input[@type='password']").send_keys("Aa123456")

        #Input ssid password
        driver.find_element_by_xpath("(//input[@type='password'])[2]").send_keys("12345678")

        #Go to mesh network page
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Mesh Network Settings')]")))
        
        #Click next button
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Discover Network Settings')]")))
        
        #-----------------------------------Scan and manage device-----------------------------------#
        #Click layer2
        driver.find_element_by_xpath("//p").click()

        #Input DAP2's IP
        driver.find_element_by_name("fromIP").send_keys(self.devip)
        driver.find_element_by_name("toIp").send_keys(self.devip)
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Discover Device')]")))

        #Click discover button
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "discover_button"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Scan Finished')]")))
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div"))).click()
        driver.find_element_by_xpath("//password-input/div/input").clear()
        driver.find_element_by_xpath("//password-input/div/input").send_keys("errorpwd")
        
        #Import to DAP2
        driver.find_element_by_xpath("//button[contains(.,'Import')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Import Device(s)')]")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Yes')]"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//p[contains(.,'Task successfully sent!')]")))
        driver.find_element_by_xpath("//button[contains(.,'Apply & Exit')]").click()
        time.sleep(5)

        #Test1 - Create New Profile, then Delete, it shall disappeared from Profile list.
        #Delete test profile
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[7]/div/div[9]/div/button[2]"))).click()
        
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Delete Network')]")))
            time.sleep(3)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(.,'Yes')]"))).click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Test_Network')]")))
            time.sleep(3)
            print(f"{bcolors.PASS_GREEN}Test1 - Create New Profile, then Delete, it shall disappeared from Profile list. -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test1 - Create New Profile, then Delete, it shall disappeared from Profile list. -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test1.png')
            code = 1


        if 'code' in locals():
            sys.exit(code)
          


if __name__ == "__main__":
    unittest.main()