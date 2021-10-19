#----------MODULE IMPORT----------#
import unittest
import time
import sys
import os
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
#15/Create Profile/Export Profile Test
#Verify the user can export the existed profile to a .DAT file.
#Export existing profile, the system shall create a DAT file automatically.

#----------MAIN----------#
class DNC_AUTOTEST(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory" : r"D:\Chrome download folder"}
        options.add_experimental_option("prefs",prefs)
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
        
        #--------------------------------------------------Login to DNC--------------------------------------------------#
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
        
        #----------------------------------------Go to Configuration-Create Profile page----------------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Create Profile')]"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Add Network')]")))

        #Export profile .DAT file
        time.sleep(5)
        driver.find_element_by_css_selector(".btn-grid:nth-child(3) svg").click()
        time.sleep(5)

        #Define file
        filepath = r"D:\Chrome download folder\Auto_Network1.dat"
        
        #Test1 - Verify the .DAT file downloaded successfully       
        if os.path.isfile(filepath):
            print(f"{bcolors.PASS_GREEN}Test1 - Verify the .DAT file downloaded successfully -- PASS{bcolors.ENDC}")
            os.remove(filepath)
        else:
            print(f"{bcolors.FAIL_RED}Test1 - Verify the .DAT file downloaded successfully -- FAIL{bcolors.ENDC}")
            sys.exit(1)


if __name__ == "__main__":
    unittest.main()
      