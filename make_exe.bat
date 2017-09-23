copy src\ctr\config.txt build\dist\config.txt
copy src\ctr\example.db build\dist\example.db

cd src
C:\Python\2.7.13\Scripts\pyinstaller.exe --clean --onefile --windowed --workpath ..\build\temp --distpath ..\build\dist ctr\Main.py