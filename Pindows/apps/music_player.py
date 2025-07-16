import tkinter as tk
from tkinter import filedialog
import pygame
import time
import threading
import os
from utils.system import shutdown_pindows

pygame.mixer.init()

def content_music_player(frame, root):
    current_file = tk.StringVar(value="No file selected")
    time_label = tk.StringVar(value="00:00 / 00:00")
    is_paused = [False]
    duration = [0]
    special_file = "dSmd8Co.mp3"

    def format_time(seconds):
        minutes = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{minutes:02}:{secs:02}"

    def goodbye():
        shutdown_pindows(root)  # ← usar root como argumento

    def update_time():
        while pygame.mixer.music.get_busy():
            if not is_paused[0]:
                current_pos = pygame.mixer.music.get_pos() // 1000
                total = duration[0]
                time_label.set(f"{format_time(current_pos)} / {format_time(total)}")
        # Después de terminar la canción
        if "dSmd8Co.mp3" in current_file.get():
            print("\n\'Change Da World\',\nmy final message...\nGOODBYE\n    Moises I.")
            goodbye()

        # Solo se llama si terminó completamente
        if current_file.get().endswith(special_file):
            goodbye()

    def load_and_play():
        file = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])

        if file:
            try:
                pygame.mixer.music.load(file)
                pygame.mixer.music.play()
                current_file.set(f"Now Playing: {os.path.basename(file)}")
                is_paused[0] = False

                duration[0] = 300  # Estimación temporal

                time_label.set("00:00 / ??")
                threading.Thread(target=update_time, daemon=True).start()
            except Exception as e:
                current_file.set(f"Error: {e}")

    def stop():
        pygame.mixer.music.stop()
        current_file.set("Stopped")
        time_label.set("00:00 / 00:00")

    def pause_resume():
        if pygame.mixer.music.get_busy():
            if is_paused[0]:
                pygame.mixer.music.unpause()
                is_paused[0] = False
                pause_btn.config(text="Pause")
            else:
                pygame.mixer.music.pause()
                is_paused[0] = True
                pause_btn.config(text="Resume")

    # UI
    tk.Label(frame, textvariable=current_file, bg="#eeeeee").pack(fill="x", pady=5)
    tk.Label(frame, textvariable=time_label, font=("Consolas", 12)).pack()

    controls = tk.Frame(frame)
    controls.pack(pady=10)

    tk.Button(controls, text="Open & Play", command=load_and_play).grid(row=0, column=0, padx=5)
    pause_btn = tk.Button(controls, text="Pause", command=pause_resume)
    pause_btn.grid(row=0, column=1, padx=5)
    tk.Button(controls, text="Stop", command=stop).grid(row=0, column=2, padx=5)
