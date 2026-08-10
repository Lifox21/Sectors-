@echo off
cd /d "c:\Users\Ved Bajaj\Desktop\Lifox\QF Club\HHM"
echo --- Running Daily Market Sync: %date% %time% --- >> scratch/daily_run_log.txt
python scratch/sync_live_and_get_signals.py >> scratch/daily_run_log.txt 2>&1
echo --- Sync Completed --- >> scratch/daily_run_log.txt
