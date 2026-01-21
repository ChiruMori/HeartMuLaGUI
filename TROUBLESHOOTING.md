# HeartMuLa GUI - Troubleshooting Guide

## ❌ "Torch not compiled with CUDA enabled"

This is the most common error and means PyTorch was installed without CUDA support.

### Quick Fix

```bash
# Run the automated fix script
fix_cuda_issue.bat
```

This will:
1. Remove the old venv
2. Create new venv with Python 3.10
3. Install CUDA-enabled PyTorch
4. Install Triton
5. Install all dependencies
6. Verify the installation

### Manual Fix

If the automated script doesn't work:

```bash
# 1. Delete venv folder
rmdir /s /q venv

# 2. Create new venv with Python 3.10
D:\AI\heartlib\drivers\310\python.exe -m venv venv

# 3. Activate venv
venv\Scripts\activate

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install PyTorch with CUDA 12.1
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 6. Install Triton
python -m pip install D:\AI\heartlib\drivers\triton-2.1.0-cp310-cp310-win_amd64.whl

# 7. Install HeartMuLa
python -m pip install -e .

# 8. Install GUI dependencies
python -m pip install -r requirements-gui.txt

# 9. Verify installation
python verify_installation.py
```

### Verification

After fixing, verify CUDA is available:

```python
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

Should output: `CUDA available: True`

---

## ⚠️ Wrong Python Version

### Error: "Python 3.X detected, Python 3.10 required"

The setup script is configured to use Python 3.10 from:
```
D:\AI\heartlib\drivers\310\python.exe
```

**Solutions:**

1. **Check if Python 3.10 exists at that location:**
   ```bash
   D:\AI\heartlib\drivers\310\python.exe --version
   ```

2. **If missing, update the path in 01_SETUP_GUI.bat:**
   - Open `01_SETUP_GUI.bat`
   - Change line 8: `set PYTHON310_PATH=<your_python_3.10_path>`

3. **Or install Python 3.10 to the expected location**

---

## 🔧 Triton Installation Issues

### Error: "Failed to install Triton"

**Solution 1: Use local wheel file**
```bash
python -m pip install D:\AI\heartlib\drivers\triton-2.1.0-cp310-cp310-win_amd64.whl
```

**Solution 2: Install from PyPI**
```bash
python -m pip install triton
```

**Note:** Triton is optional but recommended for performance.

---

## 💾 Out of Memory Errors

### Error: "CUDA out of memory"

**Solutions:**

1. **Enable FP8 Quantization** (most effective)
   - Settings tab → Check "Enable FP8 Quantization"
   - Reload model
   - Reduces VRAM from 6-7 GB to 3-4 GB

2. **Reduce audio length**
   - Set Max Audio Length to 30000 (30 seconds) or less

3. **Use float16 instead of bfloat16**
   - Settings → Data Type → float16

4. **Close other GPU applications**
   - Close browsers, games, other AI tools

5. **Restart the GUI**
   - Sometimes memory isn't fully released

---

## 🐌 Slow Generation

### Normal Speed
- RTF ≈ 1.0 (30 seconds audio = 30 seconds generation)
- First generation is slower (model warmup)

### Speed Improvements

1. **Enable FP8 Quantization**
   - 10-30% faster
   - Settings → Enable FP8

2. **Check GPU usage**
   ```bash
   nvidia-smi
   ```
   - Should show high GPU utilization during generation

3. **Ensure CUDA is being used**
   ```python
   python verify_installation.py
   ```

---

## 📁 Model Files Not Found

### Error: "Expected to find checkpoint at..."

**Check model structure:**
```
ckpt/
├── HeartCodec-oss/
├── HeartMuLa-oss-3B/
├── gen_config.json
└── tokenizer.json
```

**Download missing files:**
```bash
venv\Scripts\activate

