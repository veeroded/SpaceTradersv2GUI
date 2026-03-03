# updates all string vars of the agent_data to the latest copy
def update_agent(target, data):
    # only have to check symbol since they will all have no data if that doesnt
    if target.agent_data["symbol"] == "":
        target.agent_data["symbol"].set(data["symbol"])
        target.agent_data["headquarters"].set(data["headquarters"])
        target.agent_data["starting_faction"].set(data["startingFaction"])
    target.agent_data["credits"].set(data["credits"])
    target.agent_data["ship_count"].set(data["shipCount"])
