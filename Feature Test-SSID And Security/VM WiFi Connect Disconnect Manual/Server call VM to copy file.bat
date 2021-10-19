TITLE "Server call VM to copy file"

::Create disk P: 
net use p: \\10.0.200.200\wifi_profile test@1234 /user:Administrator /persistent:NO > nul 2>&1

::VM copy wifi profile from disk P: 
copy "p:\WLAN-WPA_personal_manual.xml" "C:\Auto_Test_Folder\WLAN-WPA_personal_manual.xml" > nul 2>&1
copy "p:\WLAN-WPA2_personal_manual.xml" "C:\Auto_Test_Folder\WLAN-WPA2_personal_manual.xml" > nul 2>&1
copy "p:\WLAN-WPA3_personal_manual.xml" "C:\Auto_Test_Folder\WLAN-WPA3_personal_manual.xml" > nul 2>&1
copy "p:\WLAN-none_manual.xml" "C:\Auto_Test_Folder\WLAN-none_manual.xml" > nul 2>&1

::Create disk q: 
net use q: \\10.0.200.200\wifi_python test@1234 /user:Administrator /persistent:NO > nul 2>&1

::VM copy python file from disk Q: 
copy "q:\VM WiFi Connect Disconnect Manual.py" "C:\Auto_Test_Folder\VM WiFi Connect Disconnect Manual.py" > nul 2>&1
