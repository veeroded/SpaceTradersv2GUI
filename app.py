import customtkinter as ctk
from pages import Login, Summary
from Utils import constants


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # constants for the whole program
        self.endpoints = constants.ENDPOINTS
        self.display_format = constants.DISPLAY_FORMAT
        self.utc_format = constants.UTC_FORMAT
        self.faction_lookups = constants.FACTION_LOOKUPS
        self.agentfile = constants.AGENT_FILE

        # variables that will be managed by the sync loop 3/20 of rps used

        self.agent_data = {
            "symbol": ctk.StringVar(),
            "headquarters": ctk.StringVar(),
            "starting_faction": ctk.StringVar(),
            "credits": ctk.StringVar(),
            "ship_count": ctk.StringVar(),
        }

        # Will help with readability
        self.player_token = ctk.StringVar()

        # The loop is established immediatly after logging in

        self.title("SpaceTrader")
        self.geometry("1920x1080")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.make_tabs()

    def make_tabs(self):
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True, padx=5, pady=5)

        # List of tupples of tab_name and tab
        tabs = [("Logins", Login), ("Summary", Summary)]

        self.pages = {}

        # Making the tabs
        for tab_name, PageClass in tabs:
            self.tab_view.add(tab_name)
            page = PageClass(self.tab_view.tab(tab_name), app=self)
            page.pack(fill="both", expand=True)
            self.pages[tab_name] = page


#    # Controls tabs for the login page
#    def login_tab_lock(self):
#        for tab_name in ["Summary"]:
#            self.tab_view.tab(tab_name).configure(state="disabled")
