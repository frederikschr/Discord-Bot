import discord
from discord.ext import commands

class announcements(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def announce(self, ctx, *, message):

        embed = discord.Embed(title="Announcement by developer", color=discord.Color.red())
        embed.add_field(name="Message", value=message)

        for guild in self.client.guilds:

            await guild.text_channels[0].send(embed=embed)
            await guild.text_channels[0].send("@here")

def setup(client):
    client.add_cog(announcements(client))