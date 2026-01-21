@echo off
echo ========================================
echo HeartMuLa Music Generator GUI
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found!
    echo Please create a virtual environment first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -e .
    echo.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting GUI application...
python gui_app.py

if errorlevel 1 (
    echo.
    echo An error occurred while running the application.
    pause
)

deactivate
