from discord.ext import commands

class calculator(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def calc(self, ctx, num1, cal, num2):
        try:
            if cal == "+":
                x = int(num1) + int(num2)
                await ctx.send(f"`{x}`")

            elif cal == "-":
                x = int(num1) - int(num2)
                await ctx.send(f"`{x}`")

            elif cal == "*":
                x = int(num1) * int(num2)
                await ctx.send(f"`{x}`")

            elif cal == ":":
                x = int(num1) / int(num2)
                x = int(x)
                await ctx.send(f"`{x}`")

            else:
                await ctx.send("`The operator you entered is invalid.`")

        except ValueError:
            await ctx.send("`You entered a wrong datatype.`")

def setup(client):
    client.add_cog(calculator(client))