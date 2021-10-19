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
#3.1.10/Create Profile/Import Profile to Discovered AP Test
#Verify the user can import the profile to selected AP, then take effect immediately on DAP UI.
#1. Select exist Profile, then Discover Standalone/ Managed/ Unmanaged AP.
#2. Input DAP's username/ password, then import to discovered AP, the profile shall apply to DAP immediately.
#3. Input wrong username/ password, then import to discovered AP, the profile shall not apply to DAP.

#----------MAIN----------#
class DNC_AUTOTEST(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe', chrome_options=options)
        self.url = "https://localhost:30001"
        self.account = "admin"
        self.password = "Aa123456"
        self.device_ip = "172.17.193.249"

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
        
        #------------------------------------------------Navigate to Create Profile page------------------------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Create Profile')]"))).click()
        
        #------------------------------------------------Manage the AP2 via profile3 using incorrect username------------------------------------------------#
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[3]/div/div[8]/div/button"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Discover Network Settings')]")))               
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Discover Device')]")))
        driver.find_element_by_id("discover_button").click()
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Scan Finished')]")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div[2]/div/div[2]/div/div/div/div/div/div/div"))).click()
        driver.find_element_by_xpath("//div[3]/input").clear()
        driver.find_element_by_xpath("//div[3]/input").send_keys("erroruser")
        driver.find_element_by_xpath("//password-input/div/input").clear()
        driver.find_element_by_xpath("//password-input/div/input").send_keys("errorpwd")
        
        #Import to DAP2
        driver.find_element_by_xpath("//button[contains(.,'Import')]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Import Device(s)')]")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Yes')]"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//p[contains(.,'Task successfully sent!')]")))

        time.sleep(15)

        #Import to DAP2
        driver.find_element_by_xpath("//button[contains(.,'Import')]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Import Device(s)')]")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Yes')]"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//p[contains(.,'Task successfully sent!')]")))
        
        #Test1 - Input wrong username/ password, then import to discovered AP, the profile shall not apply to DAP
        try:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Fail')]")))
            driver.find_element_by_xpath("//button[contains(.,'Cancel')]").click()
            print(f"{bcolors.PASS_GREEN}Test1 - Input wrong username/ password, then import to discovered AP, the profile shall not apply to DAP -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test1 - Input wrong username/ password, then import to discovered AP, the profile shall not apply to DAP -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test1.png')
            code = 1
           
        #------------------------------------------------Manage the AP2 via profile3 using correct username------------------------------------------------#
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[3]/div/div[8]/div/button"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Discover Network Settings')]")))               
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Discover Device')]")))
        driver.find_element_by_id("discover_button").click()
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Scan Finished')]")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div[2]/div/div[2]/div/div/div/div/div/div/div"))).click()
        driver.find_element_by_xpath("//password-input/div/input").clear()
        driver.find_element_by_xpath("//password-input/div/input").send_keys("admin")
        
        #Import to DAP2
        driver.find_element_by_xpath("//button[contains(.,'Import')]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Import Device(s)')]")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Yes')]"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//p[contains(.,'Task successfully sent!')]")))

        time.sleep(15)

        #Import to DAP2
        driver.find_element_by_xpath("//button[contains(.,'Import')]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Import Device(s)')]")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Yes')]"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//p[contains(.,'Task successfully sent!')]")))
        
        #Test2 - Input DAP's username/ password, then import to discovered AP, the profile shall apply to DAP immediately
        try:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Success')]")))
            driver.find_element_by_xpath("//button[contains(.,'Cancel')]").click()
            print(f"{bcolors.PASS_GREEN}Test2 - Input DAP's username/ password, then import to discovered AP, the profile shall apply to DAP immediately -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test2 - Input DAP's username/ password, then import to discovered AP, the profile shall apply to DAP immediately -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test2.png')
            code = 1

        #------------------------------------------------DAP2 run factory default------------------------------------------------#   
        print(f"{bcolors.HEADER_PURPLE}Wait for DAP(2) apply setting{bcolors.ENDC}") 
        time.sleep(180)
        print(f"{bcolors.HEADER_PURPLE}Wait for DAP(2) reset to default setting{bcolors.ENDC}") 
        tn=Telnet(self.device_ip)
        tn.read_until(b"login:")
        tn.write("admin".encode('ascii') + b"\r\n")
        tn.read_until(b"Password:")
        tn.write("Aa123456".encode('ascii') + b"\r\n")
        tn.write("set factorydefault".encode('ascii') + b"\r\n")
        time.sleep(20)
        res1 = tn.read_very_eager().decode('ascii')
        print(f"{bcolors.HEADER_PURPLE}********************{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}{res1}{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}********************{bcolors.ENDC}")

        tn.write("reboot".encode('ascii') + b"\r\n")
        time.sleep(10)
        res2 = tn.read_eager().decode('ascii')
        tn.write("exit".encode('ascii') + b"\r\n")
        print(f"{bcolors.HEADER_PURPLE}{res2}{bcolors.ENDC}")
        print(f"{bcolors.HEADER_PURPLE}********************{bcolors.ENDC}")
        time.sleep(300)

        
        if 'code' in locals():
            sys.exit(code)


if __name__ == "__main__":
    unittest.main()