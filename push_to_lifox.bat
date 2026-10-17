@echo off
title Push to Lifox21 Public Repository
cd /d "%~dp0"
echo ====================================================================
echo  Pushing HMM Quantitative Trading System to Lifox21/Sectors-
echo ====================================================================
echo.
echo Launching Git authentication... (a browser window will open)
echo Please log in / authorize as Lifox21.
echo.
git push -u lifox master
echo.
if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] Codebase and Workflows successfully pushed to Lifox21!
) else (
    echo [ERROR] Push failed. Please check your GitHub credentials.
)
echo.
pause
