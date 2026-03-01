BASEURL = "https://api.spacetraders.io/v2/"
AGENT_FILE = "./agents.json"

ENDPOINTS = {
    "API_STATUS": f"{BASEURL}",
    "LIST_FACTIONS": f"{BASEURL}factions",
    "CLAIM_USER": f"{BASEURL}register",
    "MY_ACCOUNT": f"{BASEURL}my/agent",
    "MY_CONTRACTS": f"{BASEURL}my/contracts",
    "MY_SHIPS": f"{BASEURL}my/ships",
}
UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
DISPLAY_FORMAT = " %B, %Y"
FACTION_LOOKUPS = {}