# Download all models
hf download --local-dir './ckpt' 'HeartMuLa/HeartMuLaGen'
hf download --local-dir './ckpt/HeartMuLa-oss-3B' 'HeartMuLa/HeartMuLa-oss-3B'
hf download --local-dir './ckpt/HeartCodec-oss' 'HeartMuLa/HeartCodec-oss'
```

---

## 🖥️ GUI Won't Start

### Error: "No module named 'tkinter'"

Tkinter should be included with Python. If missing:

**Windows:**
- Reinstall Python 3.10 with "tcl/tk and IDLE" option checked

**Linux:**
```bash
sudo apt-get install python3-tk
```

### Error: "No module named 'heartlib'"

```bash
venv\Scripts\activate
python -m pip install -e .
```

---

## 🔴 BitsAndBytes Issues

### Warning: "bitsandbytes not installed"

FP8 quantization won't be available.

**Install:**
```bash
venv\Scripts\activate
python -m pip install bitsandbytes
```

**Windows-specific issues:**
```bash
python -m pip install bitsandbytes-windows
```

---

## 🎵 No Sound in Output

### File created but no audio

1. **Check file size**
   - Should be > 100 KB
   - If 0 KB, generation failed

2. **Try different media player**
   - VLC Media Player
   - Windows Media Player
   - Browser

3. **Check output path**
   - Default: `./output/`
   - Verify in Settings tab

---

## 🔄 Model Loading Hangs

### Stuck at "Loading model..."

**Normal behavior:**
- First load: 2-5 minutes
- With FP8: 3-7 minutes (quantization overhead)

**If stuck > 10 minutes:**

1. **Check Task Manager**
   - Is Python using GPU?
   - Is memory increasing?

2. **Check for errors in log window**

3. **Restart and try without FP8**
   - Uncheck FP8 in Settings
   - Load model again

4. **Try CPU mode** (slow but works)
   - Settings → Device → cpu

---

## 🔍 Verification Checklist

Run the verification script:
```bash
venv\Scripts\activate
python verify_installation.py
```

**Critical checks:**
- ✓ Python 3.10
- ✓ PyTorch with CUDA
- ✓ Transformers
- ✓ Tkinter

**Optional but recommended:**
- ✓ Triton
- ✓ BitsAndBytes
- ✓ Model files

---

## 📊 System Information

### Check CUDA availability
```python
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
print(f"Device name: {torch.cuda.get_device_name(0)}")
```

### Check VRAM
```bash
nvidia-smi
```

### Check Python packages
```bash
pip list
```

---

## 🆘 Still Having Issues?

### Collect diagnostic information:

1. **Run verification:**
   ```bash
   python verify_installation.py > diagnostic.txt
   ```

2. **Check PyTorch:**
   ```bash
   python -c "import torch; print(torch.__version__, torch.cuda.is_available())" >> diagnostic.txt
   ```

3. **List packages:**
   ```bash
   pip list >> diagnostic.txt
   ```

4. **Share diagnostic.txt** when asking for help

### Get help:
- Discord: https://discord.gg/BKXF5FgH
- GitHub Issues: https://github.com/HeartMuLa/heartlib/issues
- Email: heartmula.ai@gmail.com

---

## 🔧 Common Solutions Summary

| Problem | Solution |
|---------|----------|
| CUDA not available | Run `fix_cuda_issue.bat` |
| Out of memory | Enable FP8 quantization |
| Slow generation | Enable FP8, check GPU usage |
| Model not found | Download models with `hf download` |
| GUI won't start | Check tkinter, reinstall Python |
| Wrong Python version | Use Python 3.10 from drivers/310 |
| Triton missing | Install from local wheel or PyPI |
| BitsAndBytes missing | `pip install bitsandbytes` |

---

## 📝 Best Practices

1. **Always use the provided scripts:**
   - `01_SETUP_GUI.bat` for initial setup
   - `fix_cuda_issue.bat` for CUDA problems
   - `verify_installation.py` to check everything

2. **Keep venv clean:**
   - Don't mix pip and conda
   - Don't install packages globally
   - Always activate venv first

3. **Check before asking for help:**
   - Run verification script
   - Check log window in GUI
   - Review this troubleshooting guide

4. **For 8GB VRAM:**
   - Always enable FP8
   - Keep audio length ≤ 60 seconds
   - Close other GPU apps
