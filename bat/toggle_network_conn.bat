:: run as admin
set iface="Ethernet"
netsh interface show interface %iface% |find "Connected" >nul
if errorlevel 1 (netsh interface set interface %iface% enabled) else (netsh interface set interface %iface% disabled)
