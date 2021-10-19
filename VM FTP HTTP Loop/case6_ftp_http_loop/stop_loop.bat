@ECHO off

TITLE "STOP_LOOP"

ECHO %date:~5,5% %time:~0,8% SCRIPT: case6_ftp_http_loop/stop_loop >> C:\vm%1%_log.txt
ECHO %date:~5,5% %time:~0,8% START_TIME: %date:~5,5% %time:~0,8% >> C:\vm%1%_log.txt

taskkill /f /im http-ping.exe
taskkill /f /im ping.exe
taskkill /f /im ftp.exe
taskkill /f /im cmd.exe 