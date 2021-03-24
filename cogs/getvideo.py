import discord
from discord.ext import commands
from requestings.get_url import get_url

class getvideo(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def getvideo(self, ctx, *, keywords):

        video = get_url(f"{keywords}")

        embed = discord.Embed(title="Video found", color=discord.Color.red())
        embed.add_field(name=f"{video}", value=f"{ctx.author}")

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(getvideo(client))