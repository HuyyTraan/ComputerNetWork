@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo        WeApRous P2P Chat - Easy Launch Script
echo ============================================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed!
    echo.
    echo Please install Node.js from: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo [OK] Node.js detected
echo.

REM Check if dependencies are installed
if not exist "node_modules" (
    echo [INFO] Installing dependencies...
    npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
)

REM Get username from user
set /p USERNAME="Enter your username: "
if "%USERNAME%"=="" (
    echo [ERROR] Username cannot be empty
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Starting P2P Chat for: %USERNAME%
echo ============================================================
echo.

REM Start WeApRous server if not running
echo [1/3] Checking WeApRous server...
curl -s http://127.0.0.1:8000 >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Starting WeApRous server...
    start "WeApRous-Server" cmd /k "python start_app.py"
    timeout /t 3 /nobreak >nul
) else (
    echo [OK] WeApRous server already running
)

REM Start P2P client
echo [2/3] Starting P2P client for %USERNAME%...
start "P2P-%USERNAME%" cmd /k "node p2p_client.js %USERNAME%"

REM Wait for P2P client to start
echo [INFO] Waiting for P2P client to initialize...
timeout /t 3 /nobreak >nul

REM Open browser
echo [3/3] Opening browser...
start "" "http://127.0.0.1:8000/p2p_integrated.html?auto"

echo.
echo ============================================================
echo [SUCCESS] P2P Chat UI launched!
echo ============================================================
echo.
echo Next steps:
echo   1. Check the P2P client terminal for WebSocket port
echo   2. In the browser, the port should auto-detect
echo   3. If not, enter the port manually
echo   4. Click "Connect to P2P Client"
echo   5. Start chatting!
echo.
echo To chat with another user:
echo   - Run this script again on another terminal with different username
echo   - OR run: node p2p_client.js ^<other-username^>
echo.
pause
