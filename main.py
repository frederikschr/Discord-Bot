import discord
from discord.ext import commands
import os
from requestings.get_prefix import get_prefix
from dotenv import load_dotenv
import shutil

load_dotenv()

client = commands.Bot(command_prefix = get_prefix)
client.remove_command("help")

failed_extensions = []

@client.event
async def on_ready():
    print(f"\nLogged in as {client.user}.")
    await client.change_presence(activity=discord.Game(name="FREDO BOT | f help"))

@client.event
async def on_guild_join(guild):

    embed = discord.Embed(title="Hello there!", color=discord.Color.red())
    embed.add_field(name=f"Hello {guild} members", value="I'm a Discord Bot written in Python by FreddyS#5025. Thanks for adding me to your server")
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    embed.add_field(name="Information", value="If you want to get to know all my features, simply type: f help", inline=False)
    embed.add_field(name="Important", value="If you want to use all my features, make sure to give me admin permissions", inline=False)

    await guild.text_channels[0].send(embed=embed)

    newpath = f"./guilds/{guild.id}"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    else:
        pass

@client.event
async def on_guild_remove(guild):
    path = f"./guilds/{guild.id}"
    if os.path.exists(path):
        shutil.rmtree(path)
    else:
        pass

@client.command()
@commands.is_owner()
async def testing(ctx, test_mode: bool):
    if test_mode:
        for file in os.listdir("./cogs"):
            if file.endswith(".py") and file != "__init__.py":
                try:
                    client.unload_extension(f"cogs.{file[:-3]}")
                except Exception as e:
                    print(e)

        await client.change_presence(activity=discord.Game(name="Developer mode / Na"))

        await ctx.send("`Unloaded all extensions.`")

    else:
        for file in os.listdir("./cogs"):
            if file.endswith(".py") and file != "__init__.py":
                try:
                    client.load_extension(f"cogs.{file[:-3]}")
                except Exception as e:
                    print(e)

        await ctx.send("`Loaded all extensions.`")

@client.command()
@commands.is_owner()
async def unload(ctx, cog):
    try:
        client.unload_extension(f"cogs.{cog}")
        await ctx.send(f"`Unloaded {cog}.`")
    except Exception as e:
        print(e)

@client.command()
@commands.is_owner()
async def load(ctx, cog):
    try:
        client.load_extension(f"cogs.{cog}")
        await ctx.send(f"`Loaded {cog}.`")
    except Exception as e:
        print(e)

def loadcogs():
    loaded_extensions = 0
    failed_amount = 0

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                client.load_extension(f"cogs.{filename[:-3]}")
                loaded_extensions += 1
                print(f"Loaded {filename} \n"f" --------------------")
            except Exception as e:
                failed_extensions.append(filename)
                failed_amount += 1
                print(f"Failed to load {filename} \n"f"{e} \n"f"--------------------")

    print(f"Loaded successfully: {loaded_extensions} \n" f"--------------------")
    print(f"Failed to load: {failed_amount} \n")

    for failed_extension in failed_extensions:
        print(failed_extension)
    print(f"--------------------")

if __name__ == "__main__":
    loadcogs()

client.run(os.environ["TOKEN"])



