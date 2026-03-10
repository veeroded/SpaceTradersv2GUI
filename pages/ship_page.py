import customtkinter as ctk
from .base_page import BasePage
from widgets import CTkTreeview


class Ship(BasePage):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    def make(self):
        self.shipselector = ctk.CTkComboBox(
            self,
            height=20,
            variable=self.app.selected_ship_var,
            command=self.selectship(),
        )
        self.shipselector.grid(
            row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.shipselector.bind("<Return>", lambda event: self.login_agent())

    def selectship(self):
        print("Hello World")


class Cargo(CTkTreeview):
    _COLS = ("Symbol", "Location", "Fuel", "Cooldown")
    _COL_CFG = {
        "Symbol": (110, "w"),
        "Location": (240, "w"),
        "Fuel": (110, "center"),
        "Cooldown": (100, "center"),
    }

    def __init__(self, master, **kwargs):
        kwargs.setdefault("show", "headings")
        super().__init__(master, columns=self._COLS, **kwargs)

        self.tag_configure("odd", background="#1c1c1c", foreground="#dce4ee")
        self.tag_configure("even", background="#242424", foreground="#dce4ee")

        for col, (width, anchor) in self._COL_CFG.items():
            self.heading(col, text=col)
            self.column(col, width=width, anchor=anchor)

    def load(self, ships: list[dict]):
        for row in self.get_children():
            self.delete(row)
        for i, ship in enumerate(ships):
            fuel = ship.get("fuel", {})
            nav = ship.get("nav", {})
            secs = ship.get("cooldown", {}).get("remainingSeconds", 0)

            # If true it then calculates the amount of time in seconds it would take for the journy to be complete
            if nav.get("status") == "IN_TRANSIT":
                arrival = nav.get("route", {}).get("arrival", "")
                try:
                    # Converting zulu time to utc
                    arr = datetime.fromisoformat(arrival.replace("Z", "+00:00"))
                    secs = max(
                        0, int((arr - datetime.now(timezone.utc)).total_seconds())
                    )
                except (ValueError, AttributeError):
                    pass

            self.insert(
                "",
                "end",
                tags=("odd" if i % 2 == 0 else "even",),
                values=(
                    ship.get("symbol", "—"),
                    self._fmt_location(ship),
                    f"{fuel.get('current', '?')} / {fuel.get('capacity', '?')}",
                    f"{secs}s" if secs > 0 else "Ready",
                ),
            )
