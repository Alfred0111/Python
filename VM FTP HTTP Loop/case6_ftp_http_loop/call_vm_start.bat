@ECHO off

TITLE "CALL_VM_START"


IF %1%==A (
FOR /L %%i IN (%2 1 %3) DO (
C:\PSTools\psexec \\192.168.18.%%i -u WIN7VM-1 -p sassd -i -d -c -f "c:\MultiClientAutoTest\case6_ftp_http_loop\start_loop.bat" %%i
)
)

IF %1%==B (
FOR /L %%i IN (%2 1 %3) DO (
C:\PSTools\psexec \\192.168.19.%%i -u WIN7VM-1 -p sassd -i -d -c -f "c:\wifi_batch\start_loop.bat" %%i
)
)

IF %1%==C (
FOR /L %%i IN (%2 1 %3) DO (
C:\PSTools\psexec \\192.168.20.%%i -u WIN7VM-1 -p sassd -i -d -c -f "c:\wifi_batch\start_loop.bat" %%i
)
)

IF %1%==D (
FOR /L %%i IN (%2 1 %3) DO (
C:\PSTools\psexec \\192.168.21.%%i -u WIN7VM-1 -p sassd -i -d -c -f "c:\wifi_batch\start_loop.bat" %%i
)
)