import customtkinter as ctk
from Utils import istimepassed


class Contract:
    def __init__(self, data, container, key, table=None):
        self.container = container
        self.key = key
        self.table = table  # CTkTable to update on deletion
        self.deleted = False
        self.frame = None  # optional frame

        self.update_from_api(data)

    def update_from_api(self, data):
        self.id = data.get("id")
        self.faction_symbol = data.get("factionSymbol")
        self.type = data.get("type")

        terms = data.get("terms", {})
        payment = terms.get("payment", {})
        deliver = terms.get("deliver", {})

        self.deadline = terms.get("deadline")
        self.payment_on_accept = payment.get("onAccepted")
        self.payment_on_fulfilled = payment.get("onFulfilled")

        self.good = deliver.get("tradeSymbol")
        self.destination = deliver.get("destinationSymbol")
        self.good_required = deliver.get("unitsRequired")
        self.good_fulfilled = deliver.get("unitsFulfilled")

        self.accept_deadline = data.get("acceptDeadline")
        self.accepted = data.get("accepted")
        self.fulfilled = data.get("fulfilled")

        self.check_expired()

    def check_expired(self):
        if self.deadline and istimepassed(self.deadline):
            self.delete()
            return True
        return False

    # Removes itself from the container
    def delete(self):
        if isinstance(self.container, dict):
            self.container.pop(self.key, None)
        elif isinstance(self.container, list):
            try:
                self.container.remove(self)
            except ValueError:
                pass

        self.deleted = True

        # Update table
        if self.table:
            if isinstance(self.container, dict):
                rows = [c.table_row() for c in self.container.values()]
            else:
                rows = [c.table_row() for c in self.container]
            self.table.update_rows(rows)

    def table_row(self):
        return [
            str(self.id),
            str(self.faction_symbol),
            str(self.type),
            str(self.deadline),
            str(self.payment_on_accept),
            str(self.payment_on_fulfilled),
            str(self.good),
            str(self.destination),
            str(self.good_required),
            str(self.good_fulfilled),
            str(self.accept_deadline),
            str(self.accepted),
            str(self.fulfilled),
        ]
