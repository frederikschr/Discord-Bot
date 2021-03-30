import discord
from discord.ext import commands
from requestings.get_hangmanpic import get_hangmanpic

class hangman():

    def __init__(self, client):
        self.client = client
        self.running = False
        self.players = []
        self.player_names = []
        self.guessed_characters = []
        self.word_characters = []
        self.visible_chars = []
        self.death_count = 0
        self.host =  None
        self.host_name = None
        self.word = ""

    def has_won(self):
        for char in self.visible_chars:
            if char in self.word_characters:
                pass
            else:
                return False

        return True

    def reset(self):
        self.players = []
        self.player_names = []
        self.guessed_characters = []
        self.word_characters = []
        self.visible_chars = []
        self.death_count = 0
        self.word = ""

    @commands.command()
    async def hangman(self, ctx, *players: discord.Member):
        if not self.running:

            self.reset()

            for player in players:

                if not player.id == ctx.author.id and not player.id == self.client.user.id:

                    self.players.append(player.id)
                    self.player_names.append(player.name)

                else:
                    await ctx.send("`Host and bot can't be included in the player's list.`")
                    return

            self.running = True
            self.host = ctx.author.id
            self.host_name = ctx.author

            embed = discord.Embed(title="Hangman", description=f"{self.host_name}", color=discord.Color.red())

            player_list = ", ".join(self.player_names)
            embed.add_field(name="Players", value=player_list)

            await ctx.send(embed=embed)

        else:

            if ctx.author.id in self.players:
                self.running = False

                self.reset()

            await ctx.send("`Game already running.`")

    @commands.command(aliases=["s"])
    async def setword(self, ctx, word: str):
        if self.running:

            if self.word == "":

                if ctx.author.id == self.host:
                    if len(word) <= 10:

                        self.word = word.upper()

                        await ctx.message.delete()

                        for character in str(self.word):
                            self.word_characters.append(character)

                        try:
                            await ctx.author.send(f"`You picked the word: {self.word}`")

                        except Exception:
                            pass

                        embed = discord.Embed(title="Hangman", description=f"{ctx.author}", color=discord.Color.red())

                        word_length = ""

                        for i in range(len(self.word_characters)):

                            word_length = word_length + ":grey_question:"
                            self.visible_chars.append(":grey_question:")

                        embed.add_field(name="Word", value=word_length, inline=False)

                        await ctx.send(embed=embed)

                    else:
                        await ctx.send("Your word is too long. Please choose a word below 11 characters.")
                else:
                    await ctx.send("`You are not the host.`")
            else:
                await ctx.send("`A word was already chosen.`")
        else:
            await ctx.send("`Currently no game is running.`")

    @commands.command()
    async def guessword(self, ctx, char):
        if self.running:
            if self.word:
                if not ctx.author.id == self.host:
                    if ctx.author.id in self.players:
                        if len(char) == 1:
                            if char.isalpha():
                                char = char.upper()

                                if not char in self.guessed_characters:

                                    embed = discord.Embed(title="Hangman", description=f"{self.host_name}", color=discord.Color.red())

                                    self.guessed_characters.append(char)

                                    if char in self.word_characters:

                                        index_counter = 0

                                        for character in self.word_characters:

                                            if character == char:
                                                self.visible_chars[index_counter] = char

                                            index_counter += 1

                                        if self.has_won():
                                            player_list = ", ".join(self.player_names)
                                            embed.add_field(name="Winner", value=player_list)
                                            embed.add_field(name="Word", value=self.word, inline=False)

                                            await ctx.send(embed=embed)

                                            self.running = False
                                            self.reset()
                                            return

                                    else:

                                        if self.death_count > 7:

                                            embed.add_field(name="Winner", value=self.host_name)
                                            embed.add_field(name="Word", value=self.word, inline=False)
                                            embed.set_image(url=get_hangmanpic(9))

                                            await ctx.send(embed=embed)

                                            self.running = False
                                            self.reset()
                                            return

                                        else:
                                            self.death_count += 1

                                    visible = " ".join(self.visible_chars)
                                    embed.add_field(name="Word", value=visible, inline=False)

                                    guessed_characters = ", ".join(self.guessed_characters)
                                    embed.add_field(name="Guessed characters", value=guessed_characters, inline=False)

                                    tries_left = 9 - self.death_count
                                    embed.add_field(name="Tries left", value=tries_left, inline=False)

                                    if self.death_count >= 1:
                                        image = get_hangmanpic(self.death_count)
                                        embed.set_image(url=image)

                                    await ctx.send(embed=embed)

                                else:
                                    await ctx.send("`You already guessed this character.`")
                            else:
                                await ctx.send("`Please choose a character and not a number.`")
                        else:
                            await ctx.send("`Please choose a character and not a word.`")
                    else:
                        await ctx.send("`You are not a player in the current session.`")
                else:
                    await ctx.send("`You are the host.`")
            else:
                await ctx.send("`No word has been selected yet.`")
        else:
            await ctx.send("`Currently no game is running.`")

class manager(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.guilds = {}
        self.ids = []


    @commands.command()
    async def hangman(self, ctx, *players: discord.Member):
        for key, value in self.guilds.items():
            if key == str(ctx.guild.id):
                await value.hangman(value, ctx, *players)
                return

        object_name = ctx.guild.id
        object_name = hangman(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.hangman(object_name, ctx, *players)

    @commands.command()
    async def setword(self, ctx, word: str):
        for key, value in self.guilds.items():
            if key == str(ctx.guild.id):
                await value.setword(value, ctx, word)
                return

        object_name = ctx.guild.id
        object_name = hangman(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.setword(object_name, ctx, word)

    @commands.command(aliases=["g"])
    async def guessword(self, ctx, char):
        for key, value in self.guilds.items():
            if key == str(ctx.guild.id):
                await value.guessword(value, ctx, char)
                return

        object_name = ctx.guild.id
        object_name = hangman(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.guessword(object_name, ctx, char)

def setup(client):
    client.add_cog(manager(client))

