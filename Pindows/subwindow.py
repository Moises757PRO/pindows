import tkinter as tk

class SubWindow(tk.Frame):
    def __init__(self, master, title="Subwindow", bg_color="lightblue", content_func=None, on_minimize=None, **kwargs):
        super().__init__(master, **kwargs)
        self.title = title
        self.on_minimize = on_minimize
        self["bg"] = bg_color
        self["bd"] = 2
        self["relief"] = "raised"

        # Title bar (header)
        title_bar = tk.Frame(self, bg=bg_color)
        title_bar.pack(fill="x")

        # Title label
        tk.Label(title_bar, text=title, bg=bg_color, font=("Arial", 11, "bold")).pack(side="left", padx=5)

        # Minimize button
        tk.Button(title_bar, text="–", width=2, command=self.minimize).pack(side="right", padx=2)

        # Close button
        tk.Button(title_bar, text="✕", width=2, command=self.destroy).pack(side="right", padx=2)

        # Inner content area
        self.inner_frame = tk.Frame(self, bg="white", bd=1, relief="sunken")
        self.inner_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Insert user content
        if content_func:
            content_func(self.inner_frame)
        else:
            tk.Label(self.inner_frame, text="No content provided", bg="white").pack(pady=5)

        # Draggable behavior only via title bar
        def bind_drag(widget):
            widget.bind("<Button-1>", self.start_move)
            widget.bind("<B1-Motion>", self.do_move)

        bind_drag(title_bar)
        for child in title_bar.winfo_children():
            bind_drag(child)

        self._x = 0
        self._y = 0

    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def do_move(self, event):
        dx = event.x - self._x
        dy = event.y - self._y
        x = self.winfo_x() + dx
        y = self.winfo_y() + dy
        self.place(x=x, y=y)

    def minimize(self):
        self.place_forget()
        if self.on_minimize:
            self.on_minimize(self)
