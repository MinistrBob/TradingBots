rem Date and time for file name, hours are counted <10 (one character instead of two => 07).
FOR /F "tokens=1-4 delims=., " %%i IN ('DATE /t') DO SET pdate=%%k_%%j_%%i
FOR /F "tokens=1-4 delims=:"  %%b IN ('TIME /T') DO SET ptime=%%b_%%c
set date_name=%pdate%_%ptime%
rem echo %date_name%

rem Base Project Folder
rem SET BASEPATH=c:\mysources
rem Folder Project Name 
SET PNAME=MyStudyProjects
rem Backup Path
SET BP=%BACKUP_PATH%\%PNAME%
rem Path to WinRAR
rem SET WINRAR=C:\Program Files\WinRAR\WinRAR.exe
rem Path to 7-Zip
rem SET SZIP=c:\Program Files\7-Zip\7z.exe

mkdir "%BP%"
rem "%WINRAR%" a -r -s -m5 -md1024 -ag_YYYYMMDD-NN "%BP%\%PNAME%.rar" "c:\MyGit\%PNAME%\*"
"%SZIP%" a -t7z -r -mx9 -mtc=on -mta=on -mtr=on -xr@exclude.txt -xr!__pycache__ "%BP%\%date_name%_%PNAME%.7z" "%BASEPATH%\%PNAME%\*"
"%SZIP%" a -t7z -r -mx9 -mtc=on -mta=on -mtr=on -p%mypass% -ir@exclude.txt "%BP%\%date_name%_%PNAME%_PASS.7z" "%BASEPATH%\%PNAME%\exclude.txt"
rem Delete backups except last 6
cd /d "%BP%"
for /f "skip=6 eol=: delims=" %%F in ('dir /b /o-d *.7z') do @del "%%F"

pause
