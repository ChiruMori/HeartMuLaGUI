@echo off
echo ========================================
echo Installing FFmpeg for Audio Waveforms
echo ========================================
echo.
echo This will install FFmpeg using winget (Windows Package Manager)
echo FFmpeg enables waveform visualization in the Music Library.
echo.
pause

echo Checking if winget is available...
winget --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: winget not found!
    echo.
    echo Please install FFmpeg manually:
    echo 1. Download from: https://www.gyan.dev/ffmpeg/builds/
    echo 2. Extract to C:\ffmpeg
    echo 3. Add C:\ffmpeg\bin to your PATH environment variable
    echo.
    pause
    exit /b 1
)

echo Installing FFmpeg...
winget install Gyan.FFmpeg

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Please restart the GUI application.
echo Waveforms should now display in the Music Library.
echo.
pause
