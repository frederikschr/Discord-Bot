import discord
from discord.ext import commands

class changestatus(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def changestatus(self, ctx, *, status):
        await self.client.change_presence(activity=discord.Game(name=f"{status}"))

def setup(client):
    client.add_cog(changestatus(client))