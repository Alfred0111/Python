import sys
from auto_pkg.auto import Bcolors, Format_check, WiFi_control


# DEFINE PARAMETER
method = sys.argv[1]
vmnumber = sys.argv[2]

# LOG
print(f"{Bcolors.PARM_YELLOW}METHOD is {method}{Bcolors.ENDC}")
print(f"{Bcolors.PARM_YELLOW}VMNUMBER is {vmnumber}{Bcolors.ENDC}")


# VM NUMBER FORMAT CHECK
Format_check.vmnum_check(method, vmnumber)


# MAIN
if method == "Continuity":
    vmn = vmnumber.split("-")
    for i in range(int(vmn[0]), int(vmn[1])+1):
        WiFi_control.profile_clear(i)
else:
    vmn = vmnumber.split(",")
    count = 0
    listlen = len(vmn)
    while count < listlen:
        WiFi_control.profile_clear(int(vmn[count]))
        count += 1
