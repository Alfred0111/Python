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
#5/DDP Discovery/Port DDP setting enable/diable
#1.Go to Configuration > Porfile Settings> Site> Network > Switch > Switch Series > Port Setting page. to select the port for setting then Click Edit icon :
#2.Go to DDP item, select Enable / Diable drop-down box.:
#3.Click Save button for save configuration.:
#4.Go to Configuration > Proile Settings> Site> Network > Switch Push Apply & Exit button to send config to switch device :
#5.Check the switch Port DDP Enable / Disable function is correct setup in switch device from console or web page:

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
   
        #--------------------Navigate to switch port setting page--------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Profile Settings')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'SW_Auto_Site1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'SW_Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Switch')])[4]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'DGS-1210')])[4]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Port Setting')])[11]"))).click()

        #--------------------Disable port1 DDP--------------------#
        #select port1
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div[2]/div/div/div/div/div/div/div"))).click()

        #click edit button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#edit path"))).click()

        #disable DDP feature
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[3]/div[2]/div/div/span/span[2]/span"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[3]/span/span"))).click()

        #click save button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]"))).click()
        time.sleep(3)

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

        #--------------------------------------Check port1 DDP is disabled--------------------------------------#
        #navigate to system D-Link Discovery Protocol page
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'System')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'D-Link Discover Protocol')]"))).click()
        time.sleep(5)

        #switch frame
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_name("main"))

        #get port1 DDP state
        state = driver.find_element_by_xpath("//td[2]/span").text
        print(f"{bcolors.INFO_WARNING_YELLOW}Port1 DDP state is {state}{bcolors.ENDC}")
        
        #Test1 - Check port1 DDP state is correct
        try:
            self.assertEqual(" Disabled", state)
            print(f"{bcolors.PASS_GREEN}Test1 - Check port1 DDP state is correct -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test1 - Check port1 DDP state is correct -- FAIL{bcolors.ENDC}")
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
   
        #--------------------Navigate to switch port setting page--------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Profile Settings')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'SW_Auto_Site1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'SW_Auto_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Switch')])[4]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'DGS-1210')])[4]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Port Setting')])[11]"))).click()

        #--------------------Enable port1 DDP--------------------#
        #select port1
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div[2]/div/div/div/div/div/div/div"))).click()

        #click edit button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#edit path"))).click()

        #enable DDP feature
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[3]/div[2]/div/div/span/span[2]/span"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[4]/span/span"))).click()

        #click save button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]"))).click()
        time.sleep(3)

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

        #--------------------------------------Check port1 DDP is enabled--------------------------------------#
        #navigate to system D-Link Discovery Protocol page
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'System')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'D-Link Discover Protocol')]"))).click()
        time.sleep(5)

        #switch frame
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_name("main"))

        #get port1 DDP state
        state = driver.find_element_by_xpath("//td[2]/span").text
        print(f"{bcolors.INFO_WARNING_YELLOW}Port1 DDP state is {state}{bcolors.ENDC}")
       
        #Test2 - Check port1 DDP state is correct
        try:
            self.assertEqual(" Enabled", state)
            print(f"{bcolors.PASS_GREEN}Test2 - Check port1 DDP state is correct -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test2 - Check port1 DDP state is correct -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test2.png')
            code = 1
              
        if 'code' in locals():
            sys.exit(code)  


if __name__ == "__main__":
    unittest.main()
