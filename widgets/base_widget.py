# base_widget.py
from __future__ import annotations
from typing import TYPE_CHECKING
import customtkinter as ctk

if TYPE_CHECKING:
    from app import App


class BaseWidget(ctk.CTkFrame):
    app: "App"

    def __init__(self, parent, app: "App", **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
