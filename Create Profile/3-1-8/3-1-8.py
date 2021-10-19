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
#3.1.8/Create Profile/Discover L3 IP Range Test
#Verify the user can create new profile then discover specified IP range for standalone DAP.
#1. Arrange the LAN environment with different IP segment as 172.17.192.x/ 172.17.193.x.
#2. Deploy the DNH-100 on 172.17.192.x. segment.
#3. Deploy the DAP on 172.17.193.x. segment.
#4. Execute the Layer3 Discovery on DNH-100, the DAP shall be discovered.

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
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Dashboard')]")))
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
        driver.find_element_by_name("newsite").send_keys("Test_Site")
        driver.find_element_by_name("netName").clear()
        driver.find_element_by_name("netName").send_keys("Test_Network")
        
        #Click next button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Next')]"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Network Configurations')]")))

        #-----------------------------------Input key and device password Aa123456-----------------------------------#
        #Select device type as AP
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(.,'Access Point')]"))).click()
        time.sleep(3)

        driver.find_element_by_xpath("//password-input[@id='password']/div/input").send_keys("12345678")
        driver.find_element_by_xpath("//input[@type='password']").send_keys("Aa123456")

        #Go to mesh network page
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Mesh Network Settings')]")))

        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Discover Network Settings')]")))
        time.sleep(3)
        
        #-----------------------------------Scan and manage device-----------------------------------#
        driver.find_element_by_xpath("//div[@id='addNetworkDialog']/form/div/div[2]/div/label/p").click()
        driver.find_element_by_xpath("//div[@id='addNetworkDialog']/form/div/div/div/label").click()        
        driver.find_element_by_name("fromIP").send_keys(self.devip)
        driver.find_element_by_name("toIp").send_keys(self.devip)
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Discover Device')]")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "discover_button"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Scan Finished')]")))

        #Test1 - Verify the user can create new profile then discover specified IP range for standalone DAP.
        try:
            #Scan device
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div")))
            print(f"{bcolors.PASS_GREEN}Test1 - Verify the user can create new profile then discover specified IP range for standalone DAP. -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test1 - Verify the user can create new profile then discover specified IP range for standalone DAP. -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test1.png')
            code = 1
        
        #-----------------------------------Delete the test profile-----------------------------------#
        driver.find_element_by_xpath("//button[contains(.,'Apply & Exit')]").click()
        #Click test profile delete button
        time.sleep(3)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[7]/div/div[9]/div/button[2]"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(.,'Yes')]"))).click()
        time.sleep(3)


        if 'code' in locals():
            sys.exit(code)
          


if __name__ == "__main__":
    unittest.main()