import customtkinter as ctk


class Ship:
    def __init__(self, data):
        self.symbol = ctk.StringVar(value=data["symbol"])
        self.role = ctk.StringVar(value=data["registration"]["role"])
        self.fuel = ctk.StringVar(value=str(data["fuel"]["current"]))
        self.fuelcap = ctk.StringVar(value=str(data["fuel"]["current"]))
        self.status = ctk.StringVar(value=data["nav"]["status"])

    def update(self, data):
        self.fuel.set(str(data["fuel"]["current"]))
        self.status.set(data["nav"]["status"])
