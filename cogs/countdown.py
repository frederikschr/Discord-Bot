import discord
from discord.ext import commands
from discord.utils import get
import asyncio

class countdown(commands.Cog):

    def __init__(self, client):
        self.client = client

    def bot_is_connected(self, ctx):
        voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
        return voice_client and voice_client.is_connected()

    @commands.command()
    async def timer(self, ctx, tspan, type):
        try:
            x = int(tspan)

            await ctx.send(f"`Starting Countdown of: {tspan} {type}.`")

            if type == "sec":
                while x > 0:
                    x -= 1
                    await asyncio.sleep(1)
                await ctx.send("`Countdown is finished!`")


            elif type == "min":
                x = x * 60
                while x > 0:
                    x -= 1
                    await asyncio.sleep(1)
                await ctx.send("`Countdown is finished!`")


            if ctx.author.voice:
                if not self.bot_is_connected(ctx):
                    channel = ctx.author.voice.channel
                    await channel.connect()
                else:
                    pass

                voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
                voice.play(discord.FFmpegPCMAudio("./audio/s.alarm.mp3"))
                await asyncio.sleep(10)
                await voice.disconnect()

            else:
                pass

        except Exception:
            await ctx.send("`Countdown is missing a timespan or sec / min`")


def setup(client):
    client.add_cog(countdown(client))

