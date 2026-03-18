import requests
from Utils import constants as c

#The base function for the api clals 
def json_request(Bearer, endpoint) -> dict:

    headers = {"Authorization": f"Bearer {Bearer}"}

    response = requests.get(
        f"{endpoint}",
        headers=headers,
    )
    if response.status_code == 200:
        return response.json()["data"]
    else:
        return response.json()


# only have to run once since these / this doesnt change often
def systems_data(Bearer):
    return json_request(Bearer, "/systems")


def systems_waypoints_data(Bearer, Waypoint):
    return json_request(Bearer, f"{c.ENDPOINTS['SYSTEMS']}/{Waypoint}/waypoints")


# Have to update frequently so that the player has up to date data
def agent_data(Bearer) -> dict:
    return json_request(Bearer, c.ENDPOINTS["MY_ACCOUNT"])


def contracts_data(Bearer) -> dict:
    return json_request(Bearer, c.ENDPOINTS["MY_CONTRACTS"])


def ships_data(Bearer) -> dict:
    return json_request(Bearer, c.ENDPOINTS["MY_SHIPS"])
