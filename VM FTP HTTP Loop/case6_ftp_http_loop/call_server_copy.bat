@ECHO off

TITLE CALL_SERVER_COPY

::copy wifi batch file from server A::
net use z: \\172.17.193.14\wifi_batch test@1234 /user:administrator /persistent:NO
copy z:\start_loop.bat c:\wifi_batch\start_loop.bat
copy z:\stop_loop.bat c:\wifi_batch\stop_loop.bat