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


# VM NUMBER FORMAT CHECK
Format_check.vmnum_check(method, vmnumber)


# MAIN
if method == "Continuity":
    vmn = vmnumber.split("-")
    for i in range(int(vmn[0]), int(vmn[1])+1):
        System.reboot_shutdown(i, action)
else:
    vmn = vmnumber.split(",")
    count = 0; listlen = len(vmn)
    while count < listlen:
        System.reboot_shutdown(int(vmn[count]), action)
        count += 1
