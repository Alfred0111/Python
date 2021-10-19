#**********IMPORT MODULE**********#
import os 
import time  
import sys
import shutil

#**********DEFINE VARIABLE**********#
action = sys.argv[1]
i = sys.argv[2]
ssid = sys.argv[3]
security = sys.argv[4] 

#**********CHECK SECURITY TYPE AND DEFINE VARIABLE**********#
if security == 'none':
    secname = 'none'
    status = '開放'
    pfname = 'AutoTest_none'
elif security == 'WPA2':
    secname = 'WPA2_personal'
    status = 'WPA2-Personal'
    pfname = 'AutoTest_WPA2_personal'
else:
    secname = 'WPA3_personal'
    status = 'WPA3-個人'
    pfname = 'AutoTest_WPA3_personal'

#**********PRE ACTION**********#
#Clear vm report
vm_report = 'C:\\Auto_Test_Folder\\Report\\report'+str(i)+'.txt'
if os.path.exists(vm_report):
    os.remove(vm_report)
    
#**********DEFINE FUNCTION**********# 
def LOG(message):
    with open(vm_report, "a+") as text_file:
        print(message, file=text_file)

def CONNECT():
    os.system('netsh wlan delete profile name=*') #0 - delete wifi profile
    time.sleep(2)
    os.system('netsh wlan add profile filename=C:\\Auto_Test_Folder\\WLAN-'+secname+'_manual.xml') #1 - Import wifi profile
    time.sleep(3)
    os.system('netsh wlan connect name=AutoTest_'+secname+' ssid='+ssid+' interface=WLAN') #2 - Connect to wifi 
    time.sleep(20)
    os.system('netsh wlan show interface > "C:\\Auto_Test_Folder\\connect.txt"') #3 - Confirm status and return status
    text = open("C:\\Auto_Test_Folder\\connect.txt",'r') #4 - Read the status
    connectres = text.read()
    text.close()
    return connectres
    
#**********MAIN**********# 
if action == 'Connect':
    connectres = CONNECT()
    if '連線' in connectres and ssid in connectres and status in connectres and pfname in connectres:
        print('Connect to Wifi successfully!')
        LOG('VM '+str(i)+' connect to Wifi successfully!')
        time.sleep(5)
    else:
        #失敗時將LOG寫進report裡，將report複製到Server A 的wifi_report資料夾底下
        print('Connect to Wifi failed!')
        LOG('VM '+str(i)+' connect to Wifi failed!')
        #Create disk z: 
        os.system('net use z: \\\\10.0.200.200\\wifi_report test@1234 /user:Administrator /persistent:NO')
        #VM的report放到server A
        os.system('copy '+vm_report+' "z:\"')

        
