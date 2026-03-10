import customtkinter as ctk
from .base_page import BasePage
from widgets import CTkTreeview
from datetime import datetime, timezone


class Summary(BasePage):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    def make(self):
        self.ship_sum = ShipSummaryTree(self)
        self.ship_sum.grid(
            row=2, column=0, columnspan=2, padx=2, pady=20, sticky="nsew"
        )

        self.contract_sum = ContractTree(self)
        self.contract_sum.grid(row=0, column=1, rowspan=2, sticky="nsew")

        self.Agent_box = Agent_Sum(self, self.app.agent_data_var)
        self.Agent_box.grid(column=0, row=0, rowspan=2, sticky="nsew")

    def on_select(self, callback):
        self.ship_sum.bind(
            "<<TreeviewSelect>>", lambda e: callback(self.ship_sum.selected_ship())
        )

    def refresh(self):
        self.ship_sum.load(list(self.app.ships_data.values()))
        self.contract_sum.load(self.app.contracts_data)


class Agent_Sum(ctk.CTkFrame):
    def __init__(
        self,
        master,
        agent_data,
        width: int = 500,
        height: int = 500,
        **kwargs,
    ):
        super().__init__(
            master,
            width,
            height,
            **kwargs,
        )
        self.columnconfigure(0, weight=1)
        for i in range(0, 11):
            self.rowconfigure(i, weight=1)

        # All the labels for the agent summary with the labels being filled with string vars that have the name of the displayed var added to the front

        header = ctk.CTkLabel(self, text="Agent")
        header.grid(column=0, row=1, sticky="nsew")

        symbol = ctk.CTkLabel(self, textvariable=agent_data["symbol"])
        symbol.grid(column=0, row=2, sticky="nsew")

        credits = ctk.CTkLabel(self, textvariable=agent_data["credits"])
        credits.grid(column=0, row=4, sticky="nsew")

        faction = ctk.CTkLabel(self, textvariable=agent_data["starting_faction"])
        faction.grid(column=0, row=6, sticky="nsew")

        shipcount = ctk.CTkLabel(self, textvariable=agent_data["ship_count"])
        shipcount.grid(column=0, row=8, sticky="nsew")


class ShipSummaryTree(CTkTreeview):
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

    def selected_ship(self) -> dict | None:
        iid = self.focus()
        if not iid:
            return None
        symbol, location, fuel, cooldown = self.item(iid, "values")
        return {
            "symbol": symbol,
            "location": location,
            "fuel": fuel,
            "cooldown": cooldown,
        }

    @staticmethod
    def _fmt_location(ship: dict) -> str:
        nav = ship.get("nav", {})
        status = nav.get("status", "")
        wp = nav.get("waypointSymbol", "?")
        if status == "IN_TRANSIT":
            dest = nav.get("route", {}).get("destination", {}).get("symbol", "?")
            return f"{wp} → {dest}"
        return f"{wp} ({status.replace('_', ' ').title()})"


class ContractTree(CTkTreeview):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("show", "headings")
        super().__init__(
            master,
            columns=("ID", "Type", "Deliver", "Progress", "Deadline", "Status"),
            **kwargs,
        )

        self.tag_configure("odd", background="#1c1c1c", foreground="#dce4ee")
        self.tag_configure("even", background="#242424", foreground="#dce4ee")

        for col, (width, anchor) in [
            ("ID", (160, "w")),
            ("Type", (110, "w")),
            ("Deliver", (180, "w")),
            ("Progress", (100, "center")),
            ("Deadline", (140, "center")),
            ("Status", (90, "center")),
        ]:
            self.heading(col, text=col)
            self.column(col, width=width, anchor=anchor)

    def load(self, contracts: list[dict]):
        for row in self.get_children():
            self.delete(row)
        for i, c in enumerate(contracts):
            deliver = c.get("terms", {}).get("deliver", [{}])[0]
            dt_raw = c.get("terms", {}).get("deadline", "")
            try:
                dt = datetime.fromisoformat(dt_raw.replace("Z", "+00:00"))
                secs = max(0, int((dt - datetime.now(timezone.utc)).total_seconds()))
                h, m = divmod(secs // 60, 60)
                deadline = f"{h}h {m}m"
            except (ValueError, AttributeError):
                deadline = "—"
            self.insert(
                "",
                "end",
                tags=("odd" if i % 2 == 0 else "even",),
                values=(
                    c.get("id", "—"),
                    c.get("type", "—").title(),
                    f"{deliver.get('tradeSymbol', '?')} → {deliver.get('destinationSymbol', '?')}",
                    f"{deliver.get('unitsFulfilled', 0)} / {deliver.get('unitsRequired', '?')}",
                    deadline,
                    "✅ Done"
                    if c.get("fulfilled")
                    else "🔄 Active"
                    if c.get("accepted")
                    else "📋 Open",
                ),
            )

    def selected_contract(self) -> dict | None:
        iid = self.focus()
        if not iid:
            return None
        id_, type_, deliver, progress, deadline, status = self.item(iid, "values")
        return {
            "id": id_,
            "type": type_,
            "deliver": deliver,
            "progress": progress,
            "deadline": deadline,
            "status": status,
        }
