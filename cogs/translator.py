import discord
from discord.ext import commands
from googletrans import Translator, LANGUAGES

class translator(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def translate(self, ctx, source, destination, *, text):

        embed = discord.Embed(title="Translator", color=discord.Color.red())

        trans = Translator()

        try:
            t = trans.translate(f"{text}", src=f"{source}", dest=f"{destination}")

            embed.add_field(name="Source", value=LANGUAGES[source])
            embed.add_field(name="Destination", value=LANGUAGES[destination])

            embed.add_field(name="Text", value=text, inline=False)

            embed.add_field(name="Translation", value=t.text, inline=False)

            await ctx.send(embed=embed)

        except ValueError:
            await ctx.send("`Please choose valid languages.`")

    @commands.command()
    async def languageregister(self, ctx):

        embed = discord.Embed(title="Languages", color=discord.Color.red())

        embed.add_field(name="A-D", value="Languages Page 1")
        embed.add_field(name="E-H", value="Languages Page 2")
        embed.add_field(name="I-M", value="Languages Page 3")
        embed.add_field(name="M-S", value="Languages Page 4")

        await ctx.send(embed=embed)

    @commands.command()
    async def getlanguages(self, ctx, page: int):

        embed1 = discord.Embed(title="Languages", color=discord.Color.red())
        embed2 = discord.Embed(title="Languages", color=discord.Color.red())
        embed3 = discord.Embed(title="Languages", color=discord.Color.red())
        embed4 = discord.Embed(title="Languages", color=discord.Color.red())


        count = 0

        for lang in LANGUAGES:
            if count <= 20:
                embed1.add_field(name=f"{LANGUAGES[lang]}", value=f"{lang}")
                count += 1

            elif count <= 40:
                embed2.add_field(name=f"{LANGUAGES[lang]}", value=f"{lang}")
                count += 1

            elif count <= 60:
                embed3.add_field(name=f"{LANGUAGES[lang]}", value=f"{lang}")
                count += 1

            elif count <= 80:
                embed4.add_field(name=f"{LANGUAGES[lang]}", value=f"{lang}")
                count += 1

        if page == 1:
            await ctx.send(embed=embed1)
        elif page == 2:
            await ctx.send(embed=embed2)
        elif page == 3:
            await ctx.send(embed=embed3)
        elif page == 4:
            await ctx.send(embed=embed4)

        else:
            await ctx.send("`No page was found.`")

def setup(client):
    client.add_cog(translator(client))