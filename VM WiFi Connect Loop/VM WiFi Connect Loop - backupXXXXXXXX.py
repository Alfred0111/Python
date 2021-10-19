import os
import time
import sys
import random
import datetime

# DEFINE PARM
i = sys.argv[1]
action = sys.argv[2]
ssid = sys.argv[3]
security = sys.argv[4]
mode = sys.argv[5]
value = sys.argv[6]


# PRINT PARAMETERS WHICH RECEIVED FROM SERVRE MAIN
print(f"VM number is {i}")
print(f"Action is {action}")
print(f"SSID is {ssid}")
print(f"Security is {security}")
print(f"Mode is {mode}")
if mode != "Loop":
    print(f"Value is {value}")
print()

# CHECK SECURITY TYPE AND DEFINE VARIABLE
if security == 'none':
    secname = 'none'
    status = '開啟'
    pfname = 'AutoTest_none'
elif security == 'WPA2':
    secname = 'WPA2_personal'
    status = 'WPA2-Personal'
    pfname = 'AutoTest_WPA2_personal'
else:
    secname = 'WPA3_personal'
    status = 'WPA3-個人'
    pfname = 'AutoTest_WPA3_personal'

# PRE ACTION
#Clear vm report
print("Clear VM report.....")
#vm_report = 'C:\\Auto_Test_Folder\\Report\\report_con_loop'+str(i)+'.txt'
vm_report = rf"C:\Auto_Test_Folder\Report\report_con_loop{str(i)}.txt"
if os.path.exists(vm_report):
    os.remove(vm_report)
print()

#Clear wifi profile
print('Clear wifi profile.....')
os.system('netsh wlan delete profile name=*')
print()

#Import wifi profile
print('Import new wifi profile.....')
os.system('netsh wlan add profile filename=C:\\Auto_Test_Folder\\WLAN-'+secname+'_manual.xml')
print()

#**********DEFINE FUNCTION**********#
def LOG(message):
    with open(vm_report, "a+") as text_file:
        print(message, file=text_file)

def CONNECT():
    wait = random.randint(10,60) #0 - Wait random time 10-60 sec
    before = datetime.datetime.now()
    print(str(before)+' Will connect to wifi after ' +str(wait)+ ' seconds')
    LOG(str(before)+' Will connect to wifi after ' +str(wait)+ ' seconds')
    time.sleep(wait)

    con = datetime.datetime.now()
    print()
    print(str(con)+' Starting to connect wifi')
    LOG(str(con)+' Starting to connect wifi')
    os.system('netsh wlan connect name=AutoTest_'+secname+' ssid='+ssid+' interface=WLAN') #0 - Connect to wifi
    time.sleep(20)

    print()
    print('Display wlan interface status:')
    os.system('netsh wlan show interface > "C:\\Auto_Test_Folder\\connect.txt" && netsh wlan show interface') #1 - Write and display wlan status to text file

    discon = datetime.datetime.now()
    print()
    print(str(discon)+' Starting to disconnect wifi')
    LOG(str(discon)+' Starting to disconnect wifi')
    os.system('netsh wlan disconnect interface="WLAN"') #2 - Disconnect to wifi

    text = open("C:\\Auto_Test_Folder\\connect.txt",'r') #3 - Read connect result from text file
    connectres = text.read()
    text.close()
    return connectres

#**********MAIN**********#
if mode =='Counts':
    for a in range(1,int(value)+1):
        connectres = CONNECT()
        if '連線' in connectres and ssid in connectres and status in connectres and pfname in connectres:
            print('#No.'+str(a)+'-Connect to wifi successfully!')
            LOG('#No.'+str(a)+'-Connect to wifi successfully!')
            LOG(connectres)
        else:
            print('#No.'+str(a)+'-Connect to wifi failed!')
            LOG('#No.'+str(a)+'-Connect to wifi failed!')
            LOG(connectres)
elif mode =='Duration':
    a = int(time.time())
    b = a + int(value)
    gettime = int(time.time())
    x = 1
    while gettime<=b:
        connectres = CONNECT()
        if '連線' in connectres and ssid in connectres and status in connectres and pfname in connectres:
            print('#No.'+str(x)+'-Connect to wifi successfully!')
            LOG('#No.'+str(x)+'-Connect to wifi successfully!')
            LOG(connectres)
        else:
            print('#No.'+str(x)+'-Connect to wifi failed!')
            LOG('#No.'+str(x)+'-Connect to wifi failed!')
            LOG(connectres)
        x += 1
        gettime = int(time.time())
    end = datetime.datetime.now()
    print('Test finished '+str(end))
    LOG('Test finished '+str(end))
else:
    a=1
    while a>=1:
        connectres = CONNECT()
        if '連線' in connectres and ssid in connectres and status in connectres and pfname in connectres:
            print('#No.'+str(a)+'-Connect to wifi successfully!')
            LOG('#No.'+str(a)+'-Connect to wifi successfully!')
            LOG(connectres)
        else:
            print('#No.'+str(a)+'-Connect to wifi failed!')
            LOG('#No.'+str(a)+'-Connect to wifi failed!')
            LOG(connectres)
        a += 1


os.system("pause")


