import customtkinter as ctk
from .base_page import BasePage

class Summary(BasePage):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    def  make(self):
        self.box = ctk.CTkTextbox(self, width=200, height=200, activate_scrollbars = False)
        self.box.insert("0.0", "hi")
        self.box.grid(column=0, row = 0)
