@echo off
cd /d "%~dp0"
echo ==================================================================== >> scratch\daily_run_log.txt
echo --- Running HMM Market Execution / Cron Sync: %date% %time% --- >> scratch\daily_run_log.txt
echo Target Remote: lifox (Lifox21/Sectors-) >> scratch\daily_run_log.txt
python trading_bot.py --once --auto-push --remote lifox --branch master >> scratch\daily_run_log.txt 2>&1
echo --- Execution Completed: %date% %time% --- >> scratch\daily_run_log.txt
