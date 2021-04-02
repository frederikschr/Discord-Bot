import discord
from discord.ext import commands
import json
from requestings.get_id import get_id

class servermessenger(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def addserver(self, ctx, *, guild_name):
        with open("./json/guilds.json", "r") as f:
            guilds = json.load(f)

        guilds[str(guild_name)] = ctx.guild.id

        with open("./json/guilds.json", "w") as f:
            json.dump(guilds, f, indent=4)

        await ctx.send(f"`Added this server to the server messenger as: {guild_name}`")

    @commands.command()
    async def getserver(self, ctx):
        with open("./json/guilds.json", "r") as f:
            guilds = json.load(f)

            embed = discord.Embed(title="Servers", color=discord.Color.red())

            for key, value in guilds.items():
                embed.add_field(name=f"{key}", value=f"{value}", inline=False)

            await ctx.send(embed=embed)

    @commands.command()
    async def send(self, ctx, server_name, *, content):
        try:
            if not get_id(self.client, server_name) == ctx.guild.id:

               get_server = get_id(self.client, server_name)
               guild = self.client.get_guild(get_server)

               embed = discord.Embed(title=f"Message from {ctx.author}", color=discord.Color.red())

               embed.add_field(name=f"Sent from Server: {ctx.guild}", value=f"{content}", inline=False)

               await guild.text_channels[0].send(embed=embed)

            else:
                await ctx.send("`Can't send message to own server.`")

        except KeyError:
            await ctx.send(f"`No server named: {server_name}`")

    @commands.command()
    @commands.is_owner()
    async def message(self, ctx, server_name, channel_index: int, *, message):
        with open("./json/guilds.json") as f:
            guilds = json.load(f)

        get_server = get_id(self.client, server_name)
        guild = self.client.get_guild(get_server)

        await guild.text_channels[channel_index - 1].send("`{}`".format(message))

def setup(client):
    client.add_cog(servermessenger(client))