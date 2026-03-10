from tkinter import ttk

_STYLE_APPLIED = False


def _apply_ctk_style():
    global _STYLE_APPLIED
    if _STYLE_APPLIED:
        return
    s = ttk.Style()
    s.theme_use("default")
    s.configure(
        "CTk.Treeview",
        background="#1c1c1c",
        foreground="#dce4ee",
        fieldbackground="#1c1c1c",
        borderwidth=0,
        relief="flat",
        rowheight=28,
        font=("Segoe UI", 12),
    )
    s.map(
        "CTk.Treeview",
        background=[("selected", "#1f538d")],
        foreground=[("selected", "#ffffff")],
    )
    s.configure(
        "CTk.Treeview.Heading",
        background="#333333",
        foreground="#dce4ee",
        borderwidth=0,
        relief="flat",
        font=("Segoe UI", 12, "bold"),
        padding=(8, 6),
    )
    s.map(
        "CTk.Treeview.Heading",
        background=[("active", "#3d3d3d"), ("pressed", "#3d3d3d")],
        relief=[("active", "flat"), ("pressed", "flat")],
    )
    _STYLE_APPLIED = True


class CTkTreeview(ttk.Treeview):
    def __init__(self, master, **kwargs):
        _apply_ctk_style()
        kwargs.setdefault("style", "CTk.Treeview")
        super().__init__(master, **kwargs)
