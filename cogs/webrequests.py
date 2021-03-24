import discord
from discord.ext import commands
import requests
import datetime
from datetime import timezone
import googlemaps
from dotenv import load_dotenv
import os

load_dotenv()

class tests(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.pic = "https://cdn.discordapp.com/attachments/817341565357129758/818964373267677184/iss-weltall-1002400x1350.png"

    @commands.command()
    async def iss(self, ctx):
        iss_position = requests.get(
            "http://api.open-notify.org/iss-now.json",
        ).json()["iss_position"]

        dt = datetime.datetime.now()
        utc_time = dt.replace(tzinfo=timezone.utc)

        key = os.environ["GOOGLE_API_KEY"]
        gmaps = googlemaps.Client(key=key)

        output = [
            round(float(iss_position['latitude']), 2),
            round(float(iss_position['longitude']), 2),
            utc_time
        ]

        try:
            reverse_geocode_result = gmaps.reverse_geocode((iss_position['latitude'], iss_position['longitude']))
            address = reverse_geocode_result[0]["formatted_address"]

        except IndexError:

            address = "Not available"

        people_list = []

        people = requests.get("http://api.open-notify.org/astros.json").json()["people"]

        for person_names in people:
            people_list.append(person_names["name"])

        names = ", ".join(people_list)

        latitude = ""
        longitude = ""

        if output[0] >= 0:
            latitude = "North"
        else:
            output[0] *= (-1)
            latitude = "South"

        if output[1] >= 0:
            longitude = "East"
        else:
            output[1] *= (-1)
            longitude = "West"

        position = "{}° {} \n {}° {}".format(output[0], latitude, output[1], longitude)

        time = f"{output[2]}"
        time_sliced = f"{time[:-13]} UTC"

        embed = discord.Embed(title="International Space Station", color=discord.Color.red())
        embed.add_field(name="Position", value=position, inline=False)
        embed.add_field(name="Location", value=address, inline=False)
        embed.add_field(name="Onboard", value=names)
        embed.add_field(name="Time", value=time_sliced, inline=False)
        embed.set_image(url=self.pic)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(tests(client))
