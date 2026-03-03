import customtkinter as ctk


class Contract:
    def __init__(self, data):
        self.id = ctk.StringVar(value=data["id"])
        self.faction_symbol = ctk.StringVar(value=data["id"])
        self.type = ctk.StringVar(value=data["id"])

        self.deadline = ctk.StringVar(value=data["terms"]["deadline"])
        self.payment_on_accept = ctk.StringVar(value=data["terms"]["payment"]["onAccepted"])
        self.payment_on_funfilled = ctk.StringVar(value=data["terms"]["payment"]["onFufilled"])
        self.goods = ctk.StringVar(value=data["terms"]["deliver"]["tradeSymbol"])
        self.goods = ctk.StringVar(value=data["terms"]["deliver"]["destinationSymbol"])
        self.goods = ctk.StringVar(value=str(data["terms"]["deliver"]["unitsRequired"]))
        self.goods = ctk.StringVar(value=data["terms"]["deliver"]["unitsFufilled"])
    def update(self, data):
        
