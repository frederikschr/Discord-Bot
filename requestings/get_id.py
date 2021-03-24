import json

def get_id(client, server_name):
    with open("./json/guilds.json", "r") as f:
        guild = json.load(f)

    return guild[str(server_name)] #returning ID


