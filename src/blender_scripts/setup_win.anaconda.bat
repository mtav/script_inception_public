call "%USERPROFILE%\AppData\Local\anaconda3\Scripts\activate.bat"
cd /D "%~dp0"
echo %cd%
python setup_win.py
pause
