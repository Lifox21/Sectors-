@echo off
title Stop HMM Trading Bot
echo Stopping any running HMM trading bot processes...
wmic process where "commandline like '%%trading_bot.py%%'" call terminate >nul 2>&1
echo Done! HMM trading bot has been stopped.
pause
