@echo off
set /p ver="Enter version: v"

for %%I in (.) do set currentdir=%%~nxI
if %currentdir% == "tools" cd ..

@echo on
mkdir dist\v%ver%
mkdir dist\v%ver%\windows
mkdir dist\v%ver%\linux

:: Windows
pyinstaller discord-attachments-downloader.py --onefile -i "NONE" --distpath dist\v%ver%\windows
call tools\copy_docs.cmd dist\v%ver%\windows
cd dist\v%ver%\windows
"C:\Program Files\7-Zip\7z.exe" a ..\discord-attachments-downloader-v%ver%-windows.zip
cd ..\..\..

:: Mac isn't supported bc Apple makes it fucking impossible to run their stuff on a VM
:: Will add once I get a Mac, which I'll do right after the Toronto Maple Leafs win the Stanley Cup
:: If you are on a Mac, try using the Linux version (idk if it works on Mac)
:: and failing that just run the py file directly

:: Linux
ubuntu run pyinstaller discord-attachments-downloader.py --onefile --distpath dist/v%ver%/linux
call tools\copy_docs.cmd dist\v%ver%\linux
cd dist\v%ver%\linux
"C:\Program Files\7-Zip\7z.exe" a ..\discord-attachments-downloader-v%ver%-linux.zip
::====================
::pause