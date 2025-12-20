@echo off
REM Run All Examples - Chapter 8 Auto Exposure
REM Windows batch script to run all examples

cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist "..\..\virtual_env\Scripts\activate.bat" (
    call "..\..\virtual_env\Scripts\activate.bat"
)

REM Run the Python script
python run_all_examples.py %*
