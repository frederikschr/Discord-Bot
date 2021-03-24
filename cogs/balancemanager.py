import discord
from discord.ext import commands, tasks
import json
import asyncio
from requestings.get_balance import get_balance
from checks.has_balance import has_balance
from checks.is_registered import is_registered

class balancemanager(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def addme(self, ctx):
        with open("./json/balances.json", "r") as f:
            balance = json.load(f)

        if not is_registered(ctx.author.id):
            balance[(ctx.author.id)] = 100
            await ctx.send(f"`You have been added to the balance system`")
        else:
            await ctx.send("`You are already added to the balance system.`")
            return

        with open("./json/balances.json", "w") as f:
            json.dump(balance, f, indent=4)

    @commands.command()
    async def getbalance(self, ctx):
        if get_balance(ctx.author.id) == KeyError:
            await self.addme(ctx)
            await ctx.send(f"`You have been added to the balance system. \n{ctx.author}: {get_balance(ctx.author.id)} Coins`")

        else:
            await ctx.send(f"`{ctx.author}: {get_balance(ctx.author.id)}`")

    @commands.command()
    async def sendmoney(self, ctx, amount, member:discord.Member):
        with open("./json/balances.json", "r") as f:
            balance = json.load(f)

            if ctx.author.id == member.id:
                await ctx.send("`You can't send money to yourself.`")
                return

            if amount == "all":
                amount = get_balance(ctx.author.id)

            if not has_balance(amount, ctx.author.id):
                await ctx.send("`You don't have enough money.`")
                return
            else:
                pass

            member_balance = get_balance(member.id)
            member_balance += int(amount)

            author_balence = get_balance(ctx.author.id)
            author_balence -= int(amount)

            balance[str(member.id)] = member_balance
            balance[str(ctx.author.id)] = author_balence

            await ctx.send(f"`You sent {amount} to {member} \n Your new balance is: {author_balence}`")

        with open("./json/balances.json", "w") as f:
            json.dump(balance, f, indent=4)

    @commands.command()
    @commands.is_owner()
    async def givemoney(self, ctx, amount, member:discord.Member):
        with open("./json/balances.json", "r") as f:
            balances = json.load(f)

        member_balance = get_balance(member.id)
        member_balance += int(amount)

        balances[(str(member.id))] = member_balance

        with open("./json/balances.json", "w") as f:
            json.dump(balances, f, indent=4)

    @commands.Cog.listener()
    async def on_ready(self):
        self.balance_changer.start()

    @tasks.loop(hours=3)
    async def balance_changer(self):

        with open("./json/balances.json", "r") as f:
            balances = json.load(f)

        for key, value in balances.items():
            old_balance = value

            new_balance = int(old_balance) + 100

            balances[key] = new_balance

        #for guild in self.client.guilds:
            #await guild.text_channels[0].send("`Everyone received 100$.`")

        with open("./json/balances.json", "w") as f:
            json.dump(balances, f, indent=4)

def setup(client):
    client.add_cog(balancemanager(client))
