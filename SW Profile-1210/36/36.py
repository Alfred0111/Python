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
#36/Vlan Description Edit Test/To verify Vlan configuration will be push to switch properly
#1. To create VLAN and Description first.
#2. Click Edit button, the Vlan configuration will focus in the id we editted.
#3. Try to make some changes, then click Save button.
#4. To push the profile to switch, and make sure description is updated.
#5. Try to Edit vlan description with doulble bytes (space key also need to check) again. And make sure it works properly.
#6. To make sure the max length is 255.

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

        #--------------------Configure VLAN rule--------------------#
        #Input VLAN ID
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "vlanId"))).send_keys("666")

        #Input description
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "vlanDescription"))).send_keys("VLAN666")

        #click add button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Add')]"))).click()
        time.sleep(1)

        #click save button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Basic successfully saved')]")))

        #--------------------------------------Push config to device--------------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'SW_Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Apply')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration has uploaded successfully')]")))
        
        #Wait push success
        WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        
        #Wait DAP1 apply the setting
        time.sleep(180)

    def test2_dgs(self):
        driver = self.driver
        driver.get(self.dgsurl)
        driver.maximize_window()

        #--------------------------------------Login to DGS--------------------------------------# 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pinkpanther")))
        driver.find_element_by_id("pinkpanther").send_keys(self.password)
        driver.find_element_by_xpath("//input[@value='OK']").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Exit']"))).click()
        try:
            driver.switch_to.default_content()
            time.sleep(5)
            driver.switch_to.frame(driver.find_element_by_name("left"))
            driver.switch_to.frame(driver.find_element_by_name("treeConfig"))
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'DGS-1210-10')]")))
            print(f"{bcolors.INFO_WARNING_YELLOW}Login to DGS - OK{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Unable to login to DGS, stop the test{bcolors.ENDC}")
            driver.save_screenshot('./DGS Login failed.png')   
            sys.exit(1)  

        #--------------------------------------Check VLAN setting--------------------------------------#
        #navigate to 802.1Q VLAN page
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'VLAN')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'802.1Q VLAN')]"))).click()
        time.sleep(5)

        #switch frame
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_name("main"))

        #get VLAN name
        vlan = driver.find_element_by_xpath("//tr[3]/td[2]/span/input")
        print(f"{bcolors.INFO_WARNING_YELLOW}Profile name is {vlan.get_attribute('value')}{bcolors.ENDC}")
       
        #Test1 - To verify VLAN configuration will be push to switch properly
        try:
            self.assertEqual("666", vlan.get_attribute('value'))
            print(f"{bcolors.PASS_GREEN}Test1 - To verify VLAN configuration will be push to switch properly -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test1 - To verify VLAN configuration will be push to switch properly -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test1.png')
            code = 1
              
        if 'code' in locals():
            sys.exit(code)    

    def test3_dnc(self):
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

        #--------------------Modify VLAN rule--------------------#
        #Click VLAN rule edit button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div[3]/div/button/md-icon"))).click()
        time.sleep(2)

        #Input VLAN ID
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "vlanId"))).clear()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "vlanId"))).send_keys("777")

        #Input description
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "vlanDescription"))).clear()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "vlanDescription"))).send_keys("VLAN777")

        #click rule save button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]"))).click()
        time.sleep(1)

        #click save button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Basic successfully saved')]")))

        #--------------------------------------Push config to device--------------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'SW_Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Apply')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration has uploaded successfully')]")))
        
        #Wait push success
        WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        
        #Wait DAP1 apply the setting
        time.sleep(180)

    def test4_dgs(self):
        driver = self.driver
        driver.get(self.dgsurl)
        driver.maximize_window()

        #--------------------------------------Login to DGS--------------------------------------# 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pinkpanther")))
        driver.find_element_by_id("pinkpanther").send_keys(self.password)
        driver.find_element_by_xpath("//input[@value='OK']").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Exit']"))).click()
        try:
            driver.switch_to.default_content()
            time.sleep(5)
            driver.switch_to.frame(driver.find_element_by_name("left"))
            driver.switch_to.frame(driver.find_element_by_name("treeConfig"))
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'DGS-1210-10')]")))
            print(f"{bcolors.INFO_WARNING_YELLOW}Login to DGS - OK{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Unable to login to DGS, stop the test{bcolors.ENDC}")
            driver.save_screenshot('./DGS Login failed.png')   
            sys.exit(1)  

        #--------------------------------------Check VLAN setting--------------------------------------#
        #navigate to 802.1Q VLAN page
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'VLAN')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'802.1Q VLAN')]"))).click()
        time.sleep(5)

        #switch frame
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_name("main"))

        #get VLAN name
        vlan = driver.find_element_by_xpath("//tr[3]/td[2]/span/input")
        print(f"{bcolors.INFO_WARNING_YELLOW}Profile name is {vlan.get_attribute('value')}{bcolors.ENDC}")
       
        #Test2 - To verify edit VLAN configuration successfully
        try:
            self.assertEqual("777", vlan.get_attribute('value'))
            print(f"{bcolors.PASS_GREEN}Test2 - To verify edit VLAN configuration successfully -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test2 - To verify edit VLAN configuration successfully -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test2.png')
            code = 1
              
        if 'code' in locals():
            sys.exit(code)  


    def test5_dnc(self):
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

        #--------------------Check VLAN description max length--------------------#
        #Click VLAN rule edit button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div[3]/div/button/md-icon"))).click()
        time.sleep(2)

        #Input description
        string = ("A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789"
        "A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789"
        "A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "vlanDescription"))).clear()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "vlanDescription"))).send_keys(string)

        #click rule save button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]"))).click()
        time.sleep(1)

        #click save button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Basic successfully saved')]")))

        #get description text
        description = driver.find_element_by_xpath("//div[2]/div/div[2]/div/div[2]/div").text
        print(f"{bcolors.INFO_WARNING_YELLOW}VLAN rule description is {description}{bcolors.ENDC}")

        string_max = ("A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789"
        "A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789"
        "A123456789A123456789A123456789A123456789A123456789A1234")
       
        #Test3 - To verify description max length is 255
        try:
            self.assertEqual(string_max, description)
            print(f"{bcolors.PASS_GREEN}Test3 - To verify description max length is 255 -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test3 - To verify description max length is 255 -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test3.png')
            code = 1
                     
        #--------------------Delete VLAN rule--------------------#
        #click del button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div[2]/div/div[3]/div/button[2]"))).click()
        time.sleep(1)

        #click save button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Basic successfully saved')]")))

        #--------------------------------------Push config to device--------------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'SW_Auto_Network1')]"))).click()
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
