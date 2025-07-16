import tkinter as tk
from tkinter import filedialog, messagebox
import os

def content_text_processor(frame):
    text = tk.Text(frame, wrap="word")
    text.pack(expand=True, fill="both", padx=5, pady=5)

    def save_file():
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write(text.get("1.0", "end-1c"))
            messagebox.showinfo("Saved", f"File saved to {file}")

    def load_file():
        file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file:
            with open(file, "r", encoding="utf-8") as f:
                text.delete("1.0", "end")
                text.insert("1.0", f.read())

    toolbar = tk.Frame(frame, bg="#dddddd")
    toolbar.pack(fill="x")
    tk.Button(toolbar, text="Open", command=load_file).pack(side="left", padx=2, pady=2)
    tk.Button(toolbar, text="Save", command=save_file).pack(side="left", padx=2, pady=2)

def content_file_explorer(frame, create_window_callback):
    current_path = tk.StringVar()
    history = []

    listbox = tk.Listbox(frame)
    listbox.pack(fill="both", expand=True, padx=30, pady=5)

    path_label = tk.Label(frame, textvariable=current_path, bg="white", anchor="w")
    path_label.pack(fill="x")

    def load_directory(path):
        try:
            entries = os.listdir(path)
        except PermissionError:
            return

        listbox.delete(0, "end")
        current_path.set(path)
        for item in entries:
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                listbox.insert("end", f"[DIR] {item}")
            else:
                listbox.insert("end", item)

    def on_item_double_click(event):
        selection = listbox.curselection()
        if not selection:
            return
        item_text = listbox.get(selection[0])
        name = item_text.replace("[DIR] ", "")
        new_path = os.path.join(current_path.get(), name)
        if os.path.isdir(new_path):
            history.append(current_path.get())
            load_directory(new_path)
        elif new_path.endswith(".txt"):
            try:
                with open(new_path, "r", encoding="utf-8") as f:
                    content = f.read()
                # Abrir en nueva ventana de texto
                def text_window_content(frame):
                    text = tk.Text(frame, wrap="word")
                    text.insert("1.0", content)
                    text.pack(expand=True, fill="both", padx=5, pady=5)
                create_window_callback(f"Viewing: {name}", text_window_content)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file:\n{e}")

    def go_back():
        if history:
            previous = history.pop()
            load_directory(previous)

    def choose_start_folder():
        start_path = filedialog.askdirectory()
        if start_path:
            history.clear()
            load_directory(start_path)

    # Top toolbar
    toolbar = tk.Frame(frame)
    toolbar.pack(fill="x")
    tk.Button(toolbar, text="Browse", command=choose_start_folder).pack(side="left", padx=2)
    tk.Button(toolbar, text="Back", command=go_back).pack(side="left", padx=2)

    listbox.bind("<Double-Button-1>", on_item_double_click)

    # Start with user's home directory
    load_directory(os.path.expanduser("~"))
