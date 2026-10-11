@echo off
title HMM Continuous Trading Bot - COEP Quantitative Finance Club
cd /d "c:\Users\Ved Bajaj\Desktop\Lifox\QF Club\HHM"
echo ====================================================================
echo  HMM Continuous Trading Bot -- Indian Equities (NSE)
echo  Active Trading Hours : 09:15 AM to 03:30 PM IST (Monday - Friday)
echo  Polling Frequency    : Every 60 seconds during market session
echo  Automatic Standby    : Low-power countdown outside market hours
echo ====================================================================
python trading_bot.py --loop --interval 60
pause

