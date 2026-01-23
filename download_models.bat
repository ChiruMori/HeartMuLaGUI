@echo off
echo ========================================
echo HeartMuLa - Model Downloader
echo ========================================
echo.
echo This will download the required models from Hugging Face.
echo Total download size: ~10-12 GB
echo.
echo Models to download:
echo - HeartMuLaGen (tokenizer and config)
echo - HeartMuLa-oss-3B (main model)
echo - HeartCodec-oss (audio codec)
echo.
echo Download location: ./ckpt
echo.
pause

REM Check if venv exists and activate it
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo WARNING: Virtual environment not found. Using system Python.
    echo It's recommended to run 01_SETUP_GUI.bat first.
    echo.
    pause
)

REM Check if huggingface-cli is installed
python -c "import huggingface_hub" 2>nul
if errorlevel 1 (
    echo Installing huggingface_hub...
    python -m pip install huggingface_hub
)

echo.
echo ========================================
echo Checking existing models...
echo ========================================

set MODELS_EXIST=0

if exist "ckpt\HeartCodec-oss" (
    echo [OK] HeartCodec-oss found
    set /a MODELS_EXIST+=1
) else (
    echo [ ] HeartCodec-oss not found
)

if exist "ckpt\HeartMuLa-oss-3B" (
    echo [OK] HeartMuLa-oss-3B found
    set /a MODELS_EXIST+=1
) else (
    echo [ ] HeartMuLa-oss-3B not found
)

if exist "ckpt\tokenizer.json" (
    echo [OK] tokenizer.json found
    set /a MODELS_EXIST+=1
) else (
    echo [ ] tokenizer.json not found
)

if exist "ckpt\gen_config.json" (
    echo [OK] gen_config.json found
    set /a MODELS_EXIST+=1
) else (
    echo [ ] gen_config.json not found
)

echo.
if %MODELS_EXIST%==4 (
    echo All models appear to be present!
    echo.
    choice /C YN /M "Do you want to re-download anyway"
    if errorlevel 2 (
        echo Skipping download.
        goto :end
    )
)

echo.
echo ========================================
echo Downloading models from Hugging Face...
echo ========================================
echo.
echo This may take 10-30 minutes depending on your internet speed.
echo.

REM Create ckpt directory if it doesn't exist
if not exist "ckpt" mkdir ckpt

echo [1/3] Downloading HeartMuLaGen (tokenizer and config)...
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='HeartMuLa/HeartMuLaGen', local_dir='./ckpt', local_dir_use_symlinks=False)"
if errorlevel 1 (
    echo ERROR: Failed to download HeartMuLaGen
    echo.
    echo Troubleshooting:
    echo - Check your internet connection
    echo - Make sure you have enough disk space (~12 GB^)
    echo - Try running: python -m pip install --upgrade huggingface_hub
    pause
    exit /b 1
)

echo.
echo [2/3] Downloading HeartMuLa-oss-3B (main model, ~8 GB)...
echo This is the largest file - please be patient...
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='HeartMuLa/HeartMuLa-RL-oss-3B-20260123', local_dir='./ckpt/HeartMuLa-oss-3B', local_dir_use_symlinks=False)"
if errorlevel 1 (
    echo ERROR: Failed to download HeartMuLa-oss-3B
    pause
    exit /b 1
)

echo.
echo [3/3] Downloading HeartCodec-oss (audio codec, ~2 GB)...
echo Final download - almost done!
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='HeartMuLa/HeartCodec-oss-20260123', local_dir='./ckpt/HeartCodec-oss', local_dir_use_symlinks=False)"
if errorlevel 1 (
    echo ERROR: Failed to download HeartCodec-oss
    pause
    exit /b 1
)

echo.
echo ========================================
echo Verifying download...
echo ========================================
echo.

if exist "ckpt\HeartCodec-oss" (
    echo [OK] HeartCodec-oss
) else (
    echo [X] HeartCodec-oss MISSING!
)

if exist "ckpt\HeartMuLa-oss-3B" (
    echo [OK] HeartMuLa-oss-3B
) else (
    echo [X] HeartMuLa-oss-3B MISSING!
)

if exist "ckpt\tokenizer.json" (
    echo [OK] tokenizer.json
) else (
    echo [X] tokenizer.json MISSING!
)

if exist "ckpt\gen_config.json" (
    echo [OK] gen_config.json
) else (
    echo [X] gen_config.json MISSING!
)

echo.
echo ========================================
echo Download Complete!
echo ========================================
echo.
echo Models are ready in: ./ckpt
echo.
echo Next step: Launch the GUI
echo   Double-click: start.bat
echo   OR run: python gui_app.py
echo.

:end
pause
