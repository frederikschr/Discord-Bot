import discord
from discord.ext import commands
import json
from checks.has_balance import has_balance
from requestings.get_balance import get_balance
import random
import asyncio
from discord.utils import get
from checks.is_registered import is_registered

class roulette():

    def __init__(self, client):
        self.client = client
        self.amount = {}
        self.color = {}
        self.oldbalance = {}
        self.winners = []
        self.oldrolls = []
        self.inactive_count = 0
        self.running = False
        self.music = False

    def bot_is_connected(self, ctx):
        voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
        return voice_client and voice_client.is_connected()

    @commands.command()
    async def roulettegame(self, ctx, music=None):
        if not self.running:
            self.running = True
            await ctx.send("`Started rolling!`")

        else:
            self.running = False
            await ctx.send("`Stopped rolling!`")
            self.oldrolls.clear()

        if music:
            self.music = True
        else:
            pass

        while self.running:
            await asyncio.sleep(15)

            if self.color:
                self.inactive_count = 0

                if self.music:
                    if ctx.author.voice and ctx.author.voice.channel:
                        channel = ctx.author.voice.channel

                        if not self.bot_is_connected(ctx):
                            await channel.connect()
                        else:
                            pass

                        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
                        voice.play(discord.FFmpegPCMAudio(f"./audio/s.roulette.mp3"))

                    else:
                        await ctx.send("`You are not connected to a voice channel.`")
                        self.running = False
                        return
                else:
                    pass

                random_choice = random.randint(1, 106)

                await asyncio.sleep(3)

                if random_choice <= 50:
                    color = 1
                    square = ":red_square:"
                    roll_color = "Red"

                elif random_choice >= 50 and random_choice <= 100:
                    color = 2
                    square = ":black_large_square:"
                    roll_color = "Black"

                else:
                    color = 3
                    square = ":green_square:"
                    roll_color = "Green"

                play_sound = False

                for key, value in self.color.items():

                    with open("./json/balances.json", "r") as f:
                        balance = json.load(f)

                    if value == color:
                        bet_amount = self.amount[(key)]

                        if color == 1 or color == 2:
                            bet_amount = bet_amount * 2

                        else:
                            bet_amount = bet_amount * 14

                            if self.music:
                                play_sound = True

                        current_balance = get_balance(key)
                        current_balance += bet_amount

                        user = await self.client.fetch_user(key)
                        self.winners.append(user)

                        balance[(key)] = current_balance

                    else:
                        bet_amount = self.amount[key]

                        current_balance = get_balance(key)
                        current_balance -= bet_amount

                        balance[(key)] = current_balance

                    with open("./json/balances.json", "w") as f:
                        json.dump(balance, f, indent=4)

                embed = discord.Embed(title="Roulette", color=discord.Color.red())
                embed.add_field(name=square, value=roll_color, inline=True)

                if self.winners:
                    for x, user in enumerate(self.winners):

                        coins_won = balance[str(user.id)] - self.oldbalance[str(user.id)]

                        embed.add_field(name=f"Winner {x+1}", value=f"{user} won {coins_won} credits", inline=False)
                else:
                    embed.add_field(name="No winner", value="///", inline=False)

                if play_sound:
                    await asyncio.sleep(3)
                    voice.play(discord.FFmpegPCMAudio(f"./audio/s.jackpot.mp3"))

                self.oldrolls.append(square)
                history = "".join(self.oldrolls)

                embed.add_field(name="History", value=history)

                await asyncio.sleep(1)
                await ctx.send(embed=embed)

                self.color.clear()
                self.amount.clear
                self.winners.clear()
                self.oldbalance.clear()

            else:
                self.inactive_count += 1

                if self.inactive_count >= 3:
                    await ctx.send("`Stopped rolling because of inactivity.`")
                    self.oldrolls.clear()
                    self.running = False
                    return

    @commands.command()
    async def betr(self, ctx, amount, field: str):
        if is_registered(ctx.author.id):
            if self.running:
                if amount == "all":
                    amount = get_balance(ctx.author.id)
                else:
                    pass

                amount = int(amount)

                if not has_balance(amount, ctx.author.id):
                    await ctx.send("`You don't have enough money.`")
                    return
                else:
                    pass
            else:
                await ctx.send("`Currently no roulette session is running.`")
                return
        else:
            await ctx.send("`You have not been added to the balance system yet.`")
            return

        self.amount[str(ctx.author.id)] = int(amount)
        self.oldbalance[str(ctx.author.id)] = get_balance(ctx.author.id)

        field = f"{field}"
        field = field.lower()

        if field == "red":
            color = 1

        elif field == "black":
            color = 2

        elif field == "green":
            color = 3

        else:
            await ctx.send("`Not a a valid color`")
            return

        self.color[str(ctx.author.id)] = int(color)

class manager(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.guilds = {}
        self.ids = []

    @commands.command()
    async def roulette(self, ctx, music=None):

        for key, value in self.guilds.items():
            if key == str(ctx.guild.id):
                await value.roulettegame(value, ctx, music=music)
                return

        object_name = ctx.guild.id
        object_name = roulette(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.roulettegame(object_name, ctx, music=music)

    @commands.command()
    async def betr(self, ctx, amount, field: str):

        for key, value in self.guilds.items():
            if key == str(ctx.guild.id):
                await value.betr(value, ctx, amount, field)
                return

        object_name = ctx.guild.id
        object_name = roulette(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.betr(object_name, ctx, amount, field)

def setup(client):
    client.add_cog(manager(client))
