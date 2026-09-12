@echo off
setlocal
set "FIM_TEST_STAGE=%LOCALAPPDATA%\FiMStudio-Validation-1.2.3"
set "FIM_TEST_REPORTS=%~dp0..\build"
if not exist "%FIM_TEST_STAGE%" mkdir "%FIM_TEST_STAGE%"
copy /Y "%FIM_TEST_REPORTS%\release\FiMpp-Studio-Portable-1.2.3-x64.exe" "%FIM_TEST_STAGE%\" >nul
if errorlevel 1 exit /b 1
copy /Y "%FIM_TEST_REPORTS%\release\FiMpp-Studio-Setup-1.2.3-x64.exe" "%FIM_TEST_STAGE%\" >nul
if errorlevel 1 exit /b 1
echo Testing portable EXE...
start "" /wait "%FIM_TEST_STAGE%\FiMpp-Studio-Portable-1.2.3-x64.exe" --self-test --report="%FIM_TEST_STAGE%\windows-portable-validation.json"
if not exist "%FIM_TEST_STAGE%\windows-portable-validation.json" (
 echo ERROR: The portable test did not produce its report.
 exit /b 1
)
copy /Y "%FIM_TEST_STAGE%\windows-portable-validation.json" "%FIM_TEST_REPORTS%\" >nul
echo Testing installer...
start "" /wait "%FIM_TEST_STAGE%\FiMpp-Studio-Setup-1.2.3-x64.exe" /S /D=%FIM_TEST_STAGE%\Installed
if not exist "%FIM_TEST_STAGE%\Installed\FiM++ Studio.exe" (
 echo ERROR: The installed application is missing.
 exit /b 1
)
echo Testing installed EXE...
start "" /wait "%FIM_TEST_STAGE%\Installed\FiM++ Studio.exe" --self-test --report="%FIM_TEST_STAGE%\windows-installed-validation.json"
if not exist "%FIM_TEST_STAGE%\windows-installed-validation.json" (
 echo ERROR: The installed test did not produce its report.
 exit /b 1
)
copy /Y "%FIM_TEST_STAGE%\windows-installed-validation.json" "%FIM_TEST_REPORTS%\" >nul
echo Test reports copied to the shared build folder.
echo Installed test app: %FIM_TEST_STAGE%\Installed\FiM++ Studio.exe
endlocal
