import discord
from discord.ext import commands
from external.hue import *

class hue(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def on(self, ctx):
        if ctx.author.id == 398124000632504321:

            fredi_lights_on()

            await ctx.send("`Lights turned on`")

        else:
            await ctx.send("`Missing required permissions.`")

    @commands.command()
    async def off(self, ctx):
        if ctx.author.id == 398124000632504321:

            fredi_lights_off()
            await ctx.send("`Lights turned off`")

        else:
            await ctx.send("`Missing required permissions.`")

def setup(client):
    client.add_cog(hue(client))