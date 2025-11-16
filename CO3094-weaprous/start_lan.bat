@echo off
cd /d "%~dp0"

echo.
echo ===================================
echo      WeApRous LAN Launcher
echo ===================================
echo Current Network IP: 10.128.9.159
echo.
echo Starting services for LAN access...
echo.

echo [1/3] Starting Backend Server (Port 9000)...
start "Backend-9000" /MIN cmd /c "cd /d %~dp0 && python start_backend.py --ip 10.128.9.159 --port 9000"
timeout /t 2 /nobreak >nul

echo [2/3] Starting App Server (Port 8000)...
start "App-8000" /MIN cmd /c "cd /d %~dp0 && python start_app.py --ip 10.128.9.159 --port 8000 --server-ip 10.128.9.159 --server-port 9000"
timeout /t 2 /nobreak >nul

echo [3/3] Starting Proxy Server (Port 8080)...
start "Proxy-8080" cmd /c "cd /d %~dp0 && python start_proxy.py --ip 10.128.9.159 --port 8080"

echo.
echo ✅ All services started!
echo.
echo 🌍 LAN Access URLs:
echo   • Task 1A: http://10.128.9.159:8080/
echo   • Task 2:  http://10.128.9.159:8081/
echo   • Direct:  http://10.128.9.159:8000/
echo.
echo 🏠 Local Access URLs:
echo   • Task 1A: http://127.0.0.1:8080/
echo   • Task 2:  http://127.0.0.1:8081/
echo   • Direct:  http://127.0.0.1:8000/
echo.
echo 🔑 Login Credentials:
echo   • Username: admin
echo   • Password: password
echo.
echo 📱 For mobile/other devices on LAN:
echo   • Make sure they're on same WiFi (10.128.x.x)
echo   • Use: http://10.128.9.159:8080/chat.html
echo.
echo Press any key to close launcher...
pause >nul