@echo off
set VENV_PATH=%CD%\controller\.venv
echo --- Running Validation Tests ---
%VENV_PATH%\Scripts\python.exe -m pytest controller/tests/test_validation.py
if %errorlevel% neq 0 (
    echo Validation tests failed.
    exit /b 1
)
echo Validation tests passed.
