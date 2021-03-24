import json

def has_balance(amount, author):
    with open("./json/balances.json", "r") as f:
        balance = json.load(f)

    if balance[str(author)] - int(amount) >= 0 and str(author) in balance:
        return True
    else:
        return False