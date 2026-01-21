@echo off
set MAYA_VERSION=2025
set MAYA_DOCS_DIR=%USERPROFILE%\Documents\maya\%MAYA_VERSION%
set PLUGINS_DIR=%MAYA_DOCS_DIR%\plug-ins
set SCRIPTS_DIR=%MAYA_DOCS_DIR%\scripts
set ICONS_DIR=%MAYA_DOCS_DIR%\prefs\icons


for %%K in (
  "HKLM\SOFTWARE\Autodesk\Maya\%MAYA_VERSION%\Setup\InstallPath"
  "HKLM\SOFTWARE\WOW6432Node\Autodesk\Maya\%MAYA_VERSION%\Setup\InstallPath"
) do (
  for /f "tokens=2,*" %%A in ('reg query %%K /v MAYA_INSTALL_LOCATION 2^>nul') do (
    set MAYA_ROOT=%%B
  )
)

if not defined MAYA_ROOT (
    echo Maya %MAYA_VERSION% not found
    exit /b 1
)

if not exist "%MAYA_DOCS_DIR%" (
    echo Creating: %MAYA_DOCS_DIR%
    mkdir "%MAYA_DOCS_DIR%"
)

if not exist "%PLUGINS_DIR%" (
    echo Creating: %PLUGINS_DIR%
    mkdir "%PLUGINS_DIR%"
)

if not exist "%SCRIPTS_DIR%" (
    echo Creating: %SCRIPTS_DIR%
    mkdir "%SCRIPTS_DIR%"
)

if not exist "%ICONS_DIR%" (
    echo Creating: %ICONS_DIR%
    mkdir "%ICONS_DIR%"
)

echo %MAYA_ROOT%

echo "Installing pillow"

"%MAYA_ROOT%bin\mayapy.exe" -m pip install Pillow

echo "Copying plugins"

set AE_TEMPLATES_DIR=%MAYA_ROOT%scripts\AETemplates

for %%F in ("Resources\AETemplates\*.mel") do (

    if exist "%AE_TEMPLATES_DIR%\%%~nxF" (
        echo Removing existing: %%~nxF
        del "%AE_TEMPLATES_DIR%\%%~nxF"
    )

    echo Linking %%~nxF
    mklink "%AE_TEMPLATES_DIR%\%%~nxF" "%%~fF" 
)

rem copy /Y "Resources\AETemplates\*.*" "%MAYA_ROOT%scripts\AETemplates\*.*"

copy /Y "Resources\Images\*.*" "%ICONS_DIR%\*.*"

mklink /D "%SCRIPTS_DIR%\max_payne_maya" "%~dp0\max_payne_maya"

mklink /D "%SCRIPTS_DIR%\max_payne_sdk" "%~dp0\max_payne_sdk"

mklink "%PLUGINS_DIR%\max_payne_2_sdk_custom_nodes.py" "%~dp0max_payne_2_sdk_custom_nodes.py"

mklink "%PLUGINS_DIR%\max_payne_sdk_kf2_importer.py" "%~dp0max_payne_sdk_kf2_importer.py"

mklink "%PLUGINS_DIR%\max_payne_sdk_ldb_importer.py" "%~dp0max_payne_sdk_ldb_importer.py"



