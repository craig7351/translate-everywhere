@echo off
REM 只停止 AI 翻譯助手 (透過視窗標題篩選)
powershell -Command "Get-Process python* | Where-Object {$_.MainWindowTitle -like '*翻譯*'} | Stop-Process -Force" >nul 2>&1
echo AI 翻譯助手已停止
timeout /t 2 >nul
