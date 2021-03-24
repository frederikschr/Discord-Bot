from discord.ext import commands
import random

class coinflip(commands.Cog):

    def __init__(self, client):
        self.client = client

    def getrandom(self):
        rannumber = random.randint(1, 2)
        return rannumber

    @commands.command()
    async def coin(self, ctx):
        if self.getrandom() == 1:
            await ctx.send("`Heads`")

        else:
            await ctx.send("`Tails`")

def setup(client):
    client.add_cog(coinflip(client))
