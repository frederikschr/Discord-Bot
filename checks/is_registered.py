import json

def is_registered(member):
    with open("./json/balances.json", "r") as f:
        balance = json.load(f)

        if str(member) in balance:
            return True
        else:
            return False