from __future__ import annotations

import customtkinter as ctk
from .base_page import BasePage
import os
import requests
import json


class Login(BasePage):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, app=app, **kwargs)

    def make(self):

        self.loginF = ctk.CTkFrame(self)
        self.id_login = ctk.CTkComboBox(
            self, height=20, variable=self.app.player_login, command=self.login_agent
        )
        self.id_login.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.id_login.bind("<Return>", lambda event: self.login_agent())
        self.generate_login_combobox(0)

    def load_player_logins(self):
        known_agents = {}

        if os.path.exists(self.app.agentfile):
            with open(self.app.agentfile) as json_agents:
                known_agents = json.load(json_agents)
        return known_agents

    def store_agent_login(self, json_result):
        known_agents = self.load_player_logins()
        known_agents[json_result["symbol"]] = json_result["token"]
        with open(self.app.agentfile, "w") as json_agents:
            json.dump(known_agents, json_agents)

    def generate_login_combobox(self, value):
        known_agents = self.load_player_logins()
        self.agent_list = sorted(known_agents.keys(), key=str.casefold)
        self.id_login.configure(values=self.agent_list)

    def login_agent(self, *args):
        selected = self.id_login.get()
        known_agents = self.load_player_logins()

        if selected in known_agents:
            self.app.player_token.set(known_agents[selected])
        else:
            self.app.player_token.set(selected)

        print(self.app.player_token.get())
        try:
            response = requests.get(
                self.app.endpoints["MY_ACCOUNT"],
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.app.player_token.get()}",
                },
            )
            if response.status_code == 200:
                result = response.json()
                # used to hold the token for later
                result["data"]["token"] = self.app.player_token.get()
                self.show_agent_summary(result["data"])
                # print(result)

                # -1, so now store the agent name / token for future runs
                if self.id_login.get() == -1:
                    self.store_agent_login(result["data"])

            else:
                print("Failed:", response.status_code, response.reason, response.text)

        except ConnectionError as ce:
            print("Failed:", ce)

    def show_agent_summary(self, json_result):
        self.app.login_tab_lock()

        self.app.player_token.set(json_result["token"])
        self.app.player_login.set(json_result["symbol"])
        self.app.player_faction.set(
            self.get_faction_lookups()[json_result["startingFaction"]]
        )
        self.app.layer_worth.set(f"{json_result['credits']:n}")

    # Deprectaed
    def logout_agent(self):
        tabs.tab(0, state=tk.NORMAL)
        tabs.tab(1, state=tk.DISABLED)
        tabs.tab(2, state=tk.DISABLED)

        player_login.set("")
        player_token.set("")

        tabs.select(0)
