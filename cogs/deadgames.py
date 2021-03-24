import discord
from discord.ext import commands
import json

class deadgames(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.elements = []
        self.pic = "https://cdn.discordapp.com/attachments/804801624282497073/808824018441863208/crying_nword.jpg"

    @commands.Cog.listener()
    async def on_ready(self):
        with open("./json/deadgames.json") as f:
            games = json.load(f)

        for game in games:
            self.elements.append(game)

    @commands.command()
    async def addgame(self, ctx, *, game):
        self.elements.append(game)
        await ctx.send(f"`{game} was added to the dead games list. See you Buddy!`")

        with open("./json/deadgames.json", "w") as f:
            json.dump(self.elements, f)

    @commands.command()
    async def removegame(self, ctx, *, game):
        try:
            with open("./json/deadgames.json", "r") as f:
                deadgames = json.load(f)

            self.elements.remove(f"{game}")
            await ctx.send(f"`{game} has been removed from the dead games list. Welcome back Bro!`")

            with open("./json/deadgames.json", "w") as f:
                json.dump(self.elements, f)

        except ValueError:
            await ctx.send(f"`No Game named: {game}`")

    @commands.command()
    async def getgames(self, ctx):
        if self.elements:
            with open("./json./deadgames.json", "r") as f:
                getgames = json.load(f)

            embed = discord.Embed(title="Deadgames", color=discord.Color.red())
            embed.set_image(url=self.pic)

            for game in getgames:
                embed.add_field(name=f"{game}", value="Ⓕ")

            await ctx.send(embed=embed)

        else:
            await ctx.send("`Deadgames list is empty.`")

def setup(client):
    client.add_cog(deadgames(client))