import discord
from discord.ext import commands

class help(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.messages = []

    @commands.command()
    async def help(self, ctx):

        author_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

        embed = discord.Embed(title="Help", description="Open a page by reacting with the page's number", color=discord.Color.red())

        embed.add_field(name="Arcade", value="Page 1")
        embed.add_field(name="Music", value="Page 2")
        embed.add_field(name="Web", value="Page 3")
        embed.add_field(name="Balance", value="Page 4")
        embed.add_field(name="Tools", value="Page 5")
        embed.add_field(name="Random", value="Page 6")

        embed.set_author(name="Fredo", url=author_url, icon_url="https://cdn.discordapp.com/attachments/820228513000980481/820395134268080158/discord_5.png")

        message = await ctx.send(embed=embed)

        self.messages.append(message.id)

        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]

        for emoji in emojis:
            await message.add_reaction(emoji)


    @commands.command()
    @commands.is_owner()
    async def owner(self, ctx):

        embed = discord.Embed(title="Owner", color=discord.Color.red())
        embed.add_field(name="Announcements", value="• anounce: message")
        embed.add_field(name="Give Money", value="• givemoney: amount, @member")
        embed.add_field(name="Change status", value="• changestatus: status")
        embed.add_field(name="Dead games", value="• addgame: game name\n• removegame: game name\n• getgames")
        embed.add_field(name="Main streit", value="• mainstreit\n• clearmainstreit")
        embed.add_field(name="Add server", value="• addserver: server name")
        embed.add_field(name="Testing", value="• testing: true/false\n• unload: cog\n• load: cog")

        await ctx.author.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        for message in self.messages:

            if message == payload.message_id:

                if not payload.member == self.client.user:

                    member = payload.member
                    guild = member.guild

                    channel = discord.utils.get(self.client.get_all_channels(), id=payload.channel_id)

                    emoji = payload.emoji.name

                    if emoji == "1️⃣":

                        embed = discord.Embed(title="Arcade", description="Offering many fun games that you can play", color=discord.Color.red())
                        embed.add_field(name="Roulette", value="• roulette: music(optional)\n• betr: amount, field(red / black)")
                        embed.add_field(name="Minesweeper", value="• minesweeper: bombs, amount\n• betm: field\n• cashout")
                        embed.add_field(name="Hangman", value="• hangman: @players(undetermined amount)\n• setword: word\n• guessword: character")
                        embed.add_field(name="Tic Tac Toe", value="• tictactoe: @player1, @player2\n• place: field")

                    elif emoji == "2️⃣":

                        embed = discord.Embed(title="Music", description="Offering music service from youtube as well as playlist features", color=discord.Color.red())
                        embed.add_field(name="Play songs", value="• play: songname\n• playlist: playlistname\n• playfile: filename")
                        embed.add_field(name="Moderation", value="• pause\n• resume\n• stop\n• skip\n• leave")
                        embed.add_field(name="Playlists", value="• createplaylist: playlistname\n• deleteplaylist: playlistname\n• addplaylist: playlistname, url\n• removeplaylist: playlistname, url\n• clearplaylist: playlistname")
                        embed.add_field(name="Information", value="• getplaylists\n• getsongs")
                        embed.add_field(name="Download", value="• download: songname, artist, url")

                    elif emoji == "3️⃣":

                        embed = discord.Embed(title="Web", description="Offering cool and funny information from the web", color=discord.Color.red())
                        embed.add_field(name="Information", value="• iss")
                        embed.add_field(name="Pictures", value="• cat\n• dog")

                    elif emoji == "4️⃣":

                        embed = discord.Embed(title="Balance", description="Offering a virtual balance sytsem which let's you make / lose and send money", color=discord.Color.red())
                        embed.add_field(name="Setup", value="• addme")
                        embed.add_field(name="Transfer", value="• sendmoney: amount, @member")
                        embed.add_field(name="Information", value="• getbalance")

                    elif emoji == "5️⃣":

                        embed = discord.Embed(title="Tools", description="Offering tools which handle your tasks", color=discord.Color.red())
                        embed.add_field(name="Calculator", value="• calc: first number, +/-/:/*, second number")
                        embed.add_field(name="YT-Video", value="• getvideo: video name")
                        embed.add_field(name="Timer", value="• timer: time length, min / sec")
                        embed.add_field(name="Channel manager", value="• create: channel name\n• delete: channel name\n• deleteall(admin)\n• getchannel\n• purge: amount")
                        embed.add_field(name="Prefix changer", value="• changeprefix: new prefix")
                        embed.add_field(name="Server messenger", value="• getserver\n• send: server name, message")
                        embed.add_field(name="Translator", value="• translate: source language, destination language, text\n• languageregister\n•getlanguages: page")

                    elif emoji == "6️⃣":

                        embed = discord.Embed(title="Random", description="Offering features that have to do with random selections", color=discord.Color.red())
                        embed.add_field(name="Numbergame",value="• numbergame: first number, second number\n• guess: number\n• playgame")
                        embed.add_field(name="Random pick", value="• random: elements(undetermined amount)")
                        embed.add_field(name="Coinflip", value="• coin")

                    else:
                        return

                    await channel.send(embed=embed)

def setup(client):
    client.add_cog(help(client))