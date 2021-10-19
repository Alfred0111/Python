import sys
from auto_pkg.auto import Bcolors, Format_check, System

# DEFINE PARAMETER
action = sys.argv[1]
method = sys.argv[2]
vmnumber = sys.argv[3]


# LOG
print(f"{Bcolors.PARM_YELLOW}ACTION is {action}{Bcolors.ENDC}")
print(f"{Bcolors.PARM_YELLOW}METHOD is {method}{Bcolors.ENDC}")
print(f"{Bcolors.PARM_YELLOW}VMNUMBER is {vmnumber}{Bcolors.ENDC}")


# DEFINE ACTION PARM
if action == "Open":
    url = sys.argv[4]
    print(f"{Bcolors.PARM_YELLOW}URL is {url}{Bcolors.ENDC}")


# VM NUMBER FORMAT CHECK
Format_check.vmnum_check(method, vmnumber)


# MAIN
if method == "Continuity":
    vmn = vmnumber.split("-")
    for i in range(int(vmn[0]), int(vmn[1])+1):
        if action == "Open":
            System.openchrome(i, url)
        else:
            System.closechrome(i)
else:
    vmn = vmnumber.split(",")
    count = 0
    list_len = len(vmn)
    while count < list_len:
        if action == 'Open':
            System.openchrome(int(vmn[count]), url)
        else:
            System.closechrome(int(vmn[count]))
        count += 1
