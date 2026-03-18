from .base_page import BasePage
from widgets import CTkTreeview
import customtkinter as ctk
from Utils import systems_waypoints_data, navigate, orbit, dock, extract, jettison


class Ship(BasePage):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        for i in range(0, 6):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i, weight=1)

    def make(self):

        self.system_info = []
        self.current_ship = {}

        self.bottom_bar = SelectionBar(self)
        self.bottom_bar.grid(column=0, row=6, columnspan=6, sticky="ew")

        self.Cargo_label = ctk.CTkLabel(self, text="Cargo", font=ctk.CTkFont(size=20))
        self.Cargo_label.grid(column=0, row=0)
        self.Cargo = CargoTree(self)
        self.Cargo.grid(row=1, column=0, columnspan=1, sticky="nsew")

        self.waypoints_label = ctk.CTkLabel(
            self, text="waypoints", font=ctk.CTkFont(size=20)
        )
        self.waypoints_label.grid(column=0, row=2)
        self.waypoints = WaypointTree(self)
        self.waypoints.grid(row=3, column=0, columnspan=1, sticky="nsew")

        self.ActionMenu = ActionMenu(self)
        self.ActionMenu.grid(column=3, columnspan=6, row=1, rowspan=3, sticky="nsew")


class SelectionBar(ctk.CTkFrame):
    def __init__(
        self,
        master,
        **kwargs,
    ):
        super().__init__(
            master,
            **kwargs,
        )

        self.app = master.app

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.shipselector = ctk.CTkComboBox(
            self,
            height=20,
            variable=ctk.StringVar(),
        )
        self.shipselector.grid(
            column=0, row=0, columnspan=3, padx=5, pady=5, sticky="ew"
        )
        self.shipselector.bind("<Return>", lambda event: self.selectship())

        self.selectshipbutton = ctk.CTkButton(
            self, text="Select Ship", command=self.selectship
        )
        self.selectshipbutton.grid(column=3, row=0)

    def selectship(self):
        self.app.selected_ship = self.shipselector.get()
        self.master.current_ship = self.app.ships_data[self.app.selected_ship]

        self.master.Cargo.load(self.master.current_ship)
        self.master.ActionMenu.load(self.master.current_ship)

        self.master.system_info = systems_waypoints_data(
            self.app.player_token.get(), self.master.current_ship["nav"]["systemSymbol"]
        )
        self.master.waypoints.load(self.master.system_info)

    def update_ship_selecter_combobox(self):

        ship = self.app.ships_data
        ships_list = sorted(ship.keys(), key=str.casefold)
        self.shipselector.configure(values=ships_list)


