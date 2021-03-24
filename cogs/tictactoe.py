import discord
from discord.ext import commands
import random

class tictactoe():

    def __init__(self, client):
        self.client = client
        self.running = False
        self.turn = None
        self.player1 = None
        self.player2 = None
        self.mark = ""
        self.count = 0
        self.winningConditions = [[0, 1, 2],[3, 4, 5],[6, 7, 8],[0, 3, 6], [1, 4, 7],[2, 5, 8],[0, 4, 8],[2, 4, 6]]
        self.board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]

    def reset(self):
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        self.count = 0
        self.board = board

    def has_won(self):
        true_conditions = []

        for condition in self.winningConditions:
            if self.board[condition[0]] == self.mark and self.board[condition[1]] == self.mark and self.board[condition[2]] == self.mark:
                true_conditions.append(condition)
            else:
                pass
        if true_conditions:
            return True
        else:
            return False

    @commands.command()
    async def tictactoe(self, ctx, player1:discord.Member, player2:discord.Member):

        embed = discord.Embed(title="Tic tac toe", color=discord.Color.red())

        if not self.running:
            self.running = True
            self.reset()


            embed.add_field(name=f"{self.board[0]}{self.board[1]}{self.board[2]}\n"
                                 f"{self.board[3]}{self.board[4]}{self.board[5]}\n"
                                 f"{self.board[6]}{self.board[7]}{self.board[8]}", value=f"Taken: {self.count}")

            pick = random.randint(1, 2)

            self.player1 = player1
            self.player2 = player2

            if pick == 1:
                self.turn = player1
            else:
                self.turn = player2

            embed.add_field(name=f"Turn", value=f"{self.turn}")

            await ctx.send(embed=embed)

        else:
            await ctx.send("`Game in progress.`")

    @commands.command()
    async def place(self, ctx, square: int):
        square -= 1

        embed = discord.Embed(title="Tic tac toe", color=discord.Color.red())

        if self.running:
            if self.turn == ctx.author:
                if self.turn == self.player1:
                    self.mark = ":regional_indicator_x:"
                else:
                    self.mark = ":o2:"
                if -1 < square < 10 and self.board[square] == ":white_large_square:":
                    self.board[square] = self.mark
                else:
                    await ctx.send("`Choose a number between 1 and 9 and only one that are not taken yet.`")
                    return

                self.count += 1


                embed.add_field(name=f"{self.board[0]}{self.board[1]}{self.board[2]}\n"
                                     f"{self.board[3]}{self.board[4]}{self.board[5]}\n"
                                     f"{self.board[6]}{self.board[7]}{self.board[8]}", value=f"Taken: {self.count}")

                if self.has_won():
                    embed.add_field(name=f"Winner", value=f"{self.turn}", inline=True)
                    await ctx.send(embed=embed)
                    self.running = False
                    return

                elif self.count > 8:
                    embed.add_field(name=f"It's a tie!", value=f"///")
                    await ctx.send(embed=embed)

                    return

                else:
                    pass

                if self.turn == self.player1:
                    self.turn = self.player2
                else:
                    self.turn = self.player1

                embed.add_field(name=f"Turn", value=f"{self.turn}")
                await ctx.send(embed=embed)

            else:
                await ctx.send("`It is not your turn.`")
        else:
            await ctx.send("`Currently no game is running.`")

class manager(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.guilds = {}
        self.ids = []

    @commands.command()
    async def tictactoe(self, ctx, player1: discord.Member, player2: discord.Member):
        for key, value in self.guilds.items():
            if key == str(ctx.guild.id):
                await value.tictactoe(value, ctx, player1, player2)
                return

        object_name = ctx.guild.id
        object_name = tictactoe(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.tictactoe(object_name, ctx, player1, player2)

    @commands.command()
    async def place(self, ctx, square: int):

        for key, value in self.guilds.items():
            if key == str(ctx.guild.id):
                await value.place(value, ctx, square)
                return

        object_name = ctx.guild.id
        object_name = tictactoe(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.place(object_name, ctx, square)


def setup(client):
    client.add_cog(manager(client))