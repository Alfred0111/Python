TITLE "Server call VM to copy file"

::Create disk q: 
net use q: \\10.0.200.200\wifi_python test@1234 /user:Administrator /persistent:NO > nul 2>&1

::VM copy python file from disk Q:
copy "q:\VM FTP HTTP Loop.py" "C:\Auto_Test_Folder\VM FTP HTTP Loop.py" > nul 2>&1