class ActionMenu(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = master.app

        for i in range(10):
            self.columnconfigure(i, weight=1)
        for i in range(6):
            self.rowconfigure(i, weight=1)

        # Row 0: Status bar
        self.status_bar = ShipStatusBar(self)
        self.status_bar.grid(
            column=0, row=0, columnspan=10, padx=5, pady=5, sticky="ew"
        )

        # Row 1: Navigate
        self.waypoint_selector = ctk.CTkEntry(self, placeholder_text="Waypoint Symbol")
        self.waypoint_selector.grid(
            column=0, row=1, columnspan=7, padx=5, pady=5, sticky="ew"
        )
        ctk.CTkButton(self, text="Navigate", command=self.navigate_).grid(
            column=7, row=1, columnspan=3, padx=5, pady=5, sticky="ew"
        )

        # Row 2: Orbit
        ctk.CTkButton(self, text="Orbit", command=self.orbit_).grid(
            column=0, row=2, columnspan=10, padx=5, pady=5, sticky="ew"
        )

        # Row 3: Dock
        ctk.CTkButton(self, text="Dock", command=self.dock_).grid(
            column=0, row=3, columnspan=10, padx=5, pady=5, sticky="ew"
        )

        # Row 4: Extract
        ctk.CTkButton(self, text="Extract", command=self.extract_).grid(
            column=0, row=4, columnspan=10, padx=5, pady=5, sticky="ew"
        )

        # Row 5: Jettison
        self.jettison_symbol = ctk.CTkEntry(self, placeholder_text="Trade Symbol")
        self.jettison_symbol.grid(
            column=0, row=5, columnspan=4, padx=5, pady=5, sticky="ew"
        )
        self.jettison_units = ctk.CTkEntry(self, placeholder_text="Units")
        self.jettison_units.grid(
            column=4, row=5, columnspan=3, padx=5, pady=5, sticky="ew"
        )
        ctk.CTkButton(self, text="Jettison", command=self.jettison_).grid(
            column=7, row=5, columnspan=3, padx=5, pady=5, sticky="ew"
        )

    def _token(self):
        return self.app.player_token.get()

    def _ship(self):
        return self.master.current_ship["symbol"]

    def load(self, ship: dict):
        self.status_bar.load(ship)

    def navigate_(self):
        navigate(self._token(), self._ship(), self.waypoint_selector.get())

    def orbit_(self):
        orbit(self._token(), self._ship())

    def dock_(self):
        dock(self._token(), self._ship())

    def extract_(self):
        extract(self._token(), self._ship())

    def jettison_(self):
        print(
            jettison(
                self._token(),
                self._ship(),
                self.jettison_symbol.get().replace(" ", "_").upper(),
                int(self.jettison_units.get()),
            )
        )


class ShipStatusBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        for i in range(12):
            self.columnconfigure(i, weight=1)

        ctk.CTkLabel(self, text="Location").grid(column=0, row=0, padx=5, pady=5)
        ctk.CTkLabel(self, text="Status").grid(column=2, row=0, padx=5, pady=5)
        ctk.CTkLabel(self, text="Fuel").grid(column=4, row=0, padx=5, pady=5)
        ctk.CTkLabel(self, text="Cooldown").grid(column=6, row=0, padx=5, pady=5)
        ctk.CTkLabel(self, text="Cargo").grid(column=8, row=0, padx=5, pady=5)

        self.location_val = ctk.CTkLabel(self, text="—")
        self.status_val = ctk.CTkLabel(self, text="—")
        self.fuel_val = ctk.CTkLabel(self, text="—")
        self.cooldown_val = ctk.CTkLabel(self, text="—")
        self.cargo_val = ctk.CTkLabel(self, text="—")

        self.location_val.grid(column=1, row=0, padx=5, pady=5)
        self.status_val.grid(column=3, row=0, padx=5, pady=5)
        self.fuel_val.grid(column=5, row=0, padx=5, pady=5)
        self.cooldown_val.grid(column=7, row=0, padx=5, pady=5)
        self.cargo_val.grid(column=9, row=0, padx=5, pady=5)

    def load(self, ship: dict):
        from datetime import datetime, timezone

        nav = ship["nav"]
        fuel = ship["fuel"]
        cargo = ship["cargo"]
        secs = ship["cooldown"]["remainingSeconds"]

        if nav["status"] == "IN_TRANSIT":
            try:
                arr = datetime.fromisoformat(
                    nav["route"]["arrival"].replace("Z", "+00:00")
                )
                secs = max(0, int((arr - datetime.now(timezone.utc)).total_seconds()))
            except (ValueError, AttributeError):
                pass

        self.location_val.configure(text=nav["waypointSymbol"])
        self.status_val.configure(text=nav["status"].replace("_", " ").title())
        self.fuel_val.configure(text=f"{fuel['current']} / {fuel['capacity']}")
        self.cooldown_val.configure(text=f"{secs}s" if secs > 0 else "Ready")
        self.cargo_val.configure(text=f"{cargo['units']} / {cargo['capacity']}")


class CargoTree(CTkTreeview):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("show", "headings")
        super().__init__(master, columns=("Item", "Units"), **kwargs)

        self.tag_configure("odd", background="#1c1c1c", foreground="#dce4ee")
        self.tag_configure("even", background="#242424", foreground="#dce4ee")

        self.heading("Item", text="Item")
        self.heading("Units", text="Units")
        self.column("Item", width=200, anchor="w")
        self.column("Units", width=80, anchor="center")

    def load(self, ship: dict):
        for row in self.get_children():
            self.delete(row)
        cargo = ship.get("cargo", {})
        for i, item in enumerate(cargo.get("inventory", [])):
            self.insert(
                "",
                "end",
                tags=("odd" if i % 2 == 0 else "even",),
                values=(
                    item.get("name", item.get("symbol", "—")),
                    item.get("units", 0),
                ),
            )


class WaypointTree(CTkTreeview):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("show", "headings")
        super().__init__(
            master, columns=("Symbol", "Type", "Faction", "Traits"), **kwargs
        )

        self.tag_configure("odd", background="#1c1c1c", foreground="#dce4ee")
        self.tag_configure("even", background="#242424", foreground="#dce4ee")

        for col, (width, anchor) in [
            ("Symbol", (160, "w")),
            ("Type", (160, "w")),
            ("Faction", (90, "center")),
            ("Traits", (300, "w")),
        ]:
            self.heading(col, text=col)
            self.column(col, width=width, anchor=anchor)

    def load(self, waypoints: list[dict]):
        for row in self.get_children():
            self.delete(row)
        for i, wp in enumerate(waypoints):
            tag = "odd" if i % 2 == 0 else "even"
            traits = wp.get("traits", [])
            parent = self.insert(
                "",
                "end",
                tags=(tag,),
                open=False,
                values=(
                    wp.get("symbol", "—"),
                    wp.get("type", "—").replace("_", " ").title(),
                    wp.get("faction", {}).get("symbol", "—"),
                    ", ".join(t["name"] for t in traits),
                ),
            )
            for trait in traits:
                self.insert(
                    parent,
                    "end",
                    tags=(tag,),
                    values=(
                        "",
                        trait.get("name", ""),
                        "",
                        trait.get("description", ""),
                    ),
                )

    def selected_waypoint(self) -> str | None:
        iid = self.focus()
        if not iid:
            return None
        return self.item(iid, "values")[0] or self.item(self.parent(iid), "values")[0]
