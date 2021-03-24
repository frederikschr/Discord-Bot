from discord.ext import commands
import discord
from discord.ext.commands import has_permissions, MissingPermissions
import os
from discord.utils import get

class channelmanagement(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.channels = ["mainstreit-1", "🧒kinderarbeitslager🧒", "🦨rumänien🦨", "🐵monkey🐵", "🚮mülldeponie🚮","🐴juan🐴", "🔫schlachtfeld🔫"]

    def bot_is_connected(self, ctx):
        voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
        return voice_client and voice_client.is_connected()

    @commands.command()
    @has_permissions(administrator=True)
    async def create(self, ctx, channel_name):
        guild = ctx.message.guild
        await guild.create_text_channel(channel_name)
        await ctx.send(f"`{channel_name} was created.`")

    @commands.command()
    @has_permissions(administrator=True)
    async def deleteall(self, ctx):
        guild = ctx.message.guild

        for channel in list(ctx.message.guild.channels):
            try:
                await channel.delete()

            except:
                pass

    @commands.command()
    @has_permissions(administrator=True)
    async def delete(self, ctx, channel: discord.TextChannel):
        await channel.delete()
        await ctx.send(f"`{channel} was deleted.`")

    @commands.command()
    @has_permissions(administrator=True)
    async def getchannel(self, ctx):
        for channel in list(ctx.message.guild.channels):
            await ctx.send(f"`{channel}`")

    @commands.command()
    @has_permissions(administrator=True)
    async def purge(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("`Missing required permissions.`")

    @commands.command()
    async def mainstreit(self, ctx):

        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel

            if not self.bot_is_connected(ctx):
                await channel.connect()
            else:
                pass

            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            voice.play(discord.FFmpegPCMAudio("./audio/s.nuclear.mp3"))

        else:
            pass

        for channel in self.channels:
            guild = ctx.message.guild

            await guild.create_text_channel(channel)

    @commands.command()
    async def clearmainstreit(self, ctx):
        for channel in list(ctx.message.guild.text_channels):
            if channel.name in self.channels:
                await channel.delete()



def setup(client):
    client.add_cog(channelmanagement(client))