@echo off
title HMM Continuous Trading Bot - COEP Quantitative Finance Club
cd /d "%~dp0"
echo ====================================================================
echo  HMM Continuous Trading Bot -- Indian Equities (NSE)
echo  Active Trading Hours : 09:15 AM to 03:30 PM IST (Monday - Friday)
echo  Polling Frequency    : Every 60 seconds during market session
echo  Automatic Standby    : Low-power countdown outside market hours
echo  Sync Target Remote   : lifox (Lifox21/Sectors-)
echo ====================================================================
python trading_bot.py --loop --interval 60 --auto-push --remote lifox --branch master
pause
