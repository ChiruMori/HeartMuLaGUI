# HeartMuLa GUI User Guide

## Quick Start

### 1. Installation

Make sure you have Python 3.10 installed and the virtual environment set up:

```bash
# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install HeartMuLa
pip install -e .
```

### 2. Download Models

Download the required models using one of these methods:

**Using Hugging Face:**
```bash
hf download --local-dir './ckpt' 'HeartMuLa/HeartMuLaGen'
hf download --local-dir './ckpt/HeartMuLa-oss-3B' 'HeartMuLa/HeartMuLa-oss-3B'
hf download --local-dir './ckpt/HeartCodec-oss' 'HeartMuLa/HeartCodec-oss'
```

**Using ModelScope:**
```bash
modelscope download --model 'HeartMuLa/HeartMuLaGen' --local_dir './ckpt'
modelscope download --model 'HeartMuLa/HeartMuLa-oss-3B' --local_dir './ckpt/HeartMuLa-oss-3B'
modelscope download --model 'HeartMuLa/HeartCodec-oss' --local_dir './ckpt/HeartCodec-oss'
```

### 3. Launch the GUI

Simply double-click `02_START_GUI.bat` or run:
```bash
02_START_GUI.bat
```

---

## Using the GUI

### Music Generation Tab

#### 1. Select Tags
- Check the boxes for the musical tags you want
- Tags include instruments (piano, guitar, drums), moods (happy, sad, energetic), and genres (pop, rock, jazz)
- Selected tags appear below the checkbox grid
- Multiple tags can be selected and will be combined with commas

#### 2. Enter Lyrics
- Type or paste your lyrics in the text area
- Use standard song structure markers: `[Intro]`, `[Verse]`, `[Chorus]`, `[Bridge]`, `[Outro]`
- Example format:
  ```
  [Intro]

  [Verse]
  Your lyrics here
  More lyrics here

  [Chorus]
  Chorus lyrics here
  ```

#### 3. Set Generation Parameters

- **Max Audio Length (ms)**: Duration of generated music
  - 30000 = 30 seconds
  - 60000 = 1 minute
  - 240000 = 4 minutes (maximum recommended)

- **Top-K**: Controls sampling diversity (1-100)
  - Lower values (20-30): More predictable, coherent
  - Higher values (50-80): More creative, varied
  - Default: 50

- **Temperature**: Controls randomness (0.1-2.0)
  - Lower values (0.5-0.8): More conservative
  - Higher values (1.2-1.5): More experimental
  - Default: 1.0

- **CFG Scale**: Classifier-free guidance strength (1.0-3.0)
  - Lower values (1.0-1.5): More creative freedom
  - Higher values (2.0-3.0): Stricter adherence to tags/lyrics
  - Default: 1.5

- **Output Filename**: Base name for the output file (without extension)
  - Timestamp will be added automatically if enabled in Settings

#### 4. Generate or Add to Batch

- **Generate Now**: Immediately generates music with current settings
- **Add to Batch**: Saves current configuration to batch queue for later processing
- **Clear Form**: Resets all fields to default values

---

### Batch Queue Tab

Process multiple songs in sequence without manual intervention.

#### Features:
- **View Queue**: See all queued items with tags, length, and filename
- **Remove Selected**: Delete selected items from queue
- **Clear All**: Empty the entire batch queue
- **Start Batch Processing**: Generate all queued items sequentially

#### Progress Tracking:
- Progress bar shows current batch completion
- Status log displays real-time updates
- Each file is saved with timestamp (if enabled)

---

### Settings Tab

#### Model Configuration:
- **Model Path**: Location of downloaded model files (default: `./ckpt`)
- **Output Folder**: Where generated MP3 files are saved (default: `./output`)
- **Model Version**: Choose between 3B or 7B (when available)
- **Device**: Select `cuda` for GPU or `cpu` for CPU processing
- **Data Type**: 
  - `bfloat16`: Recommended for most GPUs (best balance)
  - `float16`: Alternative for older GPUs
  - `float32`: Highest quality but slowest

#### Options:
- **Auto-load model on startup**: Automatically loads model when GUI starts
- **Add timestamp to output files**: Appends date/time to filenames (recommended)

#### Actions:
- **Load Model**: Manually load the model into memory (required before generation)
- **Save Settings**: Saves current configuration to `gui_config.json`

---

## Output Files

Generated files are saved as MP3 format in the output folder with naming pattern:
```
<filename>_<YYYYMMDD_HHMMSS>.mp3
```

Example: `output_20260120_143052.mp3`

---

## Status Log

The status log at the bottom shows:
- Model loading progress
- Generation status
- Batch processing updates
- Error messages
- File save locations

---

## Tips for Best Results

### For 8GB VRAM Systems:
1. Use `bfloat16` data type
2. Keep max audio length under 60 seconds for single generations
3. Close other GPU-intensive applications
4. Consider using FP8 quantization (see optimization guide)

### Tag Selection:
- Combine 3-5 tags for best results
- Mix instrument + mood + genre for coherent output
- Example: `piano,romantic,ballad,slow,emotional`

### Lyrics:
- Use clear song structure markers
- Keep verses and choruses distinct
- Add breathing room with empty lines between sections

### Parameters:
- Start with defaults and adjust based on results
- Lower temperature for more predictable output
- Higher CFG scale for stronger tag adherence

---

## Troubleshooting

### Model Won't Load
- Verify model path contains all required files
- Check CUDA is available: `python -c "import torch; print(torch.cuda.is_available())"`
- Try switching to CPU device (slower but more compatible)

### Out of Memory Errors
- Reduce max audio length
- Switch to `float16` or enable FP8 quantization
- Close other applications
- Restart the GUI

### Generation is Slow
- This is normal - RTF ≈ 1.0 (real-time factor)
- 30 seconds of audio takes ~30 seconds to generate
- Consider FP8 quantization for faster generation

### No Sound in Output
- Check output folder path is correct
- Verify file was created
- Try playing with different media player

---

## Keyboard Shortcuts

- `Ctrl+S`: Save settings (when in Settings tab)
- `Ctrl+Q`: Quit application
- `Ctrl+L`: Clear log window

---

## Support

For issues or questions:
- GitHub: https://github.com/HeartMuLa/heartlib
- Email: heartmula.ai@gmail.com
- Discord: https://discord.gg/BKXF5FgH
