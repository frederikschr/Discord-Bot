import json

def get_balance(author):
    with open("./json/balances.json") as f:
        balance = json.load(f)
        try:
            return balance[str(author)]
        except KeyError:
            return KeyError
