from .get_api import contracts_data, agent_data, ships_data
from .update_data import update_agent
from time import sleep


# Inteneded to be run with in a loop in the background hence the rate limiting
# Also each block binds the diffent values to stringvars
def data_sync(target, Bearer):
    while True:
        lagent_data = agent_data(Bearer)
        update_agent(target, lagent_data)
        print(target.agent_data)

        lcontracts_data = contracts_data(Bearer)

        target.ships_data = ships_data(Bearer)
        sleep(10)
