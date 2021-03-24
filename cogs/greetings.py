from discord.ext import commands

class greetings(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hello(self, ctx):
        if ctx.author.id == 398124000632504321:
            await ctx.send("`Hello my master.`")

        else:
            await ctx.send(f"`Hello there {ctx.author}!`")

def setup(client):
    client.add_cog(greetings(client))