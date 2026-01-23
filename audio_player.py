"""
Inline Audio Player with Waveform Visualization for Music Library
Uses pygame for audio playback and matplotlib for waveform display
"""

import os
import threading
import time
import tkinter as tk
from tkinter import ttk
import numpy as np
from pathlib import Path

# Audio libraries
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("pygame not available - audio playback disabled")

try:
    import warnings
    # Suppress pydub ffmpeg warning
    warnings.filterwarnings("ignore", message="Couldn't find ffprobe or avprobe")
    from pydub import AudioSegment
    import librosa
    WAVEFORM_AVAILABLE = True
except ImportError:
    WAVEFORM_AVAILABLE = False
    print("pydub/librosa not available - waveform visualization disabled")

try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("matplotlib not available - waveform visualization disabled")


class InlineAudioPlayer:
    """Inline audio player with waveform visualization and controls"""
    
    def __init__(self, parent, file_path, theme_bg="#2b2b2b"):
        self.parent = parent
        self.file_path = file_path
        self.theme_bg = theme_bg
        self.is_playing = False
        self.is_paused = False
        self.duration = 0
        self.current_position = 0
        self.update_thread = None
        self.stop_update = False
        
        # Initialize pygame mixer
        if PYGAME_AVAILABLE:
            try:
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
            except:
                pass
        
        self.create_player_ui()
        self.load_audio_info()
    
    def create_player_ui(self):
        """Create the compact player UI with waveform and controls"""
        # Main player frame - more compact
        self.player_frame = ttk.Frame(self.parent)
        self.player_frame.pack(fill=tk.X, pady=2)
        
        # Waveform display area
        if MATPLOTLIB_AVAILABLE and WAVEFORM_AVAILABLE:
            self.create_waveform_display()
        else:
            # Fallback: simple progress bar
            self.create_simple_progress()
        
        # Compact controls frame
        controls_frame = ttk.Frame(self.player_frame)
        controls_frame.pack(fill=tk.X, pady=(2, 0))
        
        # Compact Play/Pause button
        self.play_btn = ttk.Button(controls_frame, text="▶️", 
                                   command=self.toggle_play, width=3)
        self.play_btn.pack(side=tk.LEFT, padx=1)
        
        # Compact Stop button
        ttk.Button(controls_frame, text="⏹️", 
                  command=self.stop, width=3).pack(side=tk.LEFT, padx=1)
        
        # Compact time labels
        self.time_label = ttk.Label(controls_frame, text="0:00/0:00", font=('TkDefaultFont', 7))
        self.time_label.pack(side=tk.LEFT, padx=5)
        
        # Volume control with theme styling
        ttk.Label(controls_frame, text="🔊", font=('TkDefaultFont', 7)).pack(side=tk.LEFT, padx=(5, 1))
        
        # Create styled scale with theme colors
        style = ttk.Style()
        style.configure("Themed.Horizontal.TScale", background=self.theme_bg)
        
        self.volume_scale = ttk.Scale(controls_frame, from_=0, to=100, 
                                      orient=tk.HORIZONTAL, length=80,
                                      command=self.set_volume,
                                      style="Themed.Horizontal.TScale")
        self.volume_scale.set(70)
        self.volume_scale.pack(side=tk.LEFT, padx=1)
    
    def create_waveform_display(self):
        """Create compact matplotlib waveform visualization"""
        # Create compact figure with dark theme
        self.fig = Figure(figsize=(4, 1), dpi=80, facecolor=self.theme_bg)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(self.theme_bg)
        
        # Style the plot - more compact
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_color('#555555')
        self.ax.spines['left'].set_color('#555555')
        self.ax.tick_params(colors='#888888', labelsize=6)
        self.ax.set_ylim(-1, 1)
        
        # Embed in tkinter - compact
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.player_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.X, pady=(0, 2))
        
        # Position marker (vertical line)
        self.position_line = None
        
        # Load and display waveform
        self.load_waveform()
    
    def create_simple_progress(self):
        """Fallback: simple progress bar if matplotlib not available"""
        progress_frame = ttk.Frame(self.player_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=600)
        self.progress_bar.pack(fill=tk.X, padx=5)
    
    def load_waveform(self):
        """Load and display audio waveform"""
        if not WAVEFORM_AVAILABLE or not MATPLOTLIB_AVAILABLE:
            return
        
        try:
            # Load audio with librosa (faster for waveform)
            y, sr = librosa.load(self.file_path, sr=22050, mono=True)
            
            # Downsample for display (show ~1000 points)
            hop_length = max(1, len(y) // 1000)
            y_display = y[::hop_length]
            
            # Time axis
            time_display = np.arange(len(y_display)) * hop_length / sr
            
            # Plot waveform
            self.ax.clear()
            self.ax.fill_between(time_display, y_display, alpha=0.6, color='#4a9eff')
            self.ax.plot(time_display, y_display, color='#2e7dd1', linewidth=0.5)
            self.ax.set_xlim(0, len(y) / sr)
            self.ax.set_ylim(-1, 1)
            self.ax.set_xlabel('Time (s)', color='#888888', fontsize=8)
            self.ax.set_ylabel('Amplitude', color='#888888', fontsize=8)
            
            # Store duration
            self.duration = len(y) / sr
            
            # Initial position line
            self.position_line = self.ax.axvline(x=0, color='#ff4444', linewidth=2, alpha=0.8)
            
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error loading waveform: {e}")
    
    def load_audio_info(self):
        """Load audio file information"""
        if not PYGAME_AVAILABLE:
            return
        
        try:
            # Get duration using pydub if available
            if WAVEFORM_AVAILABLE:
                try:
                    audio = AudioSegment.from_mp3(self.file_path)
                    self.duration = len(audio) / 1000.0  # Convert to seconds
                except Exception:
                    # FFmpeg not available - use pygame fallback
                    pass
            
            self.update_time_label()
        except Exception:
            # Silent fallback - player still works without duration
            pass
    
    def toggle_play(self):
        """Toggle play/pause"""
        if not PYGAME_AVAILABLE:
            return
        
        if not self.is_playing:
            self.play()
        else:
            if self.is_paused:
                self.resume()
            else:
                self.pause()
    
    def play(self):
        """Start playing audio"""
        if not PYGAME_AVAILABLE:
            return
        
        try:
            pygame.mixer.music.load(self.file_path)
            pygame.mixer.music.set_volume(self.volume_scale.get() / 100.0)
            pygame.mixer.music.play()
            
            self.is_playing = True
            self.is_paused = False
            self.play_btn.config(text="⏸️ Pause")
            
            # Start position update thread
            self.stop_update = False
            self.update_thread = threading.Thread(target=self.update_position, daemon=True)
            self.update_thread.start()
            
        except Exception as e:
            print(f"Error playing audio: {e}")
    
    def pause(self):
        """Pause playback"""
        if not PYGAME_AVAILABLE:
            return
        
        try:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.play_btn.config(text="▶️ Resume")
        except Exception as e:
            print(f"Error pausing audio: {e}")
    
    def resume(self):
        """Resume playback"""
        if not PYGAME_AVAILABLE:
            return
        
        try:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.play_btn.config(text="⏸️ Pause")
        except Exception as e:
            print(f"Error resuming audio: {e}")
    
    def stop(self):
        """Stop playback"""
        if not PYGAME_AVAILABLE:
            return
        
        try:
            self.stop_update = True
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            self.current_position = 0
            self.play_btn.config(text="▶️ Play")
            
            # Reset position line
            if MATPLOTLIB_AVAILABLE and self.position_line:
                self.position_line.set_xdata([0])
                self.canvas.draw()
            
            self.update_time_label()
            
        except Exception as e:
            print(f"Error stopping audio: {e}")
    
    def set_volume(self, value):
        """Set playback volume"""
        if not PYGAME_AVAILABLE:
            return
        
        try:
            volume = float(value) / 100.0
            pygame.mixer.music.set_volume(volume)
        except Exception as e:
            print(f"Error setting volume: {e}")
    
    def update_position(self):
        """Update playback position (runs in thread)"""
        start_time = time.time()
        
        while not self.stop_update and self.is_playing:
            try:
                # Check if still playing
                if not pygame.mixer.music.get_busy() and not self.is_paused:
                    # Playback finished
                    self.is_playing = False
                    self.play_btn.config(text="▶️ Play")
                    self.current_position = 0
                    break
                
                # Update position
                if not self.is_paused:
                    self.current_position = time.time() - start_time
                    
                    # Update UI
                    self.parent.after(0, self.update_ui_position)
                
                time.sleep(0.1)  # Update every 100ms
                
            except Exception as e:
                print(f"Error updating position: {e}")
                break
    
    def update_ui_position(self):
        """Update UI elements with current position (called from main thread)"""
        # Update time label
        self.update_time_label()
        
        # Update position line on waveform
        if MATPLOTLIB_AVAILABLE and self.position_line and self.duration > 0:
            self.position_line.set_xdata([self.current_position])
            self.canvas.draw_idle()
        
        # Update progress bar (fallback)
        if not MATPLOTLIB_AVAILABLE and hasattr(self, 'progress_bar') and self.duration > 0:
            progress = (self.current_position / self.duration) * 100
            self.progress_bar['value'] = min(100, progress)
    
    def update_time_label(self):
        """Update time display label - compact format"""
        current_min = int(self.current_position // 60)
        current_sec = int(self.current_position % 60)
        total_min = int(self.duration // 60)
        total_sec = int(self.duration % 60)
        
        time_str = f"{current_min}:{current_sec:02d}/{total_min}:{total_sec:02d}"
        self.time_label.config(text=time_str)
    
    def destroy(self):
        """Clean up resources"""
        self.stop_update = True
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.music.stop()
            except:
                pass
