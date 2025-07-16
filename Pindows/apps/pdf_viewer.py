import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import fitz  # PyMuPDF

def content_pdf_reader(master):
    frame = tk.Frame(master, bg="white")
    frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame, bg="white")
    v_scroll = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    h_scroll = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

    v_scroll.pack(side="right", fill="y")
    h_scroll.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)

    inner_frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")
    inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    images = []  # Para que no se borren de memoria
    doc = None   # El documento PDF
    zoom_level = tk.DoubleVar(value=2.0)  # Nivel de zoom inicial

    def render_pages():
        nonlocal images
        for widget in inner_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()
        images.clear()

        if not doc:
            return

        for page in doc:
            zoom = zoom_level.get()
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            tk_img = ImageTk.PhotoImage(img)
            label = tk.Label(inner_frame, image=tk_img, bg="white")
            label.image = tk_img
            images.append(tk_img)
            label.pack(pady=5)

    def open_pdf():
        nonlocal doc
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            doc = fitz.open(file_path)
            render_pages()

    zoom_slider = tk.Scale(inner_frame, from_=0.5, to=4.0, resolution=0.1,
                           orient="horizontal", label="Zoom", variable=zoom_level,
                           command=lambda _: render_pages())
    zoom_slider.pack(pady=10)

    open_button = tk.Button(inner_frame, text="Abrir PDF", command=open_pdf)
    open_button.pack(pady=10)
