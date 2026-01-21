# HeartMuLa GUI Application

A user-friendly graphical interface for HeartMuLa music generation with batch processing and FP8 optimization support.

## Features

✨ **User-Friendly Interface**
- Tag selection with checkboxes (40+ musical tags)
- Multi-line lyrics editor with song structure support
- Real-time parameter adjustment with helpful hints
- Status log and progress tracking

🎵 **Music Generation**
- Single song generation
- Batch queue processing
- Custom output filenames with automatic timestamps
- Configurable audio length, temperature, and other parameters

⚡ **Performance Optimization**
- **FP8 Quantization Support**: Reduces VRAM usage by ~50%
- Automatic detection of bitsandbytes library
- Optimized for 8GB VRAM systems
- Real-time generation monitoring

📁 **Batch Processing**
- Queue multiple songs with different settings
- View and manage batch queue
- Progress tracking with status updates
- Automatic file naming with timestamps

## Quick Start

### 1. Setup Environment

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install HeartMuLa
pip install -e .

# Install optional GUI dependencies (recommended)
pip install -r requirements-gui.txt
```

### 2. Download Models

```bash
# Using Hugging Face
hf download --local-dir './ckpt' 'HeartMuLa/HeartMuLaGen'
hf download --local-dir './ckpt/HeartMuLa-oss-3B' 'HeartMuLa/HeartMuLa-oss-3B'
hf download --local-dir './ckpt/HeartCodec-oss' 'HeartMuLa/HeartCodec-oss'
```

### 3. Launch GUI

**Windows:**
```bash
# Simply double-click 02_START_GUI.bat
# OR run from command line:
02_START_GUI.bat
```

**Manual Launch:**
```bash
venv\Scripts\activate
python gui_app.py
```

## Usage Guide

### First Time Setup

1. **Launch the application** using `02_START_GUI.bat`
2. **Go to Settings tab**
3. **Configure paths:**
   - Model Path: `./ckpt` (where you downloaded models)
   - Output Folder: `./output` (where MP3 files will be saved)
4. **Enable FP8 Quantization** (if you have 8GB VRAM)
5. **Click "Load Model"** - this takes 2-5 minutes
6. **Wait for "Model: Loaded"** status (green)

### Generating Music

#### Music Generation Tab

1. **Select Tags:**
   - Check boxes for desired musical characteristics
   - Combine instruments + mood + genre for best results
   - Example: `piano`, `romantic`, `ballad`, `slow`

2. **Enter Lyrics:**
   ```
   [Intro]

   [Verse]
   Your lyrics here
   More lyrics here

   [Chorus]
   Chorus lyrics here
   
   [Outro]
   Ending lyrics
   ```

3. **Set Parameters:**
   - **Max Audio Length**: 30000 ms = 30 seconds (recommended for 8GB VRAM)
   - **Top-K**: 50 (default, range 1-100)
   - **Temperature**: 1.0 (default, range 0.1-2.0)
   - **CFG Scale**: 1.5 (default, range 1.0-3.0)
   - **Output Filename**: Base name (timestamp added automatically)

4. **Generate:**
   - **Generate Now**: Create immediately
   - **Add to Batch**: Queue for later batch processing

### Batch Processing

#### Batch Queue Tab

1. Add multiple songs from the Generation tab
2. Review queue in the list view
3. Remove unwanted items if needed
4. Click **"Start Batch Processing"**
5. Monitor progress bar and status log

All files are saved to the output folder with timestamps.

## Settings

### Model Configuration

- **Model Path**: Location of downloaded models (default: `./ckpt`)
- **Output Folder**: Where generated files are saved (default: `./output`)
- **Model Version**: 3B (7B when available)
- **Device**: `cuda` for GPU, `cpu` for CPU
- **Data Type**: 
  - `bfloat16`: Recommended (best balance)
  - `float16`: Alternative for older GPUs
  - `float32`: Highest quality, slowest

### Optimization

- **Enable FP8 Quantization**: Reduces VRAM by ~50% (requires bitsandbytes)
  - ✓ Recommended for 8GB VRAM systems
  - ✓ 10-30% faster generation
  - ✓ Minimal quality loss

### Options

- **Auto-load model on startup**: Automatically loads model when GUI starts
- **Add timestamp to output files**: Appends `YYYYMMDD_HHMMSS` to filenames

## FP8 Quantization (8GB VRAM Optimization)

### Installation

```bash
pip install bitsandbytes
```

### Benefits

- **Memory**: 6-7 GB → 3-4 GB (50% reduction)
- **Speed**: 10-30% faster generation
- **Quality**: Minimal perceptual difference

### Usage

1. Install bitsandbytes (see above)
2. Launch GUI - it auto-detects the library
3. Go to Settings tab
4. Check "Enable FP8 Quantization"
5. Load model normally

The GUI will show:
- ✓ bitsandbytes available (green) - FP8 enabled
- ✗ bitsandbytes not installed (orange) - FP8 disabled

### Testing & Benchmarking

```bash
# Run optimization script with benchmark
python optimize_fp8.py --model_path ./ckpt --version 3B --benchmark
```

See `FP8_OPTIMIZATION_GUIDE.md` for detailed information.

## File Structure

```
heartlib/
├── gui_app.py                  # Main GUI application
├── start.bat                   # Windows launcher script
├── optimize_fp8.py             # FP8 optimization script
├── requirements-gui.txt        # GUI dependencies
├── GUI_USER_GUIDE.md          # Detailed user guide
├── FP8_OPTIMIZATION_GUIDE.md  # FP8 optimization guide
├── gui_config.json            # Settings (auto-generated)
├── output/                    # Generated music files
│   └── *.mp3
└── ckpt/                      # Model files
    ├── HeartCodec-oss/
    ├── HeartMuLa-oss-3B/
    ├── gen_config.json
    └── tokenizer.json
