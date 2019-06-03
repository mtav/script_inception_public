REM Set up variables
set NSI_FILE=script_inception_public.nsi

REM create setup for new
"C:\Program Files\NSIS\makensis.exe" "%NSI_FILE%"
IF ERRORLEVEL 1 EXIT /B

