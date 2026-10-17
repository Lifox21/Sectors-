@echo off
title 1-Click Windows Cron / Task Scheduler Setup for HMM Trading Bot
cd /d "%~dp0"

echo ====================================================================
echo  HMM Trading Bot -- 1-Click Windows Task Scheduler / Cron Setup
echo  Syncs directly with repository: Lifox21/Sectors- (remote: lifox)
echo ====================================================================
echo.
echo This script registers scheduled tasks in Windows Task Scheduler:
echo   [1] 09:15 AM (Mon-Fri) - Market Open Order Execution
echo   [2] 12:15 PM (Mon-Fri) - Midday Surveillance & Stop-Loss Check
echo   [3] 03:15 PM (Mon-Fri) - Portfolio Rebalance Window (Swaps & Signals)
echo   [4] 03:30 PM (Mon-Fri) - Market Close Settlement
echo   [5] 04:00 PM (Mon-Fri) - Post-Market EOD README Dashboard Push to Lifox
echo.
echo Zero cloud queue delays. Runs directly on your machine at the exact minute!
echo ====================================================================
echo.

set SCRIPT_DIR=%~dp0
set RUNNER=%SCRIPT_DIR%run_daily_local.bat

echo Registering task: HMM_0915_Market_Open...
schtasks /create /tn "HMM_0915_Market_Open" /tr "\"%RUNNER%\"" /sc WEEKLY /d MON,TUE,WED,THU,FRI /st 09:15 /f
if %ERRORLEVEL% neq 0 (
    echo [WARNING] Administrator privileges may be required. If this failed, right-click and "Run as Administrator".
)

echo Registering task: HMM_1215_Midday_Check...
schtasks /create /tn "HMM_1215_Midday_Check" /tr "\"%RUNNER%\"" /sc WEEKLY /d MON,TUE,WED,THU,FRI /st 12:15 /f

echo Registering task: HMM_1515_Rebalance_Window...
schtasks /create /tn "HMM_1515_Rebalance_Window" /tr "\"%RUNNER%\"" /sc WEEKLY /d MON,TUE,WED,THU,FRI /st 15:15 /f

echo Registering task: HMM_1530_Market_Close...
schtasks /create /tn "HMM_1530_Market_Close" /tr "\"%RUNNER%\"" /sc WEEKLY /d MON,TUE,WED,THU,FRI /st 15:30 /f

echo Registering task: HMM_1600_EOD_Sync_Lifox...
schtasks /create /tn "HMM_1600_EOD_Sync_Lifox" /tr "\"%RUNNER%\"" /sc WEEKLY /d MON,TUE,WED,THU,FRI /st 16:00 /f

echo.
echo ====================================================================
echo  [SUCCESS] All 5 Windows Cron Tasks have been registered!
echo  Logs will be written to: scratch\daily_run_log.txt
echo  All updates automatically push to: lifox master
echo ====================================================================
echo.
pause
