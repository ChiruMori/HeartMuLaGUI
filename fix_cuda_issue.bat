@echo off
echo ========================================
echo HeartMuLa - Fix CUDA Issue
echo ========================================
echo.
echo This script will:
echo 1. Remove the existing venv
echo 2. Recreate it with Python 3.10
echo 3. Install CUDA-enabled PyTorch
echo 4. Install Triton
echo 5. Install all dependencies
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo [1/5] Removing old virtual environment...
if exist "venv\" (
    rmdir /s /q venv
    echo ✓ Old venv removed
) else (
    echo ✓ No existing venv found
)

echo.
echo [2/5] Creating new venv with Python 3.10...
set PYTHON310_PATH=D:\AI\heartlib\drivers\310\python.exe

if not exist "%PYTHON310_PATH%" (
    echo ERROR: Python 3.10 not found at %PYTHON310_PATH%
    echo Please check the path
    pause
    exit /b 1
)

"%PYTHON310_PATH%" -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create venv
    pause
    exit /b 1
)

echo ✓ Virtual environment created

echo.
echo [3/5] Activating venv and upgrading pip...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip

echo.
echo [4/5] Installing PyTorch with CUDA 12.1...
echo This may take a few minutes...
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
if errorlevel 1 (
    echo ERROR: Failed to install PyTorch
    pause
    exit /b 1
)

echo ✓ PyTorch with CUDA installed

echo.
echo [5/5] Installing Triton...
set TRITON_WHL=D:\AI\heartlib\drivers\triton-2.1.0-cp310-cp310-win_amd64.whl

if exist "%TRITON_WHL%" (
    echo Installing from local wheel...
    python -m pip install "%TRITON_WHL%"
    if errorlevel 1 (
        echo WARNING: Local wheel failed, trying PyPI...
        python -m pip install triton
    )
) else (
    echo Local wheel not found, installing from PyPI...
    python -m pip install triton
)

echo.
echo [6/5] Installing HeartMuLa and dependencies...
python -m pip install -e .
python -m pip install -r requirements-gui.txt

echo.
echo ========================================
echo Verifying Installation...
echo ========================================
echo.

python verify_installation.py

echo.
echo ========================================
echo Fix Complete!
echo ========================================
echo.
echo If verification passed, you can now run: start.bat
echo.
pause
