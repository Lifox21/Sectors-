@echo off
title Uninstall Windows Cron / Task Scheduler Tasks for HMM Bot
cd /d "%~dp0"

echo ====================================================================
echo  Uninstalling HMM Trading Bot Windows Scheduled Tasks
echo ====================================================================
echo.

schtasks /delete /tn "HMM_0915_Market_Open" /f 2>nul
schtasks /delete /tn "HMM_1215_Midday_Check" /f 2>nul
schtasks /delete /tn "HMM_1515_Rebalance_Window" /f 2>nul
schtasks /delete /tn "HMM_1530_Market_Close" /f 2>nul
schtasks /delete /tn "HMM_1600_EOD_Sync_Lifox" /f 2>nul

echo [SUCCESS] All HMM scheduled tasks removed from Windows Task Scheduler.
echo.
pause
