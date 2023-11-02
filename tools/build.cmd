@echo off
set /p ver="Enter version: v"

for %%I in (.) do set currentdir=%%~nxI
if %currentdir% == "tools" cd ..

@echo on
mkdir dist\v%ver%
mkdir dist\v%ver%\windows
mkdir dist\v%ver%\linux

:: Windows
:::::::::::::::::::::::::::::::::

:: Single-file disribution using pyinstaller is no longer used on Windows
:: Since it keeps getting detected as Wacapew.C by Windows Security, which is a false-positive
:: Tried telling MS that this isn't a virus, and I directed them to the source code
:: However whatever bot that runs the false-positive form says my program is still a virus
:: Which is fucking infuriating
:: So instead risking my sanity any further I'm going to use cxfreeze and dsitrubite the zip instead
:: Granted, 2-3 random AI AVs still detect it, but literally anything that isn't whitelisted gets detected by those stupid things

:: Build the exe using cxfreeze
:: \
cxfreeze .\discord-attachments-downloader.py --target-dir=dist\v%ver%\windows

:: Copy the doc files
:: \
call tools\copy_docs.cmd dist\v%ver%\windows

:: dist\v%ver%\windows
cd dist\v%ver%\windows

:: Compress the files
:: dist\v%ver%\windows\
"C:\Program Files\7-Zip\7z.exe" a ..\discord-attachments-downloader-v%ver%-windows.zip
cd ..\..\..

:: Mac isn't supported bc Apple makes it fucking impossible to run their stuff on a VM
:: Will add once I get a Mac, which I'll do right after the Toronto Maple Leafs win the Stanley Cup
:: If you are on a Mac, try using the Linux version (idk if it works on Mac)
:: and failing that just run the py file directly

:: Linux
:::::::::::::::::::::::::::::::::

ubuntu run pyinstaller discord-attachments-downloader.py --onefile --distpath dist/v%ver%/linux
call tools\copy_docs.cmd dist\v%ver%\linux
cd dist\v%ver%\linux
"C:\Program Files\7-Zip\7z.exe" a ..\discord-attachments-downloader-v%ver%-linux.zip

cd ..\..\..
py tools\get_hashes.py %ver%
::====================
::pause