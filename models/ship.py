class Ship:
    def __init__(self, data, container, key, table=None):
        self.container = container
        self.key = key
        self.table = table
        self.deleted = False

        self.update(data)

    def update(self, data):
        self.symbol = data.get("symbol")

        reg = data.get("registration", {})
        self.name = reg.get("name")
        self.faction = reg.get("factionSymbol")
        self.role = reg.get("role")

        nav = data.get("nav", {})
        self.system = nav.get("systemSymbol")
        self.waypoint = nav.get("waypointSymbol")
        self.status = nav.get("status")
        self.flight_mode = nav.get("flightMode")

        route = nav.get("route", {})
        dest = route.get("destination", {})
        self.route_dest_symbol = dest.get("symbol")
        self.route_dest_type = dest.get("type")
        self.route_departure = route.get("departureTime")
        self.route_arrival = route.get("arrival")

        frame = data.get("frame", {})
        self.frame_name = frame.get("name")
        self.frame_condition = frame.get("condition")

        reactor = data.get("reactor", {})
        self.reactor_name = reactor.get("name")
        self.reactor_power = reactor.get("powerOutput")

        engine = data.get("engine", {})
        self.engine_name = engine.get("name")
        self.engine_speed = engine.get("speed")

        cargo = data.get("cargo", {})
        self.cargo_capacity = cargo.get("capacity")
        self.cargo_units = cargo.get("units")

        fuel = data.get("fuel", {})
        self.fuel_current = fuel.get("current")
        self.fuel_capacity = fuel.get("capacity")

        cooldown = data.get("cooldown", {})
        self.cooldown_remaining = cooldown.get("remainingSeconds")
        self.cooldown_expiration = cooldown.get("expiration")

    # removed from container and table
    def delete(self):
        if isinstance(self.container, dict):
            self.container.pop(self.key, None)
        elif isinstance(self.container, list):
            try:
                self.container.remove(self)
            except ValueError:
                pass

        self.deleted = True

        # Refresh table
        if self.table:
            if isinstance(self.container, dict):
                rows = [s.table_row() for s in self.container.values()]
            else:
                rows = [s.table_row() for s in self.container]
            self.table.update_rows(rows)

    def table_row(self):
        return [
            str(self.symbol),
            str(self.name),
            str(self.faction),
            str(self.role),
            str(self.system),
            str(self.waypoint),
            str(self.status),
            str(self.flight_mode),
            str(self.route_dest_symbol),
            str(self.route_dest_type),
            str(self.route_departure),
            str(self.route_arrival),
            str(self.frame_name),
            str(self.frame_condition),
            str(self.reactor_name),
            str(self.reactor_power),
            str(self.engine_name),
            str(self.engine_speed),
            str(self.cargo_capacity),
            str(self.cargo_units),
            str(self.fuel_current),
            str(self.fuel_capacity),
            str(self.cooldown_remaining),
            str(self.cooldown_expiration),
        ]
