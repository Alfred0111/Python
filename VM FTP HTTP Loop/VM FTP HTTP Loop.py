import os
import time
import sys
import datetime


# DEFINE PARM
action = sys.argv[1]
print(f"ACTION is {action}")
if action == "Start":
    mode = sys.argv[2]
    value = sys.argv[3]
    url = sys.argv[4]
    print(f"MODE is {mode}")
    if mode != "Loop":
        print(f"VALUE is {value}")
    print(f"URL is {url}")


# DEFINE FUNCTION
def http():
    http = os.system(rf'C:\http-ping.exe {url}')
    return http

def ftp():
    os.chdir(r"C:\FTP-download")
    ftp = os.system(r'C:\FTP-download\ftp-single.bat')
    return ftp


# MAIN
if mode == "Counts":
    for ct in range(1, int(value)+1):
        print(f"No.{str(ct)}- Start HTTP ping test.....")
        res1 = http()
        if res1 == 100:
            print("HTTP test passed")
        else:
            print("HTTP test failed")
        print(f"No.{str(ct)}- Start FTP download test.....")
        res2 = ftp()
        if res2 == 666:
            print("FTP test passed")
        else:
            print("FTP test failed")
    print("Test finished.....")
elif mode == "Duration":
    stime = int(time.time())
    etime = stime + int(value)
    gettime = int(time.time())
    start = datetime.datetime.now()
    print(f"Test start now {str(start)}")
    ct = 1
    while gettime <= etime:
        print(f"No.{str(ct)}- Start HTTP ping test.....")
        res1 = http()
        if res1 == 100:
            print("HTTP test passed")
        else:
            print("HTTP test failedf")
        print(f"No.{str(ct)}- Start FTP ownload test.....")
        res2 = ftp()
        if res2 == 666:
            print("FTP test passed")
        else:
            print("FTP test failed")
        ct += 1
        gettime = int(time.time())
    end = datetime.datetime.now()
    print(f"Test finished {str(end)}")
else:
    ct = 1
    while True:
        print(f"No.{str(ct)}- Start HTTP ping test.....")
        res1 = http()
        if res1 == 100:
            print("HTTP test passed")
        else:
            print("HTTP test failed")
        print(f"No.{str(ct)}- Start FTP download test.....")
        res2 = ftp()
        if res2 == 666:
            print("FTP test passed")
        else:
            print("FTP test failed")
        ct += 1


os.system("pause")
