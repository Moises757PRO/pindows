import tkinter as tk
from subwindow import SubWindow
from PIL import Image, ImageTk

from explorer import content_text_processor, content_file_explorer
from apps.image_viewer import content_image_viewer
from apps.music_player import content_music_player
from apps.window_builder import content_window_builder
from apps.pdf_viewer import content_pdf_reader
from apps.minesweeper import content_minesweeper


# --- Ventana Principal ---
root = tk.Tk()
root.geometry("900x600")
root.title("Pindows")
root.configure(bg="#3d87f5")

# --- Barra de tareas ---
taskbar = tk.Frame(root, bg="#0367fc", height=40)
taskbar.pack(side="bottom", fill="x")

minimized = {}

# --- Restaurar ventana minimizada ---
def restore_window(win):
    win.place(x=100, y=80)
    btn = minimized.pop(win)
    btn.destroy()

# --- Crear ventana nueva ---
def create_window(title, content_func):
    def on_minimize(win):
        btn = tk.Button(taskbar, text=win.title, command=lambda: restore_window(win))
        btn.pack(side="left", padx=3, pady=5)
        minimized[win] = btn

    def final_content(frame):
        if content_func == content_file_explorer:
            content_func(frame, create_window)
        else:
            content_func(frame)

    sub = SubWindow(
        master=root,
        title=title,
        bg_color="#fcba03",
        content_func=final_content,
        on_minimize=on_minimize,
        width=400,
        height=300
    )
    sub.place(x=100, y=80)

# --- Funciones de control del sistema ---
def shutdown():
    root.destroy()

def refresh():
    # Cierra ventanas minimizadas
    for win in list(minimized.keys()):
        btn = minimized.pop(win)
        btn.destroy()
        win.destroy()

    # Cierra todas las ventanas activas
    for widget in root.winfo_children():
        if isinstance(widget, SubWindow):
            widget.destroy()

# --- Menú emergente del botón Start ---
start_menu = tk.Menu(root, tearoff=0, bg="#faa911")
start_menu.add_command(label="Text Processor", command=lambda: create_window("Text Editor", content_text_processor))
start_menu.add_command(label="File Explorer", command=lambda: create_window("File Explorer", content_file_explorer))
start_menu.add_command(label="Image Viewer", command=lambda: create_window("Image Viewer", content_image_viewer))
start_menu.add_command(label="Music Player", command=lambda: create_window("Music Player", lambda f: content_music_player(f, root)))
start_menu.add_command(label="Window Builder", command=lambda: create_window("Window Builder", content_window_builder))
start_menu.add_command(label="PDF Reader", command=lambda: create_window("PDF Reader", content_pdf_reader))

start_menu.add_separator()

start_menu.add_command(label="💣 Minesweeper", command=lambda: create_window("Minesweeper", content_minesweeper))

start_menu.add_separator()

start_menu.add_command(label="Refresh", command=refresh)
start_menu.add_command(label="Shutdown", command=shutdown)


# --- Botón Start ---
def show_start_menu(event):
    start_menu.tk_popup(event.x_root, event.y_root)

start_btn = tk.Button(taskbar, text="Start", width=8)
start_btn.pack(side="left", padx=5, pady=5)
start_btn.bind("<Button-1>", show_start_menu)

# --- Iniciar la app ---
root.mainloop()

#Travieso! Te has metido en estos archivos