@ECHO off

TITLE "CALL_SERVER_STOP"

::ECHO Enter server code (capital letter A/B/C/D)
::SET /P server=

IF %server%==A (
C:\PSTools\psexec \\172.17.193.14 -u administrator -p test@1234 -c -f -d "C:\MultiClientAutoTest\case6_ftp_http_loop\call_vm_stop.bat" %server% %FVN% %LVN%
)

IF %server%==B (
C:\PSTools\psexec \\172.17.193.15 -u administrator -p test@1234 -c -f -d "C:\MultiClientAutoTest\case6_ftp_http_loop\call_vm_stop.bat" %server% %FVN% %LVN%
)

IF %server%==C (
C:\PSTools\psexec \\172.17.193.16 -u administrator -p test@1234 -i 2 -c -f -d "C:\MultiClientAutoTest\case6_ftp_http_loop\call_vm_stop.bat" %server% %FVN% %LVN%
)

IF %server%==D (
C:\PSTools\psexec \\172.17.193.17 -u administrator -p test@1234 -i 2 -c -f -d "C:\MultiClientAutoTest\case6_ftp_http_loop\call_vm_stop.bat" %server% %FVN% %LVN%
)