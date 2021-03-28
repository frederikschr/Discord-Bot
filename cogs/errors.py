from discord.ext import commands

class errors(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("`Invalid command used.`")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("`Command is missing an Argument.`")

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("`Missing required permissions.`")

        elif isinstance(error, commands.ChannelNotFound):
            await ctx.send("`No channel found.`")

        elif isinstance(error, commands.NotOwner):
            await ctx.send("`Only the Owner can use this command.`")

        elif isinstance(error, commands.BadArgument):
            await ctx.send("`Please choose the correct datatype.`")

        #elif isinstance(error, commands.CommandInvokeError):
            #pass

def setup(client):
    client.add_cog(errors(client))