import discord
from discord.ext import commands
import aiohttp

class webimages(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def dog(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://random.dog/woof.json") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Dog", color=discord.Color.red())
                    embed.set_image(url=data['url'])
                    embed.set_footer(text="http://random.dog/")

                    await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://aws.random.cat/meow") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Cat", color=discord.Color.red())
                    embed.set_image(url=data['file'])
                    embed.set_footer(text="http://random.cat/")

                    await ctx.send(embed=embed)

def setup(client):
    client.add_cog(webimages(client))