import discord
from discord.ext import commands
import random
import operator

class numbergame():

    def __init__(self, client):
        self.client = client

        self.first_number = None
        self.second_number = None
        self.random_number = None

        self.numbers = {}
        self.running = False

    @commands.command()
    async def numbergame(self, ctx, first_number, second_number):

        if not self.running:

            self.running = True

            if not first_number == None and not second_number == None:

                self.first_number = first_number
                self.second_number = second_number

                await ctx.send(f"`Picked a random number between {first_number} and {second_number}`")

            else:
                self.first_number = 0
                self.second_number = 100

                await ctx.send(f"`Picked a random number between 1 and 100`")

            self.random_number = random.randint(self.first_number, self.second_number)
            self.second_number += 1

            print(f"Random number is: {self.random_number}")

        else:
            await ctx.send("`Game already running.`")

    @commands.command()
    async def guess(self, ctx, number: int):

        if self.running:

            if ctx.author not in self.numbers.keys():

                if number >= self.first_number - 1 and number <= self.second_number + 1:
                    self.numbers[str(ctx.author)] = number

                    await ctx.send(f"`{ctx.author} guessed: {number}`")

                else:
                    await ctx.send("`Not in the number range.`")

            else:
                await ctx.send("`You already guessed.`")

        else:
            await ctx.send("`No game running.`")

    @commands.command()
    async def playgame(self, ctx):

        if self.running:

            for key, value in self.numbers.items():

                if value >= self.random_number:
                    new_number = value - self.random_number
                else:
                    new_number = self.random_number - value

                self.numbers[key] = new_number

            sorted_numbers = sorted(self.numbers.items(), key=operator.itemgetter(1))

            winner = sorted_numbers[0][0]

            sorted_numbers_tuple = sorted_numbers[0]
            winner_number = sorted_numbers_tuple[1]

            worst_guess = sorted_numbers[-1][0]

            print(winner)
            print(winner_number)

            embed = discord.Embed(title="Numbergame", color=discord.Color.red())
            embed.add_field(name="Number", value=self.random_number)
            embed.add_field(name="Winner", value=f"{winner} with a difference of {winner_number}", inline=False)
            embed.add_field(name="Worst guess", value=worst_guess)

            await ctx.send(embed=embed)

            self.numbers.clear()
            self.first_number = None
            self.second_number = None
            self.random_number = None

            self.running = False

        else:
            await ctx.send("`No game running.`")

class manager(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.guilds = {}
        self.ids = []

    @commands.command()
    async def numbergame(self, ctx, first_number: int = None, second_number: int = None):
        for key, value in self.guilds.items():
            if key == str(ctx.guild.id):
                await value.numbergame(value, ctx, first_number, second_number)
                return

        object_name = ctx.guild.id
        object_name = numbergame(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.numbergame(object_name, ctx, first_number, second_number)

    @commands.command()
    async def guess(self, ctx, num):
        for key, value in self.guilds.items():
            if key == str(ctx.guild.id):
                await value.guess(value, ctx, num)
                return

        object_name = ctx.guild.id
        object_name = numbergame(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.guess(object_name, ctx, num)

    @commands.command()
    async def playgame(self, ctx):
        for key, value in self.guilds.items():
            if key == str(ctx.guild.id):
                await value.playgame(value, ctx)
                return

        object_name = ctx.guild.id
        object_name = numbergame(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.playgame(object_name, ctx)

def setup(client):
    client.add_cog(manager(client))






