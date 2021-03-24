from discord.ext import commands
import random

class randompick(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def random(self, ctx, *elements):

        random_pick = random.choice(elements)

        await ctx.send(f"`{random_pick}`")

def setup(client):
    client.add_cog(randompick(client))