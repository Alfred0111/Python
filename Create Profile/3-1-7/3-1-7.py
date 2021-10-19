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
#3.1.7/Create Profile/Discovery AP Test
#Verify the user can discover the Standalone DAP, or discover Managed/ Unmanaged DAP.
#1. Create A, B profile.
#2. Set DAP_1 = A Profile, DAP_2 = B Profile, DAP_3 = Standalone
#3. Discover AP on A profile, it shall discover DAP_3 (Standalone), DAP_2 (Managed).
#4. Discover AP on B profile, it shall discover DAP_3 (Standalone), DAP_1 (Managed).

#----------MAIN----------#
class DNC_AUTOTEST(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe', chrome_options=options)
        self.url = "https://localhost:30001"
        self.account = "admin"
        self.password = "Aa123456"
        self.dev1ip = "172.17.192.230"
        self.dev2ip = "172.17.193.249"

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
        
        #-----------------------------------Go to Configuration-Create Profile page-----------------------------------# 
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Create Profile')]"))).click()
     
        #------------------------------Test1 - Use profile2 to discover DAP1 and check status is correct------------------------------# 
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div[8]/div/button"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Discover Network Settings')]")))
        #Click layer3
        driver.find_element_by_xpath("//div[@id='addNetworkDialog']/form/div/div[2]/div/label/p").click()
        #Click layer2
        driver.find_element_by_xpath("//div[@id='addNetworkDialog']/form/div/div/div/label").click()        
        driver.find_element_by_name("fromIP").send_keys(self.dev1ip)
        driver.find_element_by_name("toIp").send_keys(self.dev1ip)
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Discover Device')]")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "discover_button"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Scan Finished')]")))
        driver.find_element_by_xpath("//a[contains(.,'Managed')]").click()
        
        #Get DAP1 state
        time.sleep(5)
        state = driver.find_element_by_xpath("//div[3]/div[2]/div/div/div/div/div").text
        ipaddr = driver.find_element_by_xpath("//div[3]/div[2]/div/div/div/div[2]/div").text
        macaddr = driver.find_element_by_xpath("//div[2]/div/div/div/div[3]/div").text
        print(f"{bcolors.HEADER_PURPLE}{state}{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}{ipaddr}{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}{macaddr}{bcolors.ENDC}")
        
        #Test1 - Use profile2 to discover DAP1 and check status is correct
        try:
            self.assertEqual("Managed", state)
            self.assertEqual("172.17.192.230", ipaddr)
            self.assertEqual("18:0f:76:32:e9:f0", macaddr)
            print(f"{bcolors.PASS_GREEN}Test1 - Use profile2 to discover DAP1 and check status is correct -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test1 - Use profile2 to discover DAP1 and check status is correct -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test1.png')
            code = 1
        
        #Click cancel to exit page
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Cancel')]"))).click()

        #------------------------------Test2 - Use profile2 to discover DAP2 and check status is correct------------------------------# 
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div[8]/div/button"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Discover Network Settings')]")))
        #Click layer3
        driver.find_element_by_xpath("//div[@id='addNetworkDialog']/form/div/div[2]/div/label/p").click()
        #Click layer2
        driver.find_element_by_xpath("//div[@id='addNetworkDialog']/form/div/div/div/label").click()        
        driver.find_element_by_name("fromIP").send_keys(self.dev2ip)
        driver.find_element_by_name("toIp").send_keys(self.dev2ip)
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Discover Device')]")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "discover_button"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Scan Finished')]")))
        
        #Get DAP2 state
        time.sleep(5)
        state = driver.find_element_by_xpath("//div[3]/div[2]/div/div/div/div/div").text
        ipaddr = driver.find_element_by_xpath("//div[3]/div[2]/div/div/div/div[2]/div").text
        macaddr = driver.find_element_by_xpath("//div[2]/div/div/div/div[3]/div").text
        print(f"{bcolors.HEADER_PURPLE}{state}{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}{ipaddr}{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}{macaddr}{bcolors.ENDC}")
        
        #Test2 - Use profile2 to discover DAP2 and check status is correct
        try:
            self.assertEqual("Standalone", state)
            self.assertEqual("172.17.193.249", ipaddr)
            self.assertEqual("18:0f:76:32:ea:30", macaddr)
            print(f"{bcolors.PASS_GREEN}Test2 - Use profile2 to discover DAP2 and check status is correct -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test2 - Use profile2 to discover DAP2 and check status is correct -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test2.png')
            code = 1
        
        #Click cancel to exit page
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Cancel')]"))).click()

        #------------------------------Test3 - Use profile3 to discover DAP1 and check status is correct------------------------------# 
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[3]/div/div[8]/div/button"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Discover Network Settings')]")))
        driver.find_element_by_name("fromIP").clear()
        driver.find_element_by_name("toIp").clear()
        driver.find_element_by_name("fromIP").send_keys(self.dev1ip)
        driver.find_element_by_name("toIp").send_keys(self.dev1ip)
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Discover Device')]")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "discover_button"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Scan Finished')]")))
        driver.find_element_by_xpath("//a[contains(.,'Managed')]").click()
        
        #Get DAP1 state
        time.sleep(5)
        state = driver.find_element_by_xpath("//div[3]/div[2]/div/div/div/div/div").text
        ipaddr = driver.find_element_by_xpath("//div[3]/div[2]/div/div/div/div[2]/div").text
        macaddr = driver.find_element_by_xpath("//div[2]/div/div/div/div[3]/div").text
        print(f"{bcolors.HEADER_PURPLE}{state}{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}{ipaddr}{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}{macaddr}{bcolors.ENDC}")
        
        #Test3 - Use profile3 to discover DAP1 and check status is correct
        try:
            self.assertEqual("Managed", state)
            self.assertEqual("172.17.192.230", ipaddr)
            self.assertEqual("18:0f:76:32:e9:f0", macaddr)
            print(f"{bcolors.PASS_GREEN}Test3 - Use profile3 to discover DAP1 and check status is correct -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test3 - Use profile3 to discover DAP1 and check status is correct -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test3.png')
            code = 1
        
        #Click cancel to exit page
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Cancel')]"))).click()

        #------------------------------Test4 - Use profile3 to discover DAP2 and check status is correct------------------------------# 
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[3]/div/div[8]/div/button"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Discover Network Settings')]")))
        driver.find_element_by_name("fromIP").clear()
        driver.find_element_by_name("toIp").clear()
        driver.find_element_by_name("fromIP").send_keys(self.dev2ip)
        driver.find_element_by_name("toIp").send_keys(self.dev2ip)
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Discover Device')]")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "discover_button"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Scan Finished')]")))
        
        #Get DAP2 state
        time.sleep(5)
        state = driver.find_element_by_xpath("//div[3]/div[2]/div/div/div/div/div").text
        ipaddr = driver.find_element_by_xpath("//div[3]/div[2]/div/div/div/div[2]/div").text
        macaddr = driver.find_element_by_xpath("//div[2]/div/div/div/div[3]/div").text
        print(f"{bcolors.HEADER_PURPLE}{state}{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}{ipaddr}{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}{macaddr}{bcolors.ENDC}")
        
        #Test4 - Use profile3 to discover DAP2 and check status is correct
        try:
            self.assertEqual("Standalone", state)
            self.assertEqual("172.17.193.249", ipaddr)
            self.assertEqual("18:0f:76:32:ea:30", macaddr)
            print(f"{bcolors.PASS_GREEN}Test4 - Use profile3 to discover DAP2 and check status is correct -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test4 - Use profile3 to discover DAP2 and check status is correct -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test4.png')
            code = 1
        
        #Click cancel to exit page
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Cancel')]"))).click()


        if 'code' in locals():
            sys.exit(code)
          


if __name__ == "__main__":
    unittest.main()