import tkinter as tk

def content_window_builder(frame, master):
    frame.configure(bg="#f0f0f0")

    tk.Label(frame, text="Window Title:").pack(pady=5)
    title_entry = tk.Entry(frame)
    title_entry.pack(pady=5)

    def create_subwindow():
        title = title_entry.get().strip()
        if not title:
            title = "Untitled"

        from subwindow import SubWindow  # Import dentro de la función para evitar bucles
        SubWindow(
            master=master,
            title=title,
            width=300,
            height=180,
            bg="#ffffff",
            make_content=lambda f: tk.Label(f, text="This is your new window!", bg="white").pack(padx=10, pady=10)
        )

    tk.Button(frame, text="Create", command=create_subwindow).pack(pady=10)
