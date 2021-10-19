#*************************MODULE IMPORT*************************#
import unittest
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

#*************************DEFINE ANSI COLOR CODE*************************#
class bcolors():
    HEADER_PURPLE = '\033[0;35m'
    PASS_GREEN = '\033[92m'
    INFO_WARNING_YELLOW = '\033[93m'
    FAIL_RED = '\033[91m'
    ENDC = '\033[0m'

#*************************CASE DESCRIPTION*************************#
#DGS-1210-10
#35/Vlan Description Test/To verify Vlan configuration will be push to switch properly
#1. Create a Profile.
#2. Enter to Basic Tab of Profile Settings and Expand VLAN configuration.
#3. Input VLAN ID (2-4094), and input some single bytes in description column, then click Add button.
#4. Make sure the the vlan ID&Description which we configured in Vlan list table.
#5. Try to click save button.
#6. Make sure the configuration is pushed into Switch.
#7. To create a new VLAN and input some double bytes (space key also need to check) in decription column, then click Add button.
#8. Make sure the the vlan ID&Description which we configured in Vlan list table.
#9. Try to click save button.
#10. Make sure the system work properly.

#*************************MAIN*************************#
class DNC_AUTOTEST(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe', chrome_options=options)
        self.url = "https://localhost:30001"
        self.dgsurl = "http://172.17.192.164"
        self.account = "admin"
        self.password = "Aa123456"

    def tearDown(self):
        self.driver.quit()

    def test1_dnc(self):
        driver = self.driver
        driver.get(self.url)
        driver.maximize_window()

        #--------------------Login to DNC--------------------# 
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
   
        #--------------------Navigate to switch basic page--------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Profile Settings')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'SW_Auto_Site1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'SW_Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Switch')])[4]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'DGS-1210')])[4]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Basic')])[11]"))).click()

        #--------------------Add VLAN rule 1--------------------#
        #Input VLAN ID
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "vlanId"))).send_keys("666")

        #Input description
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "vlanDescription"))).send_keys("VLAN666")

        #click add button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Add')]"))).click()
        time.sleep(1)

        #--------------------Add VLAN rule 2--------------------#
        #Input VLAN ID
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "vlanId"))).send_keys("888")

        #Input description
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "vlanDescription"))).send_keys("VLAN888 VLAN888")

        #click add button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Add')]"))).click()
        time.sleep(1)

        #click save button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Basic successfully saved')]")))

        #get VLAN rule 1 description
        des1 = driver.find_element_by_xpath("//div[2]/div/div[2]/div/div[2]/div").text
        print(f"{bcolors.INFO_WARNING_YELLOW}VLAN rule 1 description is {des1}{bcolors.ENDC}")

        #get VLAN rule 2 description
        des2 = driver.find_element_by_xpath("//div[3]/div/div[2]/div").text
        print(f"{bcolors.INFO_WARNING_YELLOW}VLAN rule 1 description is {des2}{bcolors.ENDC}")
       
        #Test1 - Add VLAN and verify VLAN description is correct
        try:
            self.assertEqual("VLAN666", des1)
            self.assertEqual("VLAN888 VLAN888", des2)
            print(f"{bcolors.PASS_GREEN}Test1 - Add VLAN and verify VLAN description is correct -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test1 - Add VLAN and verify VLAN description is correct -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test1.png')
            code = 1
                    
        #--------------------Delete VLAN rule--------------------#
        #click rule 2 del button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div[3]/div/div[3]/div/button[2]"))).click()
        time.sleep(1)
        
        #click rule 1 del button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div[2]/div/div[3]/div/button[2]"))).click()
        time.sleep(1)
                
        #click save button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Basic successfully saved')]")))
        time.sleep(3)
        
        if 'code' in locals():
            sys.exit(code)    





if __name__ == "__main__":
    unittest.main()
