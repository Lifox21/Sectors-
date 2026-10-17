Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "c:\Users\Ved Bajaj\Desktop\Lifox\QF Club\HHM"
WshShell.Run "cmd /c python trading_bot.py --loop --interval 60 --auto-push --remote lifox >> scratch\bot_live.log 2>&1", 0, False
MsgBox "HMM Continuous Trading Bot started in background!" & vbCrLf & "Logs: scratch\bot_live.log" & vbCrLf & "Sync target: Lifox21/Sectors- (lifox)", 64, "HMM Trading Bot"
