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
#3.1.5/Create Profile/Copy Profile Test
#Verify the user can copy the configurations/ parameters between different profile.
#1. Create A profile, SSID=AAAAAAAA, Security=aaaaaaaa, Guest SSID=11111111, 22222222, 33333333
#2. Create B profile, SSID=BBBBBBBB, Security=bbbbbbbb, Guest SSID=44444444, 55555555, 66666666
#3. Create C profile, SSID=CCCCCCCC, Security=cccccccc, Guest SSID=77777777, 88888888, 99999999
#4. Copy A profile to B profile, all the configurations of B profile shall be covered by A profile.
#5. Copy C profile to A profile, all the configurations of A profile shall be covered by C profile.

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
        
        #-----------------------------------Create new profile 1-----------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Configuration')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Create Profile')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Add Network')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Add Network')]")))
        
        #Input site and network name
        driver.find_element_by_name("newsite").send_keys("Test_Site1")
        driver.find_element_by_name("netName").clear()
        driver.find_element_by_name("netName").send_keys("Test_Network1")
        
        #Click next button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Next')]"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Network Configurations')]")))
        
        #Select device type as AP
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(.,'Access Point')]"))).click()
        time.sleep(3)

        #Input key and device password Aa123456
        driver.find_element_by_xpath("//password-input[@id='password']/div/input").send_keys("12345678")
        driver.find_element_by_xpath("//input[@type='password']").send_keys("Aa123456")

        #Go to mesh network page
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Mesh Network Settings')]")))

        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Discover Network Settings')]")))
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        
        #Apply setting
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Discover Device')]")))
        driver.find_element_by_xpath("//button[contains(.,'Apply & Exit')]").click()

        #-----------------------------------Create new profile 2-----------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Add Network')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Add Network')]")))
        
        #Input site and network name
        driver.find_element_by_name("newsite").send_keys("Test_Site2")
        driver.find_element_by_name("netName").clear()
        driver.find_element_by_name("netName").send_keys("Test_Network2")
        
        #Click next button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Next')]"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Network Configurations')]")))

        #Select device type as AP
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(.,'Access Point')]"))).click()
        
        #Input key and device password Aa123456
        driver.find_element_by_xpath("//password-input[@id='password']/div/input").send_keys("12345678")
        driver.find_element_by_xpath("//input[@type='password']").send_keys("Aa123456")

        #Go to mesh network page
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Mesh Network Settings')]")))

        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Discover Network Settings')]")))
        driver.find_element_by_xpath("//button[contains(.,'Next')]").click()

        #Apply setting
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Discover Device')]")))
        driver.find_element_by_xpath("//button[contains(.,'Apply & Exit')]").click()

        #----------------------------------------Copy AP profile2 setting to new profile1----------------------------------------#
        #Click new profile1 copy button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[7]/div/div[7]/div/button[2]"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Network Profile Copy From')]")))
        
        #Drop-down menu(select Auto_site2)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[2]/span"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[4]/span/span"))).click()       
        driver.find_element_by_xpath("//button[contains(.,'Copy')]").click()
        time.sleep(3)
        
        #----------------------------------------Copy AP profile3 setting to new profile2----------------------------------------#
        #Click new profile2 copy button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[8]/div/div[7]/div/button[2]"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Network Profile Copy From')]")))
        
        #Drop-down menu(select Auto_site3)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[2]/span"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[5]/span/span"))).click()       
        driver.find_element_by_xpath("//button[contains(.,'Copy')]").click()
        time.sleep(3)
        
        #----------------------------------------Test1 - Check the setting of new profile1 is correct----------------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Profile Settings')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Test_Site1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Test_Network1')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Access Point')])[7]"))).click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'SSID')])[7]"))).click()
        
        #Check ssid value
        ssid1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[2]/div/div/div/div[3]/div"))).text
        print(f"{bcolors.INFO_WARNING_YELLOW}Test profile1 2.4GHz SSID is {ssid1}{bcolors.ENDC}")

        ssid2 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[2]/div/div[3]/div"))).text
        print(f"{bcolors.INFO_WARNING_YELLOW}Test profile1 5GHz 1 SSID is {ssid2}{bcolors.ENDC}")

        ssid3 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[3]/div/div[3]/div"))).text
        print(f"{bcolors.INFO_WARNING_YELLOW}Test profile1 5GHz 2 (Tri-Band) SSID is {ssid3}{bcolors.ENDC}")

        #Check guest ssid value
        guest_ssid1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[4]/div/div[3]/div"))).text
        print(f"{bcolors.INFO_WARNING_YELLOW}Test profile1 2.4GHz guest SSID is {guest_ssid1}{bcolors.ENDC}")

        guest_ssid2 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[5]/div/div[3]/div"))).text
        print(f"{bcolors.INFO_WARNING_YELLOW}Test profile1 5GHz 1 guest SSID is {guest_ssid2}{bcolors.ENDC}")
        
        guest_ssid3 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[6]/div/div[3]/div"))).text
        print(f"{bcolors.INFO_WARNING_YELLOW}Test profile1 5GHz 2 (Tri-Band) guest SSID is {guest_ssid3}{bcolors.ENDC}")

        if (ssid1 == "Auto_SSID2") and (ssid1 == "Auto_SSID2") and (ssid1 == "Auto_SSID2") and (guest_ssid1 == "Auto_SSID_Guest2")  and (guest_ssid2 == "Auto_SSID_Guest2") and (guest_ssid3 == "Auto_SSID_Guest2"):
            print(f"{bcolors.PASS_GREEN}Test1 - Check the setting of new profile1 is correct -- PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL_RED}Test1 - Check the setting of new profile1 is correct -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test1.png')
            code = 1
       

        #----------------------------------------Test2 - Check the setting of new profile2 is correct----------------------------------------#
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Test_Site2')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Test_Network2')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Access Point')])[8]"))).click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'SSID')])[8]"))).click()
        
        #Check ssid value
        ssid1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[2]/div/div/div/div[3]/div"))).text
        print(f"{bcolors.INFO_WARNING_YELLOW}Test profile2 2.4GHz SSID is {ssid1}{bcolors.ENDC}")

        ssid2 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[2]/div/div[3]/div"))).text
        print(f"{bcolors.INFO_WARNING_YELLOW}Test profile2 5GHz 1 SSID is {ssid2}{bcolors.ENDC}")

        ssid3 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[3]/div/div[3]/div"))).text
        print(f"{bcolors.INFO_WARNING_YELLOW}Test profile2 5GHz 2 (Tri-Band) SSID is {ssid3}{bcolors.ENDC}")

        #Check guest ssid value
        guest_ssid1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[4]/div/div[3]/div"))).text
        print(f"{bcolors.INFO_WARNING_YELLOW}Test profile2 2.4GHz guest SSID is {guest_ssid1}{bcolors.ENDC}")

        guest_ssid2 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[5]/div/div[3]/div"))).text
        print(f"{bcolors.INFO_WARNING_YELLOW}Test profile2 5GHz 1 guest SSID is {guest_ssid2}{bcolors.ENDC}")
        
        guest_ssid3 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[6]/div/div[3]/div"))).text
        print(f"{bcolors.INFO_WARNING_YELLOW}Test profile2 5GHz 2 (Tri-Band) guest SSID is {guest_ssid3}{bcolors.ENDC}")

        if (ssid1 == "Auto_SSID3") and (ssid1 == "Auto_SSID3") and (ssid1 == "Auto_SSID3") and (guest_ssid1 == "Auto_SSID_Guest3")  and (guest_ssid2 == "Auto_SSID_Guest3") and (guest_ssid3 == "Auto_SSID_Guest3"):
            print(f"{bcolors.PASS_GREEN}Test2 - Check the setting of new profile2 is correct -- PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL_RED}Test2 - Check the setting of new profile2 is correct -- FAIL{bcolors.ENDC}")
            driver.save_screenshot('./Test2.png')
            code = 1

        #----------------------------------------Delete test profile----------------------------------------#
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(.,'Create Profile')]"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[8]/div/div[9]/div/button[2]"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(.,'Yes')]"))).click()
        time.sleep(3)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[7]/div/div[9]/div/button[2]"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(.,'Yes')]"))).click()
        time.sleep(3)


        if 'code' in locals():
            sys.exit(code)
          


if __name__ == "__main__":
    unittest.main()