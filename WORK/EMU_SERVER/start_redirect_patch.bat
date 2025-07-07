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

:: 4001=> patch?? 20001 => server??
python packet_redirect_v3.py 210.101.85.171 4001 192.168.0.15 1510