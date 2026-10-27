@echo off
REM Spusti Jev: test lektora + Neohunter triedenie odpovedi kandidatov. Vystup ide do vystup_jev.txt
set PYTHONUTF8=1
set UV="%USERPROFILE%\.local\bin\uv.exe"
cd /d "%~dp0"
echo Spustam Jev priklady, vystup ide do vystup_jev.txt ...
echo 14_jev %date% %time% > vystup_jev.txt
echo ################ 1_basics\1_three_primitives.py >> vystup_jev.txt
pushd 1_basics
%UV% run 1_three_primitives.py >> ..\vystup_jev.txt 2>&1
popd
echo. >> vystup_jev.txt
echo ################ 5_neohunter\1_reply_triage_gate.py >> vystup_jev.txt
pushd 5_neohunter
%UV% run 1_reply_triage_gate.py >> ..\vystup_jev.txt 2>&1
echo. >> ..\vystup_jev.txt
echo ################ 5_neohunter\2_inbox_then_draft.py >> ..\vystup_jev.txt
%UV% run 2_inbox_then_draft.py >> ..\vystup_jev.txt 2>&1
popd
echo HOTOVO >> vystup_jev.txt
echo.
echo Hotovo. Okno mozes zavriet.
pause
