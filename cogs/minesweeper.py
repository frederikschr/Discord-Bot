import discord
from discord.ext import commands
import random
import json
from requestings.get_balance import get_balance
from checks.has_balance import has_balance
from checks.is_registered import is_registered

class minesweeper():

    def __init__(self, client):
        self.client = client
        self.running = False
        self.lost = False
        self.player = ""
        self.id = 0
        self.profit = 0
        self.oldbalance = 0
        self.amount = 0
        self.multi = 0
        self.count = 0
        self.bombs = []
        self.board = [":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:",
                      ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:",
                      ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:",
                      ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:"]

    def reset(self):
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:"]

        self.lost = False
        self.player = ""
        self.multi = 0
        self.count = 0
        self.id = 0
        self.amount = 0
        self.oldbalance = 0
        self.profit = 0
        self.bombs.clear()
        self.board = board


    def change_multiplier(self):
        length = len(self.bombs)
        multi = self.count * length / 8
        self.multi = multi

    def has_won(self, won: bool):
        with open("./json/balances.json", "r") as f:
            balance = json.load(f)

        old_balance = get_balance(self.id)

        if won:
            won_money = self.amount * self.multi
            new_balance = old_balance + won_money

        else:
            new_balance = old_balance - self.amount

        balance[str(self.id)] = new_balance

        with open("./json/balances.json", "w") as f:
            json.dump(balance, f, indent=4)

    @commands.command()
    async def minesweeper(self, ctx, bombs: int, amount):
        if not self.running:
            self.running = True
            self.reset()

            if amount == "all":
                amount = get_balance(ctx.author.id)
            else:
                amount = int(amount)

            self.player = ctx.author
            self.id = ctx.author.id
            self.amount = int(amount)
            self.oldbalance = get_balance(ctx.author.id)

            if bombs >= 0 and bombs <= 15:

                if is_registered(ctx.author.id):

                    if has_balance(amount, ctx.author.id):

                        for x in range(bombs):
                            random_number = random.randint(0,15)

                            while random_number in self.bombs:
                                random_number = random.randint(0, 15)

                            self.bombs.append(random_number)

                        embed = discord.Embed(title="Minesweeper", color=discord.Color.red())


                        line = ""
                        for x in range(len(self.board)):
                            if x == 3 or x == 7 or x == 11 or x == 15:
                                line += " " + self.board[x]
                                await ctx.send(line)
                                line = ""
                            else:
                                line += " " + self.board[x]

                        embed.add_field(name="Bombs", value=f"{len(self.bombs)}:bomb:", inline=True)
                        embed.add_field(name="Your Bet", value=f"{amount}$")

                        await ctx.send(embed=embed)

                    else:
                        await ctx.send("`You dont't have enough money.`")
                        self.running = False
                else:
                    await ctx.send("`You have not been added to the balance system yet.`")
                    self.running = False
            else:
                await ctx.send("`Please choose a bomb amount between 1 and 15.`")
                self.running = False
        else:
            await ctx.send("`Game in progress.`")

    @commands.command()
    async def betm(self, ctx, square: int):
        if self.running:
            if ctx.author == self.player:
                if square >= 1 and square <= 16:

                    square -= 1

                    if not self.board[square] == ":black_large_square:":

                        self.count += 1

                        embed = discord.Embed(title="Minesweeper", color=discord.Color.red())

                        if int(square) in self.bombs:
                            self.lost = True

                            for bomb in self.bombs:
                                self.board[bomb] = ":bomb:"

                        else:
                            self.board[square] = ":black_large_square:"

                        self.change_multiplier()

                        line = ""
                        for x in range(len(self.board)):
                            if x == 3 or x == 7 or x == 11 or x == 15:
                                line += " " + self.board[x]
                                await ctx.send(line)
                                line = ""
                            else:
                                line += " " + self.board[x]

                        squares_left = 16 - self.count - len(self.bombs)

                        embed.add_field(name="Balance", value=f"{self.multi * self.amount}$", inline=False)
                        embed.add_field(name="Squares left", value=f"{squares_left}", inline=False)

                        multi = (self.count + 1) * (len(self.bombs) / 8)
                        next_revenue = multi * self.amount

                        embed.add_field(name="Next revenue", value=f"{next_revenue}$")

                        bomb_length = len(self.bombs) - 1
                        no_bomb_squares = 15 - bomb_length

                        if self.count == no_bomb_squares and self.count != 1:
                            embed = discord.Embed(name="Minesweeper", color=discord.Color.red())

                            self.running = False
                            self.has_won(True)

                            self.profit = get_balance(self.id) - int(self.oldbalance)

                            embed.add_field(name="You won", value=f"+{self.profit}$")

                            await ctx.send(embed=embed)
                            return

                        elif self.lost:
                            embed = discord.Embed(title="Minesweeper", color=discord.Color.red())

                            embed.add_field(name="You lost", value=f"-{self.amount}$")
                            self.running = False
                            self.has_won(False)

                            await ctx.send(embed=embed)
                            return

                        await ctx.send(embed=embed)

                    else:
                        await ctx.send("`This Square is already taken.`")
                else:
                    await ctx.send("`Please choose a square amount between 1 and 16.`")
            else:
                await ctx.send("`You are not the player of this session.`")
        else:
            await ctx.send("`Currently no game is running.`")

    @commands.command()
    async def cashout(self, ctx):
        if self.running:

            embed = discord.Embed(name="Minesweeper", color=discord.Color.red())

            self.has_won(True)
            self.running = False

            self.profit = get_balance(self.id) - int(self.oldbalance)

            embed.add_field(name="You won", value=f"+{self.profit}$")

            await ctx.send(embed=embed)

        else:
            await ctx.send("`Currently no game is running.`")

class manager(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.guilds = {}
        self.ids = []

    @commands.command()
    async def minesweeper(self, ctx, bombs: int, amount):
        for key, value in self.guilds.items():
            if key == str(ctx.guild.id):
                await value.minesweeper(value, ctx, bombs, amount)
                return

        object_name = ctx.guild.id
        object_name = minesweeper(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.minesweeper(object_name, ctx, bombs, amount)

    @commands.command()
    async def betm(self, ctx, square: int):

        for key, value in self.guilds.items():
            if key == str(ctx.guild.id):
                await value.betm(value, ctx, square)
                return

        object_name = ctx.guild.id
        object_name = minesweeper(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.betm(object_name, ctx, square)

    @commands.command()
    async def cashout(self, ctx):

        for key, value in self.guilds.items():
            if key == str(ctx.guild.id):
                await value.cashout(value, ctx)
                return

        object_name = ctx.guild.id
        object_name = minesweeper(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.cashout(object_name, ctx)




def setup(client):
    client.add_cog(manager(client))