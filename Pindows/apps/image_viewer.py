import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def content_image_viewer(frame):
    label = tk.Label(frame)
    label.pack(expand=True, fill="both")

    def open_image():
        file = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")])
        if file:
            try:
                img = Image.open(file)
                img.thumbnail((frame.winfo_width(), frame.winfo_height()))
                photo = ImageTk.PhotoImage(img)
                label.config(image=photo)
                label.image = photo
            except Exception as e:
                label.config(text=f"Failed to open image: {e}", image="")

    btn = tk.Button(frame, text="Open Image", command=open_image)
    btn.pack(pady=5)
