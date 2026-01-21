# HeartMuLa GUI - Quick Start Guide

## ⚠️ IMPORTANT: Python 3.10 Required

This project **requires Python 3.10** with CUDA-enabled PyTorch.

## 🚀 Installation (5 minutes + model download)

### Step 1: Setup
```bash
# Run the setup script (uses Python 3.10 from D:\AI\heartlib\drivers\310)
01_SETUP_GUI.bat
```

The setup will:
1. Create Python 3.10 virtual environment
2. Install CUDA-enabled PyTorch
3. Install all dependencies
4. **Ask if you want to download models automatically** (~10-12 GB, 10-30 min)

**If you get "Torch not compiled with CUDA enabled" error:**
```bash
# Run the fix script
fix_cuda_issue.bat
```

### Step 2: Download Models (if not done during setup)

**Option A: Automated (Recommended)**
```bash
# Run the download script
download_models.bat
```

**Option B: Manual Download**
```bash
# Activate environment
venv\Scripts\activate

# Using Hugging Face CLI
hf download --local-dir './ckpt' 'HeartMuLa/HeartMuLaGen'
hf download --local-dir './ckpt/HeartMuLa-oss-3B' 'HeartMuLa/HeartMuLa-oss-3B'
hf download --local-dir './ckpt/HeartCodec-oss' 'HeartMuLa/HeartCodec-oss'
```

### Step 3: Verify Installation (Optional)
```bash
# Activate venv
venv\Scripts\activate

# Run verification
python verify_installation.py
```

### Step 4: Launch
```bash
# Double-click 02_START_GUI.bat
# OR
02_START_GUI.bat
```

---

## 🎵 First Generation (2 minutes)

1. **Settings Tab** → Click "Load Model" → Wait for green "Model: Loaded"
2. **Generation Tab** → Select tags (e.g., `piano`, `happy`, `pop`)
3. Enter lyrics:
   ```
   [Verse]
   Your lyrics here
   
   [Chorus]
   Chorus lyrics here
   ```
4. Click **"Generate Now"**
5. Find your MP3 in `./output/` folder

---

## ⚡ 8GB VRAM Optimization

### Enable FP8 (50% less memory, 20% faster)

1. **Settings Tab**
2. Check ✓ **"Enable FP8 Quantization"**
3. Click **"Load Model"**

**Before FP8:** 6-7 GB VRAM  
**After FP8:** 3-4 GB VRAM ✓

---

## 📋 Common Parameters

| Parameter | Recommended | Range | Effect |
|-----------|-------------|-------|--------|
| Max Length | 30000 ms | 10000-240000 | Audio duration |
| Top-K | 50 | 20-80 | Creativity |
| Temperature | 1.0 | 0.5-1.5 | Randomness |
| CFG Scale | 1.5 | 1.0-3.0 | Tag adherence |

---

## 🎹 Popular Tag Combinations

**Romantic Ballad:**
`piano,romantic,ballad,slow,emotional`

**Upbeat Pop:**
`synthesizer,happy,pop,energetic,dance`

**Chill Jazz:**
`saxophone,jazz,calm,relaxing,smooth`

**Rock Energy:**
`guitar,drums,rock,energetic,electric`

**K-Pop:**
`kpop,happy,dance,energetic,synthesizer`

---

## 🔧 Troubleshooting

### Model won't load
- Check `./ckpt` folder has all files
- Try Settings → Device → `cpu`

### Out of memory
- Enable FP8 in Settings
- Reduce max length to 30000
- Close other apps

### Slow generation
- Normal: 30s audio = 30s generation
- Enable FP8 for 20% speedup

---

## 📚 Documentation

- **GUI_README.md** - Complete guide
- **GUI_USER_GUIDE.md** - Detailed usage
- **FP8_OPTIMIZATION_GUIDE.md** - Performance tips

---

## 💡 Tips

✓ Start with default parameters  
✓ Use 3-5 tags maximum  
✓ Structure lyrics with `[Verse]`, `[Chorus]` markers  
✓ Enable FP8 if you have 8GB VRAM  
✓ Add to batch for multiple songs  

---

## 🆘 Support

- Discord: https://discord.gg/BKXF5FgH
- GitHub: https://github.com/HeartMuLa/heartlib
- Email: heartmula.ai@gmail.com
