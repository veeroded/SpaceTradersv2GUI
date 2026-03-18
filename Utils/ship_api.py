import requests
from .constants import ENDPOINTS

#Base api call 
def json_post(Bearer, endpoint, extra_headers={}, json=None) -> list[dict]:

    headers = extra_headers | {"Authorization": f"Bearer {Bearer}"}

    response = requests.post(f"{endpoint}", headers=headers, json=json)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        return response.json()

#An even furuther abststraction to make it easier to create the other calls 
def ShipAction(Bearer, ship_symbol, action, extra_headers={}, json=None):
    endpoint = f"{ENDPOINTS['MY_SHIPS']}/{ship_symbol}/{action}"
    return json_post(Bearer, endpoint, extra_headers, json)


def navigate(Bearer, ship_symbol, waypoint):
    return ShipAction(
        Bearer, ship_symbol, "navigate", json={"waypointSymbol": waypoint}
    )


def orbit(Bearer, ship_symbol) -> list[dict]:
    return ShipAction(Bearer, ship_symbol, "orbit")


def dock(Bearer, ship_symbol) -> list[dict]:
    return ShipAction(Bearer, ship_symbol, "dock")


def extract(Bearer, ship_symbol) -> list[dict]:
    return ShipAction(Bearer, ship_symbol, "extract")


def ScanWaypoints(Bearer, ship_symbol) -> list[dict]:
    return ShipAction(Bearer, ship_symbol, "scan/waypoints")


def sell(Bearer, ship_symbol, good_symbol, goods_unit=1) -> list[dict]:
    return ShipAction(
        Bearer,
        ship_symbol,
        "/sell",
        "json",
        {"symbol": good_symbol, "units": goods_unit},
    )


def jettison(Bearer, ship_symbol, good_symbol, goods_unit=1) -> list[dict]:
    return ShipAction(
        Bearer,
        ship_symbol,
        "/jettison",
        {"Content-Type": "application/json"},
        {"symbol": good_symbol, "units": goods_unit},
    )
