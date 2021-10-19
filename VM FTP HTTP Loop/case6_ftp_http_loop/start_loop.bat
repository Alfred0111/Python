@ECHO off

TITLE "START_LOOP"

::clear or create log file::
ECHO= > C:\vm%1%_log.txt

ECHO %date:~5,5% %time:~0,8% SCRIPT: case6_ftp_http_loop/start_loop >> C:\vm%1%_log.txt
ECHO %date:~5,5% %time:~0,8% START_TIME: %date:~5,5% %time:~0,8% >> C:\vm%1%_log.txt


::start http request and ftp download loop::

ECHO %date:~5,5% %time:~0,8% ACTION: Run http-ping >> C:\vm%1%_log.txt
START C:\http-ping.exe http://www.google.com -t

CD C:\FTP-download\

ECHO %date:~5,5% %time:~0,8% ACTION: Run ftp-auto.bat >> C:\vm%1%_log.txt
CMD /k START C:\FTP-download\ftp-auto.bat 




:start

::check log file size::
FOR %%F IN (C:\vm%1%_log.txt) DO (
IF %%~zF GTR 5242880 RENAME %%F vm%1_log_%date:~5,2%%date:~8,2%.txt)

GOTO start