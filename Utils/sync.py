from .get_api import contracts_data, agent_data, ships_data
from time import sleep


# Inteneded to be run with in a loop in the background hence the rate limiting
# Also each block binds the diffent values to stringvars
def data_sync(target, Bearer) -> None:
    retry_delay = 5
    max_delay = 30

    while True:
        try:
            agent(target, Bearer)
            target.contracts_data = contracts_data(Bearer)
            target.ships_data = {s["symbol"]: s for s in ships_data(Bearer)}
            target.after(0, target.refresh_elements)
            retry_delay = 5
            sleep(retry_delay)
        except Exception as e:
            if "429" in str(e) or "rate" in str(e).lower():
                print(f"Rate limited. Waiting {retry_delay}s...")
                sleep(retry_delay)
                retry_delay = min(retry_delay * 2, max_delay)  # exponential backoff
            else:
                print(f"Error in data_sync: {e}")
                print((retry_delay))
                sleep(retry_delay)

#Defines the loop to manage the agent as alot of the data is stored as stringvars
def agent(target, Bearer) -> None:
    data = agent_data(Bearer)
    target.agent_data_var["symbol"].set(f"Symbol: {data['symbol']}")
    target.agent_data_var["headquarters"].set(f"Headquarters:{data['headquarters']}")
    target.agent_data_var["credits"].set(f"Credits: {data['credits']}")
    target.agent_data_var["starting_faction"].set(f"Faction: {data['startingFaction']}")
    target.agent_data_var["ship_count"].set(f"Ship Count: {data['shipCount']}")
