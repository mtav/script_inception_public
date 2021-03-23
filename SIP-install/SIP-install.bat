title SIP-install
C:
mkdir "C:\Development"
cd "C:\Development"
git clone https://github.com/mtav/script_inception_public.git C:\Development\script_inception_public
cd "C:\Development\script_inception_public"
git branch --set-upstream-to=origin/master master

pathman /au "%LOCALAPPDATA%\Programs\Python\Python37"
pathman /au "C:\Development\script_inception_public\src\bin"
pathman /au "C:\Development\bin\ImageMagick-7.0.8-49-portable-Q16-x64"

setx SIP_PATH C:\Development\script_inception_public\src
setx PYTHONPATH C:\Development\script_inception_public\src

pause
