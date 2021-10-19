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
#16.1.1/Feature Test-SSID And Security/SSID Test
#Verify the SSID configuration push to DAP
#1. On current profile, change the SSID to different character combination, The valid length shall be 0~32 characters.
#2. The SSID can consist of up to 32 alphanumeric characters, case-sensitive characters, special characters.
#3. SSID can not contain unicode and special symbol " ' ` & \

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
    
        #---------------------------------Go to Profile2 edit page---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Profile Settings')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Auto_Site2')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Auto_Network2')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Access Point')])[2]"))).click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'SSID')])[2]"))).click()

        #---------------------------------Test1 - Check ssid name character limit and add button status---------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "ssid")))
        pagedown = driver.find_element_by_tag_name('html')
        pagedown.click()
        pagedown.send_keys(Keys.PAGE_DOWN)
        time.sleep(5)


        #Test1 - Check ssid name character limit and add button status
        driver.find_element_by_name("ssid").send_keys("A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789A123456789")
        ssid_name = driver.find_element_by_name("ssid")
        try:
            self.assertEqual("A123456789A123456789A123456789A1", ssid_name.get_attribute('value'))
            #check add button can be clicked
            self.assertTrue(driver.find_element_by_xpath("//div[5]/button[2]").is_enabled())
            print(f"{bcolors.PASS_GREEN}Test1 - Check SSID name character limit and add button status -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test1 - Check SSID name character limit and add button status -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test1.png')
            code = 1


        #---------------------------------Test2 - Check SSID can not contain unicode and special symbol " ' ` & \---------------------------------#
        #Test "
        driver.find_element_by_name("ssid").clear()
        driver.find_element_by_name("ssid").send_keys("\"")
        warning1 = driver.find_element_by_xpath("//div/span[3]").text

        #Test '
        driver.find_element_by_name("ssid").clear()
        driver.find_element_by_name("ssid").send_keys("'")
        warning2 = driver.find_element_by_xpath("//div/span[3]").text

        #Test `
        driver.find_element_by_name("ssid").clear()
        driver.find_element_by_name("ssid").send_keys("`")
        warning3 = driver.find_element_by_xpath("//div/span[3]").text

        #Test &
        driver.find_element_by_name("ssid").clear()
        driver.find_element_by_name("ssid").send_keys("&")
        warning4 = driver.find_element_by_xpath("//div/span[3]").text

        #Test \
        driver.find_element_by_name("ssid").clear()
        driver.find_element_by_name("ssid").send_keys("\\")
        warning5 = driver.find_element_by_xpath("//div/span[3]").text
                     
        
        #Test2 - Check SSID can not contain unicode and special symbol " ' ` & \
        try:
            self.assertEqual(warning1,"SSID can not contain unicode and special symbol \" ' ` & \\")
            self.assertEqual(warning2,"SSID can not contain unicode and special symbol \" ' ` & \\")
            self.assertEqual(warning3,"SSID can not contain unicode and special symbol \" ' ` & \\")
            self.assertEqual(warning4,"SSID can not contain unicode and special symbol \" ' ` & \\")
            self.assertEqual(warning5,"SSID can not contain unicode and special symbol \" ' ` & \\")
            #check add button cann't be clicked
            self.assertFalse(driver.find_element_by_xpath("//div[5]/button[2]").is_enabled())
            print(f"{bcolors.PASS_GREEN}Test2 - Check SSID can not contain unicode and special symbol \" ' ` & \\ -- PASS{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL_RED}Test2 - Check SSID can not contain unicode and special symbol \" ' ` & \\ -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test2.png')
            code = 1
        
        if 'code' in locals():
            sys.exit(code)


if __name__ == "__main__":
    unittest.main()
      