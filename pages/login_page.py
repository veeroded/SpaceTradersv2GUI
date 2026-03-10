import customtkinter as ctk
from .base_page import BasePage
import os
from Utils import data_sync
import requests
import json
import threading


class Login(BasePage):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, app=app, **kwargs)

    def make(self):

        self.loginF = ctk.CTkFrame(self)
        self.id_login = ctk.CTkComboBox(
            self,
            height=20,
            variable=self.app.agent_data_var["symbol"],
            command=self.login_agent,
        )
        self.id_login.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.id_login.bind("<Return>", lambda event: self.login_agent())
        self.generate_login_combobox()

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

    def generate_login_combobox(self):
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

                (
                    threading.Thread(
                        target=data_sync,
                        args=(
                            self.app,
                            result["data"]["token"],
                        ),
                    )
                ).start()
                #                self.show_agent_summary(result["data"])
                # print(result)

                # -1, so now store the agent name / token for future runs
                if self.id_login.get() not in known_agents:
                    self.store_agent_login(result["data"])
            else:
                print("Failed:", response.status_code, response.reason, response.text)

        except ConnectionError as ce:
            print("Failed:", ce)
