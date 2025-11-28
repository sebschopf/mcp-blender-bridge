@echo off
echo --- Script de Test pour le Controleur MCP ---

REM Chemin vers l'environnement virtuel
set VENV_PATH=%CD%\controller\.venv

REM Verifier si uv est installe
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Erreur: 'uv' n'est pas trouve. Veuillez l'installer.
    exit /b 1
)

echo.

echo --- Synchronisation de l'environnement virtuel ---
uv venv %VENV_PATH% --clear
if %errorlevel% neq 0 (
    echo Erreur lors de la creation de l'environnement virtuel.
    exit /b 1
)

echo.

echo --- Installation des dependances ---
uv pip install -r .\controller\requirements.txt --python %VENV_PATH%\Scripts\python.exe
if %errorlevel% neq 0 (
    echo Erreur lors de l'installation des dependances.
    exit /b 1
)

echo.

echo --- Installation du package controller en mode editable ---
uv pip install -e .\controller --python %VENV_PATH%\Scripts\python.exe
if %errorlevel% neq 0 (
    echo Erreur lors de l'installation du package controller.
    exit /b 1
)

echo.

echo.
echo --- Lancement de Ruff (Linting) ---
%VENV_PATH%\Scripts\python.exe -m ruff check controller/
if %errorlevel% neq 0 (
    echo Des erreurs de linting ont ete detectees.
    exit /b 1
)

echo.
echo --- Lancement de Pytest ---

%VENV_PATH%\Scripts\python.exe -m pytest controller/

if %errorlevel% neq 0 (

    echo Des tests ont echoue.

    exit /b 1

)

echo.
echo --- Lancement des tests de l'Addon Blender ---

REM Copier l'addon dans le dossier des scripts de Blender
xcopy /E /I /Y blender_addon "%APPDATA%\Blender Foundation\Blender\4.5\scripts\addons\blender_addon"

REM Installer psutil dans l'environnement Python de Blender en utilisant uv
uv pip install psutil --python "C:\Program Files\Blender Foundation\Blender 4.5\4.5\python\bin\python.exe"
if %errorlevel% neq 0 (
    echo Erreur lors de l'installation de psutil dans Blender Python avec uv.
    exit /b 1
)

REM Assurez-vous que Blender est dans votre PATH ou specifiez le chemin complet
"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe" -b --python blender_addon\tests\test_addon.py --python-expr "import bpy; bpy.ops.test.mcp_addon()"

if %errorlevel% neq 0 (
    echo Des tests de l'addon ont echoue.
    exit /b 1
)

echo.

echo --- Tous les tests ont reussi ---

