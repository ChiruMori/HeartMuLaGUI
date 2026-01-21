@echo off
echo ========================================
echo HeartMuLa GUI Setup Script
echo ========================================
echo.

REM Set Python 3.10 path
set PYTHON310_PATH=D:\AI\heartlib\drivers\310\python.exe
set TRITON_URL=https://huggingface.co/madbuda/triton-windows-builds/resolve/main/triton-2.1.0-cp310-cp310-win_amd64.whl

REM Check if Python 3.10 exists at specified location
if not exist "%PYTHON310_PATH%" (
    echo ERROR: Python 3.10 not found at %PYTHON310_PATH%
    echo Please ensure Python 3.10 is installed at the correct location
    pause
    exit /b 1
)

REM Check if venv exists
if exist "venv\" (
    echo.
    echo Virtual environment already exists.
    set /p RECREATE="Do you want to recreate it? (y/N): "
    if /i "%RECREATE%"=="y" (
        echo Removing old virtual environment...
        rmdir /s /q venv
    ) else (
        goto :skip_venv
    )
)

echo.
echo [1/6] Creating virtual environment with Python 3.10...
"%PYTHON310_PATH%" -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

:skip_venv
echo.
echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [3/6] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [4/6] Installing PyTorch with CUDA support...
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
if errorlevel 1 (
    echo ERROR: Failed to install PyTorch with CUDA
    pause
    exit /b 1
)

echo.
echo [5/6] Installing Triton...
echo Downloading Triton from Hugging Face...
python -m pip install "%TRITON_URL%"
if errorlevel 1 (
    echo WARNING: Failed to install Triton from Hugging Face
    echo Trying to install from PyPI...
    python -m pip install triton
)

echo.
echo [6/6] Installing HeartMuLa and GUI dependencies...
python -m pip install -e .
if errorlevel 1 (
    echo ERROR: Failed to install HeartMuLa
    pause
    exit /b 1
)

python -m pip install -r requirements-gui.txt
if errorlevel 1 (
    echo WARNING: Some optional dependencies failed to install
    echo The GUI will still work but FP8 optimization may not be available
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo The Python environment is ready!
echo.
echo ========================================
echo Model Download
echo ========================================
echo.
echo The models (~10-12 GB) need to be downloaded from Hugging Face.
echo.

REM Check if models already exist
if exist "ckpt\HeartCodec-oss" if exist "ckpt\HeartMuLa-oss-3B" if exist "ckpt\tokenizer.json" (
    echo Models appear to be already downloaded in ./ckpt
    echo.
    goto :skip_download
)

echo Models not found. Would you like to download them now?
echo This will take 10-30 minutes depending on your internet speed.
echo.
choice /C YN /M "Download models now"
if errorlevel 2 (
    echo.
    echo Skipping model download.
    echo To download later, run: download_models.bat
    echo.
    goto :skip_download
)

echo.
echo Starting model download...
call download_models.bat
goto :end

:skip_download
echo.
echo ========================================
echo Next Steps
echo ========================================
echo.
echo 1. If models are not downloaded yet, run:
echo    download_models.bat
echo.
echo 2. Launch the GUI:
echo    Double-click: 02_START_GUI.bat
echo    OR run: python gui_app.py
echo.
echo For help, see:
echo - GUI_README.md (Quick start guide)
echo - GUI_USER_GUIDE.md (Detailed usage)
echo - FP8_OPTIMIZATION_GUIDE.md (Performance optimization)
echo.

:end
pause