```

## Output Files

Generated files follow this naming pattern:
```
<filename>_<YYYYMMDD_HHMMSS>.mp3
```

Example: `mysong_20260120_143052.mp3`

Files are saved as 48kHz MP3 format in the configured output folder.

## Tips & Best Practices

### For 8GB VRAM Systems

✓ Enable FP8 quantization  
✓ Use `bfloat16` data type  
✓ Keep audio length ≤ 60 seconds  
✓ Close other GPU applications  
✓ Generate one song at a time initially  

### Tag Selection

- Combine 3-5 tags for coherent results
- Mix categories: instrument + mood + genre
- Good: `piano,romantic,ballad,slow,emotional`
- Avoid: Too many conflicting tags

### Lyrics Tips

- Use clear structure markers: `[Intro]`, `[Verse]`, `[Chorus]`, `[Bridge]`, `[Outro]`
- Add empty lines between sections
- Keep verses and choruses distinct
- Natural language works best

### Parameter Tuning

- **Temperature**:
  - Lower (0.5-0.8): More predictable, conservative
  - Higher (1.2-1.5): More creative, experimental
  
- **Top-K**:
  - Lower (20-30): More coherent
  - Higher (50-80): More varied
  
- **CFG Scale**:
  - Lower (1.0-1.5): More creative freedom
  - Higher (2.0-3.0): Stricter tag adherence

## Troubleshooting

### Model Won't Load

**Check model path:**
```bash
dir ckpt
# Should show: HeartCodec-oss, HeartMuLa-oss-3B, gen_config.json, tokenizer.json
```

**Verify CUDA:**
```bash
python -c "import torch; print(torch.cuda.is_available())"
# Should print: True
```

**Try CPU mode:**
- Go to Settings → Device → Select `cpu`
- Note: Much slower but more compatible

### Out of Memory

1. Enable FP8 quantization in Settings
2. Reduce max audio length to 30 seconds
3. Switch to `float16` data type
4. Close other applications
5. Restart GUI application

### Generation is Slow

- **Normal**: RTF ≈ 1.0 (30s audio = 30s generation)
- **With FP8**: RTF ≈ 0.8-0.9 (20-30% faster)
- **First generation**: Slower due to model warmup

### GUI Won't Start

**Check Python version:**
```bash
python --version
# Should be 3.10.x
```

**Check tkinter:**
```bash
python -c "import tkinter"
# Should not error
```

**Check virtual environment:**
```bash
# Make sure venv is activated
venv\Scripts\activate
```

### No Sound in Output

- Verify output folder path is correct
- Check file was created in output folder
- Try different media player (VLC, Windows Media Player)
- Check file size (should be > 100 KB)

## Keyboard Shortcuts

- `Ctrl+Q`: Quit application
- `Ctrl+L`: Clear log window (when focused)

## Performance Metrics

### Without FP8 (BF16)
- VRAM: ~6-7 GB
- Speed: RTF ≈ 1.0
- 30s audio: ~30s generation

### With FP8
- VRAM: ~3-4 GB ✓
- Speed: RTF ≈ 0.8-0.9 ✓
- 30s audio: ~24-27s generation ✓

## Support & Resources

- **User Guide**: `GUI_USER_GUIDE.md`
- **FP8 Guide**: `FP8_OPTIMIZATION_GUIDE.md`
- **GitHub**: https://github.com/HeartMuLa/heartlib
- **Discord**: https://discord.gg/BKXF5FgH
- **Email**: heartmula.ai@gmail.com

## Known Limitations

- First model load takes 2-5 minutes
- Generation is real-time (RTF ≈ 1.0 without optimization)
- Maximum recommended audio length: 240 seconds (4 minutes)
- Batch processing is sequential (not parallel)
- FP8 requires NVIDIA GPU with CUDA

## Future Enhancements

- Streaming inference for longer audio
- Parallel batch processing
- Audio preview before saving
- Preset management
- Reference audio conditioning (when available)
- Export to other formats (WAV, FLAC)

## License

Apache 2.0 - See LICENSE file

## Acknowledgments

Built on top of HeartMuLa by the HeartMuLa team.  
GUI and optimization by community contributors.
