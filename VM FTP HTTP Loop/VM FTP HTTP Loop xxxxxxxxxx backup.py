#**********IMPORT MODULE**********#
import os 
import time  
import sys
import random
import datetime
import subprocess 

#**********DEFINE VARIABLE**********#
action = sys.argv[1]
divide1 = '★－:+:－:+:－:+:－:+:－:+:－:+:－:+:－:+:－:+:－:+:－★'
divide2 = '-*．-*．-*．-*．-*．-*．-*．-*．-*．-*．-*．-*．-*．-*．'
print(divide1)
print('ACTION is '+action)
if action == 'Start':
    mode = sys.argv[2]
    value = sys.argv[3]
    url = sys.argv[4]
    print('MODE is '+mode)
    if mode != 'Loop':
        print('VALUE is '+value)
    print('URL is '+url)
print(divide1)

#**********DEFINE FUNCTION**********# 
def HTTP():
    http = os.system(r'C:\http-ping.exe '+url+' > NUL 2>&1')
    return http

def FTP():
    os.chdir(r"C:\FTP-download")
    ftp = os.system(r'C:\FTP-download\ftp-single.bat > NUL 2>&1') 
    return ftp

def STOP():
    os.system('taskkill /f /t /im http-ping.exe')
    time.sleep(3) 
    os.system('taskkill /f /t /im ping.exe')
    time.sleep(3)
    os.system('taskkill /f /t /im ftp.exe')
    time.sleep(3)
    os.system('taskkill /f /t /im cmd.exe')
    time.sleep(3)
    os.system('taskkill /f /t /im python.exe')    
    
#**********MAIN**********#      
if action =='Start':
    if mode =='Counts':
        print(divide2)
        for ct in range(1,int(value)+1):
            print('No.'+str(ct)+'- Start HTTP ping test.....')
            res1 = HTTP()
            if res1 == 100:
                print('HTTP test passed')
            else:
                print('HTTP test failed')
            print('No.'+str(ct)+'- Start FTP download test.....')
            res2 = FTP()
            if res2 == 666:
                print('FTP test passed')
            else:
                print('FTP test failed')
            print(divide2)        
        print('Test finished.....')
    elif mode =='Duration':
        stime = int(time.time()) 
        etime = stime + int(value)
        gettime = int(time.time())
        start = datetime.datetime.now()
        print('Test start now '+str(start))
        ct = 1
        print(divide2)
        while gettime<=etime:
            print('No.'+str(ct)+'- Start HTTP ping test.....')
            res1 = HTTP()
            if res1 == 100:
                print('HTTP test passed')
            else:
                print('HTTP test failed')
            print('No.'+str(ct)+'- Start FTP download test.....')
            res2 = FTP()
            if res2 == 666:
                print('FTP test passed')
            else:
                print('FTP test failed')
            print(divide2)
            ct += 1
            gettime = int(time.time())
        end = datetime.datetime.now()
        print('Test finished '+str(end))
    else:
        ct = 1
        print(divide2)
        while True:
            print('No.'+str(ct)+'- Start HTTP ping test.....')
            res1 = HTTP()
            if res1 == 100:
                print('HTTP test passed')
            else:
                print('HTTP test failed')
            print('No.'+str(ct)+'- Start FTP download test.....')
            res2 = FTP()
            if res2 == 666:
                print('FTP test passed')
            else:
                print('FTP test failed')
            print(divide2)
            ct += 1
else :
    STOP()

os.system("pause")
