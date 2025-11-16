@echo off
echo ===================================
echo     WeApRous P2P Test Suite
echo ===================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js detected
echo.

REM Install dependencies
echo 📦 Installing dependencies...
npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo 🚀 Starting P2P Test Environment
echo.
echo This will open multiple terminals:
echo   • WeApRous Server
echo   • P2P Client: Alice
echo   • P2P Client: Bob
echo.

REM Start WeApRous server
echo [1/3] Starting WeApRous Server...
start "WeApRous-Server" cmd /c "python start_app.py"
timeout /t 3 /nobreak >nul

REM Start P2P clients
echo [2/3] Starting P2P Client: Alice...
start "P2P-Alice" cmd /c "npm run alice"
timeout /t 2 /nobreak >nul

echo [3/3] Starting P2P Client: Bob...
start "P2P-Bob" cmd /c "npm run bob"

echo.
echo ✅ All services started!
echo.
echo 🎯 Test P2P Commands:
echo   In Alice terminal:
echo     connect bob
echo     send bob Hello from Alice!
echo.
echo   In Bob terminal:
echo     connect alice  
echo     send alice Hi Alice!
echo.
echo 🌐 Browser UI: http://127.0.0.1:8000/chat.html
echo.
pause