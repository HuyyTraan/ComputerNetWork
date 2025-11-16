@echo off
echo ===================================
echo    Windows Firewall Configuration
echo ===================================
echo Setting up firewall rules for WeApRous LAN access...
echo Current IP: 10.128.9.159
echo.

REM Allow inbound connections for WeApRous ports
echo Adding firewall rules for WeApRous ports...

netsh advfirewall firewall add rule name="WeApRous-Backend-9000" dir=in action=allow protocol=TCP localport=9000
netsh advfirewall firewall add rule name="WeApRous-App-8000" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="WeApRous-Proxy-8080" dir=in action=allow protocol=TCP localport=8080
netsh advfirewall firewall add rule name="WeApRous-Proxy-8081" dir=in action=allow protocol=TCP localport=8081

echo.
echo ✅ Firewall rules added successfully!
echo.
echo Configured ports:
echo   • Port 9000 - Backend Server
echo   • Port 8000 - App Server  
echo   • Port 8080 - Proxy Server (Task 1A)
echo   • Port 8081 - Proxy Server (Task 2)
echo.
echo 🌐 LAN Access URLs:
echo   • Task 1A: http://10.128.9.159:8080/
echo   • Task 2:  http://10.128.9.159:8081/
echo   • Direct:  http://10.128.9.159:8000/
echo.
echo 📱 Mobile devices on same WiFi (10.128.x.x) can now access these URLs!
echo.
pause