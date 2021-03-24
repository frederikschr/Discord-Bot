from discord.ext import commands

class info(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx):
        await ctx.send("`This Bot was programmed by FreddyS#5025 using the Discord API for Python.`")

    @commands.command()
    async def infome(self, ctx):
        await ctx.send(f"`Account created: {ctx.author.created_at}`")

def setup(client):
    client.add_cog(info(client))
