@echo off
echo ========================================
echo Environment Diagnostic Check
echo ========================================
echo.

echo Checking venv activation...
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: venv not found!
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo.
echo ========================================
echo Python Information
echo ========================================
python --version
echo.
echo Python executable location:
where python
echo.

echo ========================================
echo PyTorch Check
echo ========================================
python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}'); print(f'Install path: {torch.__file__}')"

echo.
echo ========================================
echo Installed Packages
echo ========================================
pip list | findstr /i "torch triton bitsandbytes transformers"

echo.
echo ========================================
echo.
echo If CUDA shows as False above, your PyTorch is not CUDA-enabled.
echo Run fix_cuda_issue.bat to reinstall with CUDA support.
echo.
pause
