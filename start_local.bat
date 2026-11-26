@echo off
title BhashaAI - Local Development Launcher
echo ========================================================
echo        BhashaAI - AI Voice Translator Launcher
echo ========================================================
echo.

echo [1/3] Starting Backend Server (FastAPI on Port 8000)...
start "BhashaAI Backend (FastAPI)" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --reload --port 8000"

echo [2/3] Starting Frontend Server (Vite on Port 5173)...
start "BhashaAI Frontend (React)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo [3/3] Waiting for servers to initialize...
timeout /t 4 /nobreak >nul
start http://localhost:5173

echo.
echo ========================================================
echo Backend:  http://localhost:8000 (API Docs: http://localhost:8000/docs)
echo Frontend: http://localhost:5173
echo.
echo Master Admin: Superman0612 / Shubham@404
echo ========================================================
echo.
echo Dono servers running hain! In windows ko close mat karna jab tak kaam kar rahe ho.
echo.
pause
