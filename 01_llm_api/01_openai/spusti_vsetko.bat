@echo off
REM Spusti vsetky priklady z 01_openai a ulozi vystup do vystup.txt
set PYTHONUTF8=1
set UV="%USERPROFILE%\.local\bin\uv.exe"
cd /d "%~dp0"
echo Spustam priklady 01_openai, vystup ide do vystup.txt ...
echo 01_openai %date% %time% > vystup.txt
for %%D in (1_basics 2_multimodal 3_chat_history 4_tools 5_generate_image) do (
  for %%F in (%%D\*.py) do (
    if /I not "%%~nxF"=="encode.py" (
      echo   %%F
      echo. >> vystup.txt
      echo ################ %%F >> vystup.txt
      pushd %%D
      %UV% run "%%~nxF" >> ..\vystup.txt 2>&1
      popd
    )
  )
)
echo HOTOVO >> vystup.txt
echo.
echo Hotovo. Okno mozes zavriet.
pause
