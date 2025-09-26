@echo off
:: check administrator permission
net session >nul 2>&1
if %errorLevel% neq 0 (
	echo restart with administrator persmission
	powershell -Command "Start-Process cmd -ArgumentList '/c %~s0' -Verb RunAs"
	exit
)

:: run current path
cd /d "%~dp0"
echo currunt path: %CD%

:loop
python emu_server2_r01.py
echo restart after 5sec...
timeout /t 5
goto loop