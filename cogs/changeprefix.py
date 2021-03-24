from discord.ext import commands
import json

class changeprefix(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("./json/prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = "f "

        with open("./json/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open("./json/prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open("./json/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

    @commands.command()
    async def changeprefix(self, ctx, prefix):
        with open("./json/prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open("./json/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"`Changed Prefix to: {prefix}`")

def setup(client):
    client.add_cog(changeprefix(client))