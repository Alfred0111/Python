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
#31/Time schedule/Time Range Max. End Time
#1. Connect Switch and Reset Switch to factory default.
#2. Login to DNC go to Configuration > Profile Setting > Switch > Common > Time Profile page.
#3. Create time profile Name entry .
#4. Enter the time range one Week Days, and End time 23:59 .then click Add button .
#5. Verify Time Profile Table entry list.
#6. Go to Configuration -> Profile -> Upload configuration click Apply button to push configuration to device.
#7. Check the Device log and check device push success or not.


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
   
        #--------------------Navigate to time profile page--------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Profile Settings')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'SW_Auto_Site1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'SW_Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Switch')])[4]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Common')])[4]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Time Profile')])[4]"))).click()

        #--------------------Configure time profile rule--------------------#
        #Input time profile name
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "name"))).send_keys("TestSch1")

        #select Sat
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[7]/p"))).click()

        #configure end time as 23:59
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[4]/div/div/div/span/span[2]/span"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[26]/span/span"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[4]/div[2]/div/div/span/span[2]/span"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[62]/span/span"))).click()

        #click add button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Add')]"))).click()
        time.sleep(1)

        #click save button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Time Profile saved successfully')]")))

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

        #--------------------------------------Check time profile setting--------------------------------------#
        #navigate to system D-Link Discovery Protocol page
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'System')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Time Profile')]"))).click()
        time.sleep(5)

        #switch frame
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_name("main"))

        #get profile name
        name = driver.find_element_by_xpath("//tr[3]/td/span").text
        print(f"{bcolors.INFO_WARNING_YELLOW}Profile name is {name}{bcolors.ENDC}")

        #get start time
        stime = driver.find_element_by_xpath("//div/table/tbody/tr[3]/td[2]").text
        print(f"{bcolors.INFO_WARNING_YELLOW}Start time is {stime}{bcolors.ENDC}")

        #get end time
        etime = driver.find_element_by_xpath("//div/table/tbody/tr[3]/td[3]").text
        print(f"{bcolors.INFO_WARNING_YELLOW}End time is {etime}{bcolors.ENDC}")

        #get weekdays
        week = driver.find_element_by_xpath("//tr[3]/td[4]/span").text
        print(f"{bcolors.INFO_WARNING_YELLOW}Weekdays is {week}{bcolors.ENDC}")

        
        #Test1 - Check profile time setting is correct
        try:
            self.assertEqual("  TestSch1", name)
            self.assertEqual(" 00:00", stime)
            self.assertEqual(" 23:59", etime)
            self.assertEqual(" Sat", week)
            print(f"{bcolors.PASS_GREEN}Test1 - Check profile time setting is correct -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test1 - Check profile time setting is correct -- FAIL{bcolors.ENDC}")
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
   
        #--------------------Navigate to time profile page--------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Profile Settings')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'SW_Auto_Site1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'SW_Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Switch')])[4]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Common')])[4]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Time Profile')])[4]"))).click()
        
        #--------------------Delete time profile rule--------------------#
        #click del button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div[6]/div/button[2]/md-icon"))).click()
        time.sleep(1)

        #click save button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Time Profile saved successfully')]")))

        #--------------------------------------Push config to device--------------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'SW_Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Apply')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration has uploaded successfully')]")))
        
        #Wait push success
        WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'1/1')]")))
        
        #Wait DAP1 apply the setting
        time.sleep(180)


if __name__ == "__main__":
    unittest.main()
