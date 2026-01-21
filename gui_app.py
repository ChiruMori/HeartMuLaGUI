import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import os
import sys
from datetime import datetime
import threading
import json
from pathlib import Path
import torch
from heartlib import HeartMuLaGenPipeline
from PIL import Image, ImageTk

try:
    from transformers import BitsAndBytesConfig
    BITSANDBYTES_AVAILABLE = True
except ImportError:
    BITSANDBYTES_AVAILABLE = False
    BitsAndBytesConfig = None


THEMES = {
    "Dark Blue/Grey": {
        "bg": "#1e2838",
        "fg": "#e0e6ed",
        "select_bg": "#2d4263",
        "select_fg": "#ffffff",
        "button_bg": "#3a5a7a",
        "button_fg": "#ffffff",
        "entry_bg": "#2a3f5f",
        "entry_fg": "#e0e6ed",
        "frame_bg": "#1e2838",
        "accent": "#4a90e2",
        "progress_bg": "#2a3f5f",
        "progress_fg": "#4a90e2",
        "selected_tags_color": "#dcadf8"
    },
    "Dark": {
        "bg": "#1a1a1a",
        "fg": "#e0e0e0",
        "select_bg": "#2d2d2d",
        "select_fg": "#ffffff",
        "button_bg": "#3a3a3a",
        "button_fg": "#ffffff",
        "entry_bg": "#252525",
        "entry_fg": "#e0e0e0",
        "frame_bg": "#1a1a1a",
        "accent": "#0078d4",
        "progress_bg": "#252525",
        "progress_fg": "#0078d4",
        "selected_tags_color": "#dcadf8"
    },
    "Light": {
        "bg": "#f5f5f5",
        "fg": "#1a1a1a",
        "select_bg": "#e0e0e0",
        "select_fg": "#000000",
        "button_bg": "#d0d0d0",
        "button_fg": "#000000",
        "entry_bg": "#ffffff",
        "entry_fg": "#1a1a1a",
        "frame_bg": "#f5f5f5",
        "accent": "#0078d4",
        "progress_bg": "#e0e0e0",
        "progress_fg": "#0078d4",
        "selected_tags_color": "#9966cc"
    },
    "High Contrast Dark": {
        "bg": "#000000",
        "fg": "#ffffff",
        "select_bg": "#1a1a1a",
        "select_fg": "#ffff00",
        "button_bg": "#1a1a1a",
        "button_fg": "#ffffff",
        "entry_bg": "#0a0a0a",
        "entry_fg": "#ffffff",
        "frame_bg": "#000000",
        "accent": "#00ff00",
        "progress_bg": "#1a1a1a",
        "progress_fg": "#00ff00",
        "selected_tags_color": "#ff00ff"
    },
    "High Contrast Light": {
        "bg": "#ffffff",
        "fg": "#000000",
        "select_bg": "#ffff00",
        "select_fg": "#000000",
        "button_bg": "#e0e0e0",
        "button_fg": "#000000",
        "entry_bg": "#ffffff",
        "entry_fg": "#000000",
        "frame_bg": "#ffffff",
        "accent": "#0000ff",
        "progress_bg": "#e0e0e0",
        "progress_fg": "#0000ff",
        "selected_tags_color": "#8800ff"
    },
    "Ocean Blue": {
        "bg": "#0d1b2a",
        "fg": "#e0f4ff",
        "select_bg": "#1b3a52",
        "select_fg": "#ffffff",
        "button_bg": "#2a5a7a",
        "button_fg": "#ffffff",
        "entry_bg": "#1b3a52",
        "entry_fg": "#e0f4ff",
        "frame_bg": "#0d1b2a",
        "accent": "#00b4d8",
        "progress_bg": "#1b3a52",
        "progress_fg": "#00b4d8",
        "selected_tags_color": "#90e0ef"
    },
    "Forest Green": {
        "bg": "#1a2f1a",
        "fg": "#e0ffe0",
        "select_bg": "#2d4a2d",
        "select_fg": "#ffffff",
        "button_bg": "#3a6a3a",
        "button_fg": "#ffffff",
        "entry_bg": "#2d4a2d",
        "entry_fg": "#e0ffe0",
        "frame_bg": "#1a2f1a",
        "accent": "#4ade80",
        "progress_bg": "#2d4a2d",
        "progress_fg": "#4ade80",
        "selected_tags_color": "#86efac"
    },
    "Purple Haze": {
        "bg": "#1a0f2e",
        "fg": "#e8d5ff",
        "select_bg": "#2d1f4a",
        "select_fg": "#ffffff",
        "button_bg": "#4a2f6a",
        "button_fg": "#ffffff",
        "entry_bg": "#2d1f4a",
        "entry_fg": "#e8d5ff",
        "frame_bg": "#1a0f2e",
        "accent": "#a855f7",
        "progress_bg": "#2d1f4a",
        "progress_fg": "#a855f7",
        "selected_tags_color": "#c084fc"
    },
    "Sunset Orange": {
        "bg": "#2e1a0f",
        "fg": "#ffe8d5",
        "select_bg": "#4a2f1f",
        "select_fg": "#ffffff",
        "button_bg": "#6a4a2f",
        "button_fg": "#ffffff",
        "entry_bg": "#4a2f1f",
        "entry_fg": "#ffe8d5",
        "frame_bg": "#2e1a0f",
        "accent": "#fb923c",
        "progress_bg": "#4a2f1f",
        "progress_fg": "#fb923c",
        "selected_tags_color": "#fdba74"
    },
    "Crimson Red": {
        "bg": "#2e0f0f",
        "fg": "#ffd5d5",
        "select_bg": "#4a1f1f",
        "select_fg": "#ffffff",
        "button_bg": "#6a2f2f",
        "button_fg": "#ffffff",
        "entry_bg": "#4a1f1f",
        "entry_fg": "#ffd5d5",
        "frame_bg": "#2e0f0f",
        "accent": "#ef4444",
        "progress_bg": "#4a1f1f",
        "progress_fg": "#ef4444",
        "selected_tags_color": "#fca5a5"
    }
}


class HeartMuLaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HeartMuLa Music Generator")
        self.root.geometry("1200x950")
        
        self.batch_queue = []
        self.pipe = None
        self.is_generating = False
        self.current_theme = "Dark Blue/Grey"
        
        self.available_tags = [
            "piano", "guitar", "drums", "bass", "synthesizer", "violin", "saxophone",
            "happy", "sad", "energetic", "calm", "romantic", "melancholic", "upbeat",
            "pop", "rock", "jazz", "classical", "electronic", "hip-hop", "country",
            "kpop", "jpop", "ballad", "dance", "folk", "blues", "reggae",
            "wedding", "party", "relaxing", "motivational", "nostalgic", "dreamy",
            "fast", "slow", "medium", "acoustic", "electric"
        ]
        
        self.setup_ui()
        self.check_cuda_on_startup()
        self.load_config()
        self.apply_theme(self.current_theme)
        
    def setup_ui(self):
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(0, weight=1)
        
        notebook = ttk.Notebook(main_container)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        generation_frame = ttk.Frame(notebook, padding="10")
        batch_frame = ttk.Frame(notebook, padding="10")
        settings_frame = ttk.Frame(notebook, padding="10")
        info_frame = ttk.Frame(notebook, padding="10")
        
        notebook.add(generation_frame, text="Music Generation")
        notebook.add(batch_frame, text="Batch Queue")
        notebook.add(settings_frame, text="Settings")
        notebook.add(info_frame, text="Info")
        
        self.setup_generation_tab(generation_frame)
        self.setup_batch_tab(batch_frame)
        self.setup_settings_tab(settings_frame)
        self.setup_info_tab(info_frame)
        
        log_frame = ttk.LabelFrame(main_container, text="Status Log", padding="5")
        log_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        main_container.rowconfigure(1, weight=0)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap=tk.WORD, state='disabled')
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Progress bars frame
        progress_frame = ttk.LabelFrame(main_container, text="Generation Progress", padding="5")
        progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        progress_frame.columnconfigure(1, weight=1)
        
        # Step 1: Prompt Processing
        ttk.Label(progress_frame, text="1. Prompt Processing:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.progress_prompt = ttk.Progressbar(progress_frame, mode='determinate', length=300)
        self.progress_prompt.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        self.progress_prompt_label = ttk.Label(progress_frame, text="0/0")
        self.progress_prompt_label.grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        
        # Step 2: Frame Generation
        ttk.Label(progress_frame, text="2. Frame Generation:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.progress_frames = ttk.Progressbar(progress_frame, mode='determinate', length=300)
        self.progress_frames.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        self.progress_frames_label = ttk.Label(progress_frame, text="0/0")
        self.progress_frames_label.grid(row=1, column=2, sticky=tk.W, padx=(10, 0))
        
        # Step 3: Audio Decoding
        ttk.Label(progress_frame, text="3. Audio Decoding:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.progress_decode = ttk.Progressbar(progress_frame, mode='determinate', length=300)
        self.progress_decode.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        self.progress_decode_label = ttk.Label(progress_frame, text="0/0")
        self.progress_decode_label.grid(row=2, column=2, sticky=tk.W, padx=(10, 0))
        
        self.status_bar = ttk.Label(main_container, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
    def setup_generation_tab(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=0)
        parent.rowconfigure(2, weight=1)
        
        # Top row container for tags and logo
        top_container = ttk.Frame(parent)
        top_container.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N), pady=(0, 10))
        top_container.columnconfigure(0, weight=1)
        top_container.columnconfigure(1, weight=0)
        
        tags_frame = ttk.LabelFrame(top_container, text="Select Tags (comma-separated in output)", padding="10")
        tags_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 10))
        tags_frame.columnconfigure(0, weight=1)
        
        # Logo frame beside tags
        logo_frame = ttk.LabelFrame(top_container, text="", padding="10")
        logo_frame.grid(row=0, column=1, sticky=(tk.N, tk.E))
        
        # Try to load logo.png
        self.logo_label = None
        try:
            logo_path = Path("logo.png")
            if logo_path.exists():
                logo_image = Image.open(logo_path)
                # Resize if needed to fit nicely (max 600x250 as specified)
                logo_image.thumbnail((600, 250), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_image)
                self.logo_label = tk.Label(logo_frame, image=self.logo_photo, bg=THEMES[self.current_theme]["bg"])
                self.logo_label.pack()
            else:
                # Show placeholder if logo doesn't exist
                placeholder = tk.Label(logo_frame, text="Place logo.png\nin main directory\n(600x250 recommended)", 
                                     justify=tk.CENTER, foreground="gray")
                placeholder.pack()
        except Exception as e:
            # If PIL not available or image error, show message
            error_label = tk.Label(logo_frame, text=f"Logo error:\n{str(e)}", 
                                 justify=tk.CENTER, foreground="red")
            error_label.pack()
        
        tags_canvas = tk.Canvas(tags_frame, height=200)
        self.tags_canvas = tags_canvas  # Store reference for theme updates
        tags_scrollbar = ttk.Scrollbar(tags_frame, orient="vertical", command=tags_canvas.yview)
        tags_scrollable = ttk.Frame(tags_canvas)
        
        tags_scrollable.bind(
            "<Configure>",
            lambda e: tags_canvas.configure(scrollregion=tags_canvas.bbox("all"))
        )
        
        tags_canvas.create_window((0, 0), window=tags_scrollable, anchor="nw")
        tags_canvas.configure(yscrollcommand=tags_scrollbar.set)
        
        tags_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tags_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.tag_vars = {}
        for idx, tag in enumerate(self.available_tags):
            var = tk.BooleanVar()
            self.tag_vars[tag] = var
            cb = ttk.Checkbutton(tags_scrollable, text=tag, variable=var)
            cb.grid(row=idx // 6, column=idx % 6, sticky=tk.W, padx=5, pady=2)
        
        
        selected_tags_frame = ttk.Frame(tags_frame)
        selected_tags_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        ttk.Label(selected_tags_frame, text="Selected Tags:").grid(row=0, column=0, sticky=tk.W)
        self.selected_tags_label = ttk.Label(selected_tags_frame, text="None")
        self.selected_tags_label.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        for tag, var in self.tag_vars.items():
            var.trace_add('write', lambda *args: self.update_selected_tags())
        
        # Create container for lyrics and parameters side-by-side
        content_container = ttk.Frame(parent)
        content_container.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        content_container.columnconfigure(0, weight=1)
        content_container.columnconfigure(1, weight=0)
        
        # Lyrics on the left
        lyrics_frame = ttk.LabelFrame(content_container, text="Lyrics", padding="10")
        lyrics_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        lyrics_frame.columnconfigure(0, weight=1)
        lyrics_frame.rowconfigure(0, weight=1)
        
        self.lyrics_text = scrolledtext.ScrolledText(lyrics_frame, height=12, wrap=tk.WORD, width=40)
        self.lyrics_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.lyrics_text.insert('1.0', "[Intro]\n\n[Verse]\n\n[Chorus]\n\n[Outro]\n")
        
        # Parameters on the right
        params_frame = ttk.LabelFrame(content_container, text="Generation Parameters", padding="10")
        params_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        row = 0
        ttk.Label(params_frame, text="Audio Length:").grid(row=row, column=0, sticky=tk.W, pady=5)
        
        # Slider for audio length (1-240 seconds)
        self.audio_length_seconds = tk.IntVar(value=30)
        self.max_length_var = tk.StringVar(value="30000")  # Keep for compatibility
        
        slider_frame = ttk.Frame(params_frame)
        slider_frame.grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5)
        
        self.audio_slider = tk.Scale(slider_frame, from_=1, to=240, orient=tk.HORIZONTAL,
                                     variable=self.audio_length_seconds, length=300,
                                     command=self.update_audio_length_label)
        self.audio_slider.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.audio_length_label = ttk.Label(slider_frame, text="30 seconds (30000 ms)")
        self.audio_length_label.grid(row=0, column=1, padx=(10, 0))
        
        # Update max_length_var when slider changes
        def sync_length(*args):
            seconds = self.audio_length_seconds.get()
            ms = seconds * 1000
            self.max_length_var.set(str(ms))
            self.audio_length_label.config(text=f"{seconds} seconds ({ms} ms)")
        
        self.audio_length_seconds.trace_add('write', sync_length)
        
        row += 1
        ttk.Label(params_frame, text="Top-K:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.topk_var = tk.StringVar(value="50")
        ttk.Entry(params_frame, textvariable=self.topk_var, width=15).grid(row=row, column=1, sticky=tk.W, padx=5)
        ttk.Label(params_frame, text="(sampling diversity, 1-100)", foreground="gray").grid(row=row, column=2, sticky=tk.W)
        
        row += 1
        ttk.Label(params_frame, text="Temperature:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.temperature_var = tk.StringVar(value="1.0")
        ttk.Entry(params_frame, textvariable=self.temperature_var, width=15).grid(row=row, column=1, sticky=tk.W, padx=5)
        ttk.Label(params_frame, text="(randomness, 0.1-2.0)", foreground="gray").grid(row=row, column=2, sticky=tk.W)
        
        row += 1
        ttk.Label(params_frame, text="CFG Scale:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.cfg_scale_var = tk.StringVar(value="1.5")
        ttk.Entry(params_frame, textvariable=self.cfg_scale_var, width=15).grid(row=row, column=1, sticky=tk.W, padx=5)
        ttk.Label(params_frame, text="(guidance strength, 1.0-3.0)", foreground="gray").grid(row=row, column=2, sticky=tk.W)
        
        row += 1
        ttk.Label(params_frame, text="Output Filename:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.filename_var = tk.StringVar(value="output")
        ttk.Entry(params_frame, textvariable=self.filename_var, width=30).grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5)
        
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.generate_btn = ttk.Button(buttons_frame, text="Generate Now", command=self.generate_music)
        self.generate_btn.grid(row=0, column=0, padx=5)
        
        self.add_batch_btn = ttk.Button(buttons_frame, text="Add to Batch", command=self.add_to_batch)
        self.add_batch_btn.grid(row=0, column=1, padx=5)
        
        ttk.Button(buttons_frame, text="Clear Form", command=self.clear_form).grid(row=0, column=2, padx=5)
        
    def update_audio_length_label(self, value=None):
        """Update the audio length label when slider changes"""
        seconds = self.audio_length_seconds.get()
        ms = seconds * 1000
        self.max_length_var.set(str(ms))
        self.audio_length_label.config(text=f"{seconds} seconds ({ms} ms)")
    
    def setup_batch_tab(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        list_frame = ttk.Frame(parent)
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.batch_tree = ttk.Treeview(list_frame, columns=("Tags", "Length", "Filename"), show="tree headings", height=15)
        self.batch_tree.heading("#0", text="ID")
        self.batch_tree.heading("Tags", text="Tags")
        self.batch_tree.heading("Length", text="Length (s)")
        self.batch_tree.heading("Filename", text="Filename")
        
        self.batch_tree.column("#0", width=50)
        self.batch_tree.column("Tags", width=300)
        self.batch_tree.column("Length", width=100)
        self.batch_tree.column("Filename", width=200)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.batch_tree.yview)
        self.batch_tree.configure(yscrollcommand=scrollbar.set)
        
        self.batch_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.start_batch_btn = ttk.Button(buttons_frame, text="Start Batch Processing", command=self.start_batch_processing)
        self.start_batch_btn.grid(row=0, column=0, padx=5)
        
        ttk.Button(buttons_frame, text="Remove Selected", command=self.remove_from_batch).grid(row=0, column=1, padx=5)
        ttk.Button(buttons_frame, text="Clear All", command=self.clear_batch).grid(row=0, column=2, padx=5)
        
        self.batch_progress = ttk.Progressbar(buttons_frame, mode='determinate')
        self.batch_progress.grid(row=0, column=3, padx=20, sticky=(tk.W, tk.E))
        buttons_frame.columnconfigure(3, weight=1)
        
    def setup_settings_tab(self, parent):
        row = 0
        
        ttk.Label(parent, text="Model Path:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.model_path_var = tk.StringVar(value="./ckpt")
        ttk.Entry(parent, textvariable=self.model_path_var, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(parent, text="Browse", command=self.browse_model_path).grid(row=row, column=2, padx=5)
        
        row += 1
        ttk.Label(parent, text="Output Folder:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.output_folder_var = tk.StringVar(value="./output")
        ttk.Entry(parent, textvariable=self.output_folder_var, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(parent, text="Browse", command=self.browse_output_folder).grid(row=row, column=2, padx=5)
        
        row += 1
        ttk.Label(parent, text="Model Version:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.version_var = tk.StringVar(value="3B")
        version_combo = ttk.Combobox(parent, textvariable=self.version_var, values=["3B", "7B"], state="readonly", width=10)
        version_combo.grid(row=row, column=1, sticky=tk.W, padx=5)
        
        row += 1
        ttk.Label(parent, text="Device:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.device_var = tk.StringVar(value="cuda")
        device_combo = ttk.Combobox(parent, textvariable=self.device_var, values=["cuda", "cpu"], state="readonly", width=10)
        device_combo.grid(row=row, column=1, sticky=tk.W, padx=5)
        
        row += 1
        ttk.Label(parent, text="Data Type:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.dtype_var = tk.StringVar(value="bfloat16")
        dtype_combo = ttk.Combobox(parent, textvariable=self.dtype_var, values=["bfloat16", "float16", "float32"], state="readonly", width=10)
        dtype_combo.grid(row=row, column=1, sticky=tk.W, padx=5)
        
        row += 1
        ttk.Separator(parent, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        row += 1
        ttk.Label(parent, text="Optimization:", font=('TkDefaultFont', 9, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=5)
        
        row += 1
        self.use_fp8_var = tk.BooleanVar(value=BITSANDBYTES_AVAILABLE)
        fp8_check = ttk.Checkbutton(parent, text="Enable FP8 Quantization (50% less VRAM)", variable=self.use_fp8_var)
        fp8_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        if not BITSANDBYTES_AVAILABLE:
            fp8_check.config(state='disabled')
        
        row += 1
        if BITSANDBYTES_AVAILABLE:
            fp8_status = ttk.Label(parent, text="✓ bitsandbytes available", foreground="green")
        else:
            fp8_status = ttk.Label(parent, text="✗ bitsandbytes not installed (pip install bitsandbytes)", foreground="orange")
        fp8_status.grid(row=row, column=0, columnspan=3, sticky=tk.W, padx=20)
        
        row += 1
        ttk.Separator(parent, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        row += 1
        ttk.Label(parent, text="Theme:", font=('TkDefaultFont', 9, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=5)
        
        row += 1
        ttk.Label(parent, text="Color Scheme:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.theme_var = tk.StringVar(value="Dark Blue/Grey")
        theme_combo = ttk.Combobox(parent, textvariable=self.theme_var, values=list(THEMES.keys()), state="readonly", width=20)
        theme_combo.grid(row=row, column=1, sticky=tk.W, padx=5)
        theme_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_theme(self.theme_var.get()))
        
        row += 1
        ttk.Separator(parent, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        row += 1
        self.auto_load_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(parent, text="Auto-load model on startup", variable=self.auto_load_var).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        row += 1
        self.timestamp_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(parent, text="Add timestamp to output files", variable=self.timestamp_var).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        row += 1
        ttk.Separator(parent, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        row += 1
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=row, column=0, columnspan=3, sticky=tk.W)
        
        self.load_model_btn = ttk.Button(buttons_frame, text="Load Model", command=self.load_model)
        self.load_model_btn.grid(row=0, column=0, padx=5)
        
        ttk.Button(buttons_frame, text="Save Settings", command=self.save_config).grid(row=0, column=1, padx=5)
        
        self.model_status_label = ttk.Label(buttons_frame, text="Model: Not Loaded", foreground="red")
        self.model_status_label.grid(row=0, column=2, padx=20)
        
        parent.columnconfigure(1, weight=1)
        
    def setup_info_tab(self, parent):
        """Setup the Info tab with links to GitHub repositories and documentation"""
        parent.columnconfigure(0, weight=1)
        
        # Create a scrollable frame for the info content
        canvas = tk.Canvas(parent, bg=THEMES[self.current_theme]["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        parent.rowconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(scrollable_frame, text="HeartMuLaGUI - Windows Music Generation Interface", 
                               font=('TkDefaultFont', 14, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # Version info
        version_label = ttk.Label(scrollable_frame, text="Version 1.0 - Windows Edition", 
                                 font=('TkDefaultFont', 10))
        version_label.grid(row=1, column=0, pady=(0, 20), sticky=tk.W)
        
        # HeartMuLaGUI Section
        row = 2
        gui_section = ttk.LabelFrame(scrollable_frame, text="HeartMuLaGUI Project", padding="10")
        gui_section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(gui_section, text="This Windows GUI application for HeartMuLa music generation", 
                 wraplength=700).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Label(gui_section, text="GitHub Repository:", font=('TkDefaultFont', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        github_gui_link = tk.Text(gui_section, height=1, width=60, wrap=tk.NONE, relief=tk.FLAT, 
                                 background=THEMES[self.current_theme]["bg"], foreground='blue', cursor='hand2')
        github_gui_link.insert('1.0', "https://github.com/Starnodes2024/HeartMuLaGUI")
        github_gui_link.config(state='disabled')
        github_gui_link.grid(row=1, column=1, sticky=tk.W, pady=5)
        github_gui_link.bind("<Button-1>", lambda e: self.open_url("https://github.com/Starnodes2024/HeartMuLaGUI"))
        
        # Original HeartMuLa Section
        row += 1
        heartlib_section = ttk.LabelFrame(scrollable_frame, text="Original HeartMuLa Project", padding="10")
        heartlib_section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(heartlib_section, text="Based on HeartMuLa - Open Source Music Foundation Models", 
                 wraplength=700).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Label(heartlib_section, text="GitHub Repository:", font=('TkDefaultFont', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        github_heart_link = tk.Text(heartlib_section, height=1, width=60, wrap=tk.NONE, relief=tk.FLAT,
                                   background=THEMES[self.current_theme]["bg"], foreground='blue', cursor='hand2')
        github_heart_link.insert('1.0', "https://github.com/HeartMuLa/heartlib")
        github_heart_link.config(state='disabled')
        github_heart_link.grid(row=1, column=1, sticky=tk.W, pady=5)
        github_heart_link.bind("<Button-1>", lambda e: self.open_url("https://github.com/HeartMuLa/heartlib"))
        
        ttk.Label(heartlib_section, text="Research Paper:", font=('TkDefaultFont', 9, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=5)
        paper_link = tk.Text(heartlib_section, height=1, width=60, wrap=tk.NONE, relief=tk.FLAT,
                            background=THEMES[self.current_theme]["bg"], foreground='blue', cursor='hand2')
        paper_link.insert('1.0', "https://arxiv.org/abs/2601.10547")
        paper_link.config(state='disabled')
        paper_link.grid(row=2, column=1, sticky=tk.W, pady=5)
        paper_link.bind("<Button-1>", lambda e: self.open_url("https://arxiv.org/abs/2601.10547"))
        
        ttk.Label(heartlib_section, text="Demo Website:", font=('TkDefaultFont', 9, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=5)
        demo_link = tk.Text(heartlib_section, height=1, width=60, wrap=tk.NONE, relief=tk.FLAT,
                           background=THEMES[self.current_theme]["bg"], foreground='blue', cursor='hand2')
        demo_link.insert('1.0', "https://heartmula.github.io/")
        demo_link.config(state='disabled')
        demo_link.grid(row=3, column=1, sticky=tk.W, pady=5)
        demo_link.bind("<Button-1>", lambda e: self.open_url("https://heartmula.github.io/"))
        
        # Documentation Section
        row += 1
        docs_section = ttk.LabelFrame(scrollable_frame, text="Documentation", padding="10")
        docs_section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        docs_list = [
            ("Quick Start Guide", "QUICK_START.md"),
            ("User Guide", "GUI_USER_GUIDE.md"),
            ("FP8 Optimization Guide", "FP8_OPTIMIZATION_GUIDE.md"),
            ("Troubleshooting", "TROUBLESHOOTING.md"),
            ("Original HeartMuLa README", "README-HEARTLIB.md")
        ]
        
        for idx, (name, filename) in enumerate(docs_list):
            ttk.Label(docs_section, text=f"• {name}:").grid(row=idx, column=0, sticky=tk.W, pady=2)
            ttk.Label(docs_section, text=filename, foreground='gray').grid(row=idx, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        
        # License Section
        row += 1
        license_section = ttk.LabelFrame(scrollable_frame, text="License & Attribution", padding="10")
        license_section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        license_text = """This project is licensed under Apache License 2.0

HeartMuLaGUI is a derivative work based on HeartMuLa/heartlib.

Please credit both:
• HeartMuLa Team - Original music generation library
• HeartMuLaGUI Contributors - Windows GUI application

See LICENSE and LICENSE-ORIGINAL files for details."""
        
        ttk.Label(license_section, text=license_text, wraplength=700, justify=tk.LEFT).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Features Section
        row += 1
        features_section = ttk.LabelFrame(scrollable_frame, text="Key Features", padding="10")
        features_section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        features_text = """✓ Easy-to-use Windows GUI interface
✓ One-click setup with 01_SETUP_GUI.bat
✓ Automatic model download support
✓ FP8 optimization for 8GB VRAM GPUs
✓ Batch processing for multiple songs
✓ 40+ musical tags (instruments, moods, genres)
✓ Multilingual lyrics support
✓ Real-time generation progress tracking"""
        
        ttk.Label(features_section, text=features_text, justify=tk.LEFT).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # System Requirements
        row += 1
        req_section = ttk.LabelFrame(scrollable_frame, text="System Requirements", padding="10")
        req_section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        req_text = """• Windows 10/11 (64-bit)
• NVIDIA GPU with 8GB+ VRAM (CUDA support)
• 20GB free disk space (15GB for models)
• Internet connection for model download"""
        
        ttk.Label(req_section, text=req_text, justify=tk.LEFT).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        scrollable_frame.columnconfigure(0, weight=1)
    
    def open_url(self, url):
        """Open URL in default web browser"""
        import webbrowser
        try:
            webbrowser.open(url)
            self.log(f"Opening: {url}")
        except Exception as e:
            self.log(f"Error opening URL: {e}")
            messagebox.showerror("Error", f"Could not open URL:\n{url}\n\nError: {e}")
        
    def update_selected_tags(self):
        selected = [tag for tag, var in self.tag_vars.items() if var.get()]
        if selected:
            tags_str = ",".join(selected)
            self.selected_tags_label.config(text=tags_str)
        else:
            self.selected_tags_label.config(text="None")
    
    def get_selected_tags(self):
        selected = [tag for tag, var in self.tag_vars.items() if var.get()]
        return ",".join(selected) if selected else ""
    
    def browse_model_path(self):
        path = filedialog.askdirectory(title="Select Model Directory")
        if path:
            self.model_path_var.set(path)
    
    def browse_output_folder(self):
        path = filedialog.askdirectory(title="Select Output Directory")
        if path:
            self.output_folder_var.set(path)
    
    def log(self, message):
        self.log_text.config(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        self.log_text.insert(tk.END, log_msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update_idletasks()
        # Also print to console for debugging
        print(log_msg)
    
    def update_status(self, message):
        self.status_bar.config(text=message)
        self.root.update_idletasks()
        print(f"STATUS: {message}")
    
    def check_cuda_on_startup(self):
        """Check CUDA availability on startup and warn user if not available"""
        try:
            cuda_available = torch.cuda.is_available()
            torch_version = torch.__version__
            
            print("\n" + "="*60)
            print("PyTorch Environment Check")
            print("="*60)
            print(f"PyTorch version: {torch_version}")
            print(f"CUDA available: {cuda_available}")
            
            if cuda_available:
                print(f"CUDA version: {torch.version.cuda}")
                print(f"GPU Device: {torch.cuda.get_device_name(0)}")
                total_vram = torch.cuda.get_device_properties(0).total_memory / 1024**3
                print(f"Total VRAM: {total_vram:.2f} GB")
                print("="*60 + "\n")
                
                self.log(f"✓ CUDA available - GPU: {torch.cuda.get_device_name(0)}")
                self.log(f"✓ VRAM: {total_vram:.2f} GB")
            else:
                print("="*60)
                print("\n⚠ WARNING: CUDA NOT AVAILABLE!")
                print("\nThis means PyTorch was installed without CUDA support.")
                print("\nTo fix this issue:")
                print("1. Close this GUI")
                print("2. Run: fix_cuda_issue.bat")
                print("3. Restart the GUI")
                print("\nAlternatively, you can use CPU mode (very slow):")
                print("- Go to Settings tab")
                print("- Change Device to 'cpu'")
                print("="*60 + "\n")
                
                self.log("⚠ WARNING: CUDA NOT AVAILABLE!")
                self.log("PyTorch not compiled with CUDA support")
                self.log("Run fix_cuda_issue.bat to fix, or use CPU mode (slow)")
                
                # Show warning dialog
                self.root.after(1000, lambda: messagebox.showwarning(
                    "CUDA Not Available",
                    "PyTorch is not compiled with CUDA support!\n\n"
                    "GPU acceleration will NOT work.\n\n"
                    "To fix:\n"
                    "1. Close this GUI\n"
                    "2. Run: fix_cuda_issue.bat\n"
                    "3. Restart the GUI\n\n"
                    "Or use CPU mode in Settings (very slow)"
                ))
        except Exception as e:
            print(f"Error checking CUDA: {e}")
            self.log(f"Error checking CUDA: {e}")
    
    def load_model(self):
        if self.is_generating:
            messagebox.showwarning("Busy", "Cannot load model while generating music.")
            return
        
        def load_thread():
            try:
                self.log("Loading model... This may take a few minutes.")
                self.update_status("Loading model...")
                self.load_model_btn.config(state='disabled')
                
                model_path = self.model_path_var.get()
                device = torch.device(self.device_var.get())
                
                dtype_map = {
                    "bfloat16": torch.bfloat16,
                    "float16": torch.float16,
                    "float32": torch.float32
                }
                dtype = dtype_map[self.dtype_var.get()]
                
                bnb_config = None
                if self.use_fp8_var.get() and BITSANDBYTES_AVAILABLE:
                    self.log("Enabling FP8 quantization for reduced VRAM usage...")
                    bnb_config = BitsAndBytesConfig(
                        load_in_8bit=True,
                        llm_int8_threshold=6.0,
                        llm_int8_has_fp16_weight=False,
                    )
                
                self.pipe = HeartMuLaGenPipeline.from_pretrained(
                    model_path,
                    device=device,
                    dtype=dtype,
                    version=self.version_var.get(),
                    bnb_config=bnb_config
                )
                
                if bnb_config:
                    self.log("Model loaded successfully with FP8 quantization!")
                else:
                    self.log("Model loaded successfully!")
                self.update_status("Model loaded - Ready")
                self.model_status_label.config(text="Model: Loaded", foreground="green")
                self.generate_btn.config(state='normal')
                self.start_batch_btn.config(state='normal')
                
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                
                self.log(f"Error loading model: {str(e)}")
                self.log("=== Error Details ===")
                print("\n" + "="*60)
                print("ERROR LOADING MODEL")
                print("="*60)
                print(f"Error: {str(e)}")
                print("\nFull traceback:")
                print(error_details)
                print("\nPyTorch Information:")
                print(f"  Version: {torch.__version__}")
                print(f"  CUDA available: {torch.cuda.is_available()}")
                if torch.cuda.is_available():
                    print(f"  CUDA version: {torch.version.cuda}")
                    print(f"  Device: {torch.cuda.get_device_name(0)}")
                else:
                    print("  ⚠ CUDA NOT AVAILABLE - This is likely the problem!")
                print(f"\nDevice requested: {self.device_var.get()}")
                print(f"Model path: {self.model_path_var.get()}")
                print(f"FP8 enabled: {self.use_fp8_var.get()}")
                print("="*60 + "\n")
                
                # Log to GUI
                for line in error_details.split('\n')[:5]:  # First 5 lines
                    if line.strip():
                        self.log(line.strip())
                
                self.update_status("Error loading model")
                
                # Show detailed error
                error_msg = f"Failed to load model:\n{str(e)}\n\n"
                if "CUDA" in str(e) and not torch.cuda.is_available():
                    error_msg += "⚠ PyTorch not compiled with CUDA!\n\n"
                    error_msg += "Fix:\n1. Close GUI\n2. Run fix_cuda_issue.bat\n3. Restart GUI"
                
                messagebox.showerror("Error", error_msg)
            finally:
                self.load_model_btn.config(state='normal')
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def validate_parameters(self):
        try:
            max_length = int(self.max_length_var.get())
            if max_length <= 0:
                raise ValueError("Max audio length must be positive")
            
            topk = int(self.topk_var.get())
            if topk <= 0:
                raise ValueError("Top-K must be positive")
            
            temperature = float(self.temperature_var.get())
            if temperature <= 0:
                raise ValueError("Temperature must be positive")
            
            cfg_scale = float(self.cfg_scale_var.get())
            if cfg_scale < 1.0:
                raise ValueError("CFG scale must be >= 1.0")
            
            return True
        except ValueError as e:
            messagebox.showerror("Invalid Parameters", str(e))
            return False
    
    def generate_music(self):
        if self.pipe is None:
            messagebox.showwarning("Model Not Loaded", "Please load the model first in the Settings tab.")
            return
        
        if self.is_generating:
            messagebox.showwarning("Busy", "Already generating music. Please wait.")
            return
        
        if not self.validate_parameters():
            return
        
        tags = self.get_selected_tags()
        lyrics = self.lyrics_text.get('1.0', tk.END).strip()
        
        if not tags:
            messagebox.showwarning("No Tags", "Please select at least one tag.")
            return
        
        if not lyrics:
            messagebox.showwarning("No Lyrics", "Please enter lyrics.")
            return
        
        def generate_thread():
            self.is_generating = True
            start_time = datetime.now()  # Track start time
            try:
                self.generate_btn.config(state='disabled')
                self.add_batch_btn.config(state='disabled')
                self.reset_progress()
                
                output_folder = Path(self.output_folder_var.get())
                output_folder.mkdir(parents=True, exist_ok=True)
                
                filename = self.filename_var.get()
                if self.timestamp_var.get():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{filename}_{timestamp}"
                
                save_path = output_folder / f"{filename}.mp3"
                
                self.log(f"Generating music with tags: {tags}")
                self.log(f"Output: {save_path}")
                self.update_status("Generating music...")
                
                max_length = int(self.max_length_var.get())
                topk = int(self.topk_var.get())
                temperature = float(self.temperature_var.get())
                cfg_scale = float(self.cfg_scale_var.get())
                
                # Step 1: Prompt Processing
                self.log("Step 1/3: Processing prompt...")
                self.update_progress("prompt", 1, 1)
                
                # Step 2: Frame Generation (estimated based on audio length)
                max_frames = max_length // 80  # 80ms per frame
                self.log(f"Step 2/3: Generating {max_frames} audio frames...")
                
                # We'll update this during generation via a callback if possible
                # For now, simulate progress
                with torch.no_grad():
                    self.pipe(
                        {
                            "lyrics": lyrics,
                            "tags": tags,
                        },
                        max_audio_length_ms=max_length,
                        save_path=str(save_path),
                        topk=topk,
                        temperature=temperature,
                        cfg_scale=cfg_scale,
                    )
                
                # Step 3: Audio Decoding
                self.log("Step 3/3: Decoding audio...")
                self.update_progress("decode", 1, 1)
                
                # Calculate generation time
                end_time = datetime.now()
                elapsed = end_time - start_time
                minutes = int(elapsed.total_seconds() // 60)
                seconds = int(elapsed.total_seconds() % 60)
                
                self.log(f"Music generated successfully: {save_path}")
                self.log(f"Generated in {minutes} min {seconds} sec")
                self.update_status("Generation complete")
                messagebox.showinfo("Success", f"Music generated successfully!\n{save_path}\n\nGenerated in {minutes} min {seconds} sec")
                
            except Exception as e:
                self.log(f"Error during generation: {str(e)}")
                self.update_status("Generation failed")
                messagebox.showerror("Error", f"Failed to generate music:\n{str(e)}")
            finally:
                self.is_generating = False
                self.generate_btn.config(state='normal')
                self.add_batch_btn.config(state='normal')
                self.reset_progress()
        
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def add_to_batch(self):
        if not self.validate_parameters():
            return
        
        tags = self.get_selected_tags()
        lyrics = self.lyrics_text.get('1.0', tk.END).strip()
        
        if not tags:
            messagebox.showwarning("No Tags", "Please select at least one tag.")
            return
        
        if not lyrics:
            messagebox.showwarning("No Lyrics", "Please enter lyrics.")
            return
        
        batch_item = {
            "tags": tags,
            "lyrics": lyrics,
            "max_audio_length_ms": int(self.max_length_var.get()),
            "topk": int(self.topk_var.get()),
            "temperature": float(self.temperature_var.get()),
            "cfg_scale": float(self.cfg_scale_var.get()),
            "filename": self.filename_var.get()
        }
        
        self.batch_queue.append(batch_item)
        
        item_id = len(self.batch_queue)
        length_s = batch_item["max_audio_length_ms"] / 1000
        self.batch_tree.insert("", tk.END, text=str(item_id), 
                               values=(batch_item["tags"], f"{length_s:.1f}", batch_item["filename"]))
        
        self.log(f"Added to batch queue (#{item_id}): {batch_item['filename']}")
        messagebox.showinfo("Added", f"Added to batch queue (#{item_id})")
    
    def remove_from_batch(self):
        selected = self.batch_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an item to remove.")
            return
        
        for item in selected:
            idx = int(self.batch_tree.item(item, "text")) - 1
            self.batch_tree.delete(item)
        
        self.log("Removed selected items from batch queue")
    
    def clear_batch(self):
        if messagebox.askyesno("Clear Batch", "Are you sure you want to clear the entire batch queue?"):
            self.batch_queue.clear()
            for item in self.batch_tree.get_children():
                self.batch_tree.delete(item)
            self.log("Batch queue cleared")
    
    def start_batch_processing(self):
        if self.pipe is None:
            messagebox.showwarning("Model Not Loaded", "Please load the model first in the Settings tab.")
            return
        
        if self.is_generating:
            messagebox.showwarning("Busy", "Already generating music. Please wait.")
            return
        
        if not self.batch_queue:
            messagebox.showwarning("Empty Queue", "Batch queue is empty. Add items first.")
            return
        
        def batch_thread():
            self.is_generating = True
            batch_start_time = datetime.now()  # Track batch start time
            try:
                self.start_batch_btn.config(state='disabled')
                self.generate_btn.config(state='disabled')
                self.add_batch_btn.config(state='disabled')
                
                total = len(self.batch_queue)
                self.batch_progress['maximum'] = total
                self.batch_progress['value'] = 0
                
                output_folder = Path(self.output_folder_var.get())
                output_folder.mkdir(parents=True, exist_ok=True)
                
                for idx, item in enumerate(self.batch_queue, 1):
                    item_start_time = datetime.now()  # Track item start time
                    self.log(f"Processing batch item {idx}/{total}: {item['filename']}")
                    self.update_status(f"Processing batch {idx}/{total}")
                    self.reset_progress()
                    
                    filename = item['filename']
                    if self.timestamp_var.get():
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"{filename}_{timestamp}"
                    
                    save_path = output_folder / f"{filename}.mp3"
                    
                    # Step 1: Prompt Processing
                    self.log(f"  Step 1/3: Processing prompt...")
                    self.update_progress("prompt", 1, 1)
                    
                    # Step 2: Frame Generation
                    max_frames = item["max_audio_length_ms"] // 80
                    self.log(f"  Step 2/3: Generating {max_frames} frames...")
                    
                    with torch.no_grad():
                        self.pipe(
                            {
                                "lyrics": item["lyrics"],
                                "tags": item["tags"],
                            },
                            max_audio_length_ms=item["max_audio_length_ms"],
                            save_path=str(save_path),
                            topk=item["topk"],
                            temperature=item["temperature"],
                            cfg_scale=item["cfg_scale"],
                        )
                    
                    # Step 3: Audio Decoding
                    self.log(f"  Step 3/3: Decoding audio...")
                    self.update_progress("decode", 1, 1)
                    
                    # Calculate item generation time
                    item_end_time = datetime.now()
                    item_elapsed = item_end_time - item_start_time
                    item_minutes = int(item_elapsed.total_seconds() // 60)
                    item_seconds = int(item_elapsed.total_seconds() % 60)
                    
                    self.log(f"Completed: {save_path} (generated in {item_minutes} min {item_seconds} sec)")
                    self.batch_progress['value'] = idx
                
                # Calculate total batch time
                batch_end_time = datetime.now()
                batch_elapsed = batch_end_time - batch_start_time
                batch_minutes = int(batch_elapsed.total_seconds() // 60)
                batch_seconds = int(batch_elapsed.total_seconds() % 60)
                
                self.log(f"Batch processing complete! Generated {total} files.")
                self.log(f"Total batch time: {batch_minutes} min {batch_seconds} sec")
                self.update_status("Batch processing complete")
                messagebox.showinfo("Complete", f"Batch processing complete!\nGenerated {total} files.\n\nTotal time: {batch_minutes} min {batch_seconds} sec")
                
                self.clear_batch()
                
            except Exception as e:
                self.log(f"Error during batch processing: {str(e)}")
                self.update_status("Batch processing failed")
                messagebox.showerror("Error", f"Batch processing failed:\n{str(e)}")
            finally:
                self.is_generating = False
                self.start_batch_btn.config(state='normal')
                self.generate_btn.config(state='normal')
                self.add_batch_btn.config(state='normal')
                self.batch_progress['value'] = 0
        
        threading.Thread(target=batch_thread, daemon=True).start()
    
    def clear_form(self):
        for var in self.tag_vars.values():
            var.set(False)
        self.lyrics_text.delete('1.0', tk.END)
        self.lyrics_text.insert('1.0', "[Intro]\n\n[Verse]\n\n[Chorus]\n\n[Outro]\n")
        self.filename_var.set("output")
        self.log("Form cleared")
    
    def save_config(self):
        config = {
            "model_path": self.model_path_var.get(),
            "output_folder": self.output_folder_var.get(),
            "version": self.version_var.get(),
            "device": self.device_var.get(),
            "dtype": self.dtype_var.get(),
            "auto_load": self.auto_load_var.get(),
            "timestamp": self.timestamp_var.get(),
            "use_fp8": self.use_fp8_var.get(),
            "theme": self.theme_var.get(),
        }
        
        try:
            with open("gui_config.json", "w") as f:
                json.dump(config, f, indent=2)
            self.log("Settings saved")
            messagebox.showinfo("Saved", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings:\n{str(e)}")
    
    def load_config(self):
        try:
            if os.path.exists("gui_config.json"):
                with open("gui_config.json", "r") as f:
                    config = json.load(f)
                
                self.model_path_var.set(config.get("model_path", "./ckpt"))
                self.output_folder_var.set(config.get("output_folder", "./output"))
                self.version_var.set(config.get("version", "3B"))
                self.device_var.set(config.get("device", "cuda"))
                self.dtype_var.set(config.get("dtype", "bfloat16"))
                self.auto_load_var.set(config.get("auto_load", False))
                self.timestamp_var.set(config.get("timestamp", True))
                self.use_fp8_var.set(config.get("use_fp8", BITSANDBYTES_AVAILABLE))
                
                # Load and apply theme
                saved_theme = config.get("theme", "Dark Blue/Grey")
                self.theme_var.set(saved_theme)
                self.current_theme = saved_theme
                
                self.log("Settings loaded from config file")
                
                if self.auto_load_var.get():
                    self.root.after(1000, self.load_model)
        except Exception as e:
            self.log(f"Could not load config: {str(e)}")
    
    def apply_theme(self, theme_name):
        """Apply the selected theme to the GUI"""
        if theme_name not in THEMES:
            return
        
        self.current_theme = theme_name
        theme = THEMES[theme_name]
        
        # Apply to root window
        self.root.configure(bg=theme["bg"])
        
        # Create custom style and force use of 'alt' theme which is more customizable
        style = ttk.Style()
        try:
            style.theme_use('alt')  # Use 'alt' theme which allows better customization
        except:
            pass  # If 'alt' not available, continue with default
        
        # Configure ttk widgets with theme colors
        style.configure("TFrame", background=theme["bg"])
        style.configure("TLabel", background=theme["bg"], foreground=theme["fg"])
        style.configure("TLabelframe", background=theme["bg"], foreground=theme["fg"])
        style.configure("TLabelframe.Label", background=theme["bg"], foreground=theme["fg"])
        
        # Button styling with proper foreground mapping and border
        style.configure("TButton", 
                       background=theme["button_bg"], 
                       foreground=theme["button_fg"],
                       borderwidth=1,
                       relief="raised",
                       padding=6)
        style.map("TButton", 
                  background=[("active", theme["select_bg"]), ("pressed", theme["select_bg"]), ("!disabled", theme["button_bg"])],
                  foreground=[("active", theme["select_fg"]), ("pressed", theme["select_fg"]), ("!disabled", theme["button_fg"]), ("disabled", "gray")],
                  relief=[("pressed", "sunken"), ("!pressed", "raised")])
        
        # Checkbutton and Radiobutton with proper foreground and indicator colors
        style.configure("TCheckbutton", 
                       background=theme["bg"], 
                       foreground=theme["fg"],
                       indicatorcolor=theme["entry_bg"],
                       indicatorrelief="sunken",
                       borderwidth=2)
        style.map("TCheckbutton", 
                  foreground=[("active", theme["fg"]), ("!disabled", theme["fg"]), ("disabled", "gray")],
                  background=[("active", theme["bg"]), ("!disabled", theme["bg"])],
                  indicatorcolor=[("selected", theme["select_bg"]), ("!selected", theme["entry_bg"])])
        
        style.configure("TRadiobutton", 
                       background=theme["bg"], 
                       foreground=theme["fg"],
                       indicatorcolor=theme["entry_bg"],
                       indicatorrelief="sunken",
                       borderwidth=2)
        style.map("TRadiobutton", 
                  foreground=[("active", theme["fg"]), ("!disabled", theme["fg"]), ("disabled", "gray")],
                  background=[("active", theme["bg"]), ("!disabled", theme["bg"])],
                  indicatorcolor=[("selected", theme["select_bg"]), ("!selected", theme["entry_bg"])])
        
        # Notebook tabs with proper foreground
        style.configure("TNotebook", background=theme["bg"])
        style.configure("TNotebook.Tab", background=theme["button_bg"], foreground=theme["button_fg"])
        style.map("TNotebook.Tab", 
                  background=[("selected", theme["select_bg"]), ("active", theme["button_bg"])],
                  foreground=[("selected", theme["select_fg"]), ("active", theme["button_fg"])])
        
        # Entry and Combobox styling
        style.configure("TEntry", fieldbackground=theme["entry_bg"], foreground=theme["entry_fg"])
        style.map("TEntry", 
                  fieldbackground=[("readonly", theme["entry_bg"]), ("disabled", theme["bg"])],
                  foreground=[("readonly", theme["entry_fg"]), ("disabled", "gray")])
        
        style.configure("TCombobox", 
                       fieldbackground=theme["entry_bg"], 
                       foreground=theme["entry_fg"], 
                       background=theme["button_bg"], 
                       arrowcolor=theme["fg"],
                       borderwidth=1,
                       relief="sunken")
        style.map("TCombobox",
                  fieldbackground=[("readonly", theme["entry_bg"]), ("!disabled", theme["entry_bg"]), ("disabled", theme["bg"])],
                  foreground=[("readonly", theme["entry_fg"]), ("!disabled", theme["entry_fg"]), ("disabled", "gray")],
                  background=[("readonly", theme["button_bg"]), ("!disabled", theme["button_bg"]), ("disabled", theme["bg"])],
                  arrowcolor=[("disabled", "gray"), ("!disabled", theme["fg"])])
        
        # Configure progressbar with theme colors
        style.configure("TProgressbar", background=theme["progress_fg"], troughcolor=theme["progress_bg"])
        
        # Update text widgets (ScrolledText, Canvas)
        try:
            self.log_text.configure(bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["fg"])
            self.lyrics_text.configure(bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["fg"])
        except:
            pass
        
        # Update tags canvas background
        try:
            self.tags_canvas.configure(bg=theme["bg"])
        except:
            pass
        
        # Update selected tags label color
        try:
            self.selected_tags_label.configure(foreground=theme["selected_tags_color"])
        except:
            pass
        
        # Update logo background if logo exists
        if self.logo_label:
            try:
                self.logo_label.configure(bg=theme["bg"])
            except:
                pass
        
        # Update slider colors
        try:
            self.audio_slider.configure(
                bg=theme["bg"],
                fg=theme["fg"],
                troughcolor=theme["entry_bg"],
                activebackground=theme["select_bg"],
                highlightbackground=theme["bg"],
                highlightcolor=theme["select_bg"]
            )
        except:
            pass
        
        self.log(f"Theme changed to: {theme_name}")
    
    def update_progress(self, step, current, total):
        """Update progress bars with current step information"""
        if step == "prompt":
            self.progress_prompt['maximum'] = total
            self.progress_prompt['value'] = current
            self.progress_prompt_label.config(text=f"{current}/{total}")
        elif step == "frames":
            self.progress_frames['maximum'] = total
            self.progress_frames['value'] = current
            self.progress_frames_label.config(text=f"{current}/{total}")
            self.log(f"Generating frame {current}/{total}")
        elif step == "decode":
            self.progress_decode['maximum'] = total
            self.progress_decode['value'] = current
            self.progress_decode_label.config(text=f"{current}/{total}")
        
        self.root.update_idletasks()
    
    def reset_progress(self):
        """Reset all progress bars to zero"""
        self.progress_prompt['value'] = 0
        self.progress_prompt_label.config(text="0/0")
        self.progress_frames['value'] = 0
        self.progress_frames_label.config(text="0/0")
        self.progress_decode['value'] = 0
        self.progress_decode_label.config(text="0/0")
        self.root.update_idletasks()


def main():
    root = tk.Tk()
    app = HeartMuLaGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
