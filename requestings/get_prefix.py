import json

def get_prefix(client, message):
    with open("./json/prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]