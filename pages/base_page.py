from typing import TYPE_CHECKING
import customtkinter as ctk

if TYPE_CHECKING:
    from app import App


class BasePage(ctk.CTkFrame):
    app: "App"

    def __init__(self, parent, app: "App", **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app

        # 2x2 should be enough so long as i use frames
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.make()

    def make(self):
        # Just need to overide stuff here to make it page specific
        raise NotImplementedError
