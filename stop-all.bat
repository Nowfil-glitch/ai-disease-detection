@echo off
REM AI Disease Detection Platform - Windows Stop Script

echo ========================================
echo Stopping AI Disease Detection Platform
echo ========================================
echo.

echo Stopping backend server (port 8000)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo Stopping frontend server (port 3000)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo ========================================
echo All servers stopped!
echo ========================================
echo.
pause
