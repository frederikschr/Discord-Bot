import discord
from discord.ext import commands
import os
import youtube_dl
from discord.utils import get
import json
from requestings.get_url import get_url
import asyncio

class musicbot():

    def __init__(self, client):
        self.client = client
        self.song_queue = []
        self.looping = False

    def bot_is_connected(self, ctx):
        voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
        return voice_client and voice_client.is_connected()

    @commands.command()
    async def play_next_song(self, ctx):

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if not self.looping:

            try:
                for song in os.listdir(f"./guilds/{ctx.guild.id}"):
                    if song.endswith(".mp3"):
                        file = os.path.join(f"./guilds/{ctx.guild.id}", song)

                        os.remove(file)
                        print(f"Removed file: {song}")

                ydl_opts = {
                    'outtmpl': f'./guilds/{ctx.guild.id}/%(title)s.%(ext)s',
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.song_queue[0]])
                    meta = ydl.extract_info(self.song_queue[0], download=False)
                    video_name = (meta["title"])

                    try:
                        embed = discord.Embed(
                            title="Now Playing",
                            color=discord.Color.red(),
                            description=f"[{video_name}]({self.song_queue[0]})",
                            value=f"{ctx.author}")

                        await ctx.send(embed=embed)

                    except RuntimeError:
                        pass

                    del self.song_queue[0]

                for file in os.listdir(f"./guilds/{ctx.guild.id}"):
                    if file.endswith(".mp3"):
                        old_file = os.path.join(f"./guilds/{ctx.guild.id}", f"{file}")
                        new_file = os.path.join(f"./guilds/{ctx.guild.id}", "song.mp3")

                        os.rename(old_file, new_file)

                print(f"Song Queue: {self.song_queue}")

                voice.play(discord.FFmpegPCMAudio(f"./guilds/{ctx.guild.id}/song.mp3"),
                           after=lambda e: asyncio.run(self.play_next_song(self, ctx)))

            except IndexError:
                if not self.song_queue:
                    print("Finished playing...")
                else:
                    pass
        else:
            try:
                await asyncio.sleep(3)

                voice.play(discord.FFmpegPCMAudio(f"./guilds/{ctx.guild.id}/song.mp3"),
                           after=lambda e: asyncio.run(self.play_next_song(self, ctx)))

            except AttributeError:
                self.looping = False
                print("Finished playing...")


    @commands.command()
    async def play(self, ctx, *, url):

        for file in os.listdir(f"./guilds/{ctx.guild.id}"):
            try:
                if file.endswith(".mp3"):
                    file = os.path.join(f"./guilds/{ctx.guild.id}", file)
                    os.remove(file)
                    print(f"Removed file: {file}")

            except Exception:

                print("error because song is playing. adding to queue")

                async with ctx.typing():
                    try:
                        with open("./json/playlists.json", "r") as f:
                            data = json.load(f)
                            temp = data[url]
                            for song in temp:
                                print(song)
                                self.song_queue.append(song)

                            queue_index = len(self.song_queue)
                            embed = discord.Embed(title=f"In queue position: {queue_index}", color=discord.Color.red())
                            embed.add_field(name=f"{temp}", value=f"{ctx.author}")
                            await ctx.send(embed=embed)

                            return

                    except Exception:

                        video = get_url(f"{url}")
                        self.song_queue.append(video)
                        queue_index = len(self.song_queue)

                        embed = discord.Embed(title=f"In queue position: {queue_index}", color=discord.Color.red())
                        embed.add_field(name=f"{video}", value=f"{ctx.author}")
                        await ctx.send(embed=embed)

                        return


        print("no error. everything's fine.")

        async with ctx.typing():

            if ctx.author.voice and ctx.author.voice.channel:

                channel = ctx.author.voice.channel

                if not self.bot_is_connected(ctx):
                    await channel.connect()
                else:
                    pass
            else:
                await ctx.send("`You are not connected to a voice channel.`")

                return

            with open("./json/playlists.json", "r") as f:
                data = json.load(f)
                try:
                    temp = data[url]
                    for song in temp:
                        print(song)
                        self.song_queue.append(song)

                except Exception:

                    video = get_url(f"{url}")
                    print(f"Added Video: {video}")
                    self.song_queue.append(video)
                    print(f"Song Queue 1: {self.song_queue}")

        await self.play_next_song(self, ctx)

    @commands.command()
    async def download(self, ctx, song_name: str, song_artist, url: str):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("`Can't download while song is playing.`")
            return

        with open("./json/songs.json", "r") as f:
            artists = json.load(f)

        artists[str(song_name)] = song_artist

        with open("./json/songs.json", "w") as f:
            json.dump(artists, f, indent=4)

        ydl_opts = {
            'outtmpl': f'./audio/%(title)s.%(ext)s',  # Output directory
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',

            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir("./audio"):
            if file.startswith("s."):
                pass

            else:
                print(file)
                old_file = os.path.join("./audio", f"{file}")
                new_file = os.path.join("./audio", f"s.{song_name}.mp3")
                os.rename(old_file, new_file)
                print(f"renamed {file}")

    @commands.command()
    async def createplaylist(self, ctx, playlist_name: str):
        with open("./json/playlists.json") as f:
            data = json.load(f)

            playlist = playlist_name

            newlist = playlist = {
                f"{playlist}": []
            }

            data.update(newlist)

        with open("./json/playlists.json", "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"`Successfully created playlist: {playlist_name}`")

    @commands.command()
    async def deleteplaylist(self, ctx, playlist_name):
        with open("./json/playlists.json", "r") as f:
            data = json.load(f)
            try:
                del data[playlist_name]
                await ctx.send(f"`Successfully deleted playlist: {playlist_name}`")

            except Exception:
                await ctx.send(f"`No playlist named: {playlist_name}`")

        with open("./json/playlists.json", "w") as f:
            json.dump(data, f, indent=4)

    @commands.command()
    async def addplaylist(self, ctx, playlist_name: str, url: str):
        with open("./json/playlists.json", "r") as f:
            data = json.load(f)

            try:
                temp = data[playlist_name]
                new_data = str(url)
                temp.append(new_data)

            except Exception:
                await ctx.send(f"`No playlist named: {playlist_name}`")

        with open("./json/playlists.json", "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"`Successfully added to {playlist_name}: {url}`")

    @commands.command()
    async def removeplaylist(self, ctx, playlist_name: str, url: str):
        with open("./json/playlists.json", "r") as f:
            data = json.load(f)

            try:
                temp = data[playlist_name]

                temp.remove(url)

                await ctx.send(f"`Successfully removed from {playlist_name}: {url}`")

            except Exception:
                await ctx.send(f"`Playlist or song not found.`")

        with open("./json/playlists.json", "w") as f:
            json.dump(data, f, indent=4)

    @commands.command()
    async def clearplaylist(self, ctx, playlist_name: str):

        with open("./json/playlists.json","r") as f:
            data = json.load(f)

            try:

                temp = data[playlist_name]

                temp.clear()

                await ctx.send(f"`Successfully cleared playlist: {playlist_name}`")

            except Exception:
                await ctx.send("`Playlist not found.`")

        with open("./json/playlists.json","w") as f:
            json.dump(data, f, indent=4)

    @commands.command()
    async def getplaylists(self, ctx):
        with open("./json/playlists.json", "r") as f:
            data = json.load(f)

            embed = discord.Embed(title="Playlists", color=discord.Color.red())

            for key, value in data.items():

                songs = ", ".join(value)

                embed.add_field(name=f"{key}", value=f"{songs}", inline=False)

            await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.stop()
        else:
            await ctx.send("`Currently no audio is playing.`")
            return

        try:
            if self.looping:
                self.looping = False
            else:
                pass

            await self.play_next_song(self, ctx)
            await ctx.send("`Skipped to the next song.`")

        except Exception:
            pass

    @commands.command()
    async def playfile(self, ctx, *, song):

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("`Wait for the current playing music to end or use the 'stop' command.`")
            return

        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel

            if not self.bot_is_connected(ctx):
                await channel.connect()
            else:
                pass

        else:
            await ctx.send("`You are not connected to a voice channel.`")

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if os.path.isfile(f"./audio/s.{song}.mp3"):
            voice.play(discord.FFmpegPCMAudio(f"./audio/s.{song}.mp3"))

        else:
            await ctx.send(f"`No song named: {song}`")


    @commands.command()
    async def leave(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

        self.song_queue.clear()

    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()

            await ctx.message.add_reaction("▶️")

        else:
            await ctx.send("`Currently no audio is playing.`")

    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():

            voice.resume()

            await ctx.message.add_reaction("⏸️️")

        else:
            await ctx.send("`Currently no audio is playing.`")

    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            if self.looping:
                self.looping = False
            else:
                pass

            voice.stop()

            await ctx.message.add_reaction("🛑")

        else:
            await ctx.send("`Currently no audio is playing.`")

        self.song_queue.clear()

    @commands.command()
    async def loop(self, ctx):

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice.is_playing():

            self.looping = True

            await ctx.message.add_reaction("🔁")

        else:
            await ctx.send("`Currently no audio is playing.`")

    @commands.command()
    async def getsongs(self, ctx):

        with open("./json/songs.json") as f:
            songs = json.load(f)

        if len(songs) == 0:
            await ctx.send("`Currently no songs are downloaded.`")

        else:
            embed = discord.Embed(title="Downloaded Songs", color=discord.Color.red())

            for key, value in songs.items():
                embed.add_field(name=f"{key}", value=f"{value}", inline=False)

            await ctx.send(embed=embed)

class manager(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.guilds = {}

    @commands.command()
    async def play(self, ctx, *, url):
        for key, value in self.guilds.items():
            if key == str(ctx.guild.id):

                await value.play(value, ctx, url=url)
                return

        object_name = ctx.guild.id
        object_name = musicbot(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.play(object_name, ctx, url=url)

    @commands.command()
    async def playfile(self, ctx, *, song):
        for key, value in self.guilds.items():
            if key == str(ctx.guild.id):
                await value.playfile(value, ctx, song=song)
                return

        object_name = ctx.guild.id
        object_name = musicbot(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.playfile(object_name, ctx, song=song)

    @commands.command()
    async def download(self, ctx, song_name: str, song_artist, url: str):
        for key, value in self.guilds.items():

            if key == str(ctx.guild.id):
                await value.download(value, ctx, song_name, song_artist, url)
                return

        object_name = ctx.guild.id
        object_name = musicbot(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.download(object_name, ctx, song_name, song_artist, url)

    @commands.command()
    async def skip(self, ctx):
        for key, value in self.guilds.items():

            if key == str(ctx.guild.id):
                await value.skip(value, ctx)
                return

        object_name = ctx.guild.id
        object_name = musicbot(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.skip(object_name, ctx)

    @commands.command()
    async def createplaylist(self, ctx, playlist_name: str):
        for key, value in self.guilds.items():

            if key == str(ctx.guild.id):

                await value.createplaylist(value, ctx, playlist_name)
                return

        object_name = ctx.guild.id
        object_name = musicbot(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.createplaylist(object_name, ctx, playlist_name)

    @commands.command()
    async def removeplaylist(self, ctx, playlist_name: str, url: str):
        for key, value in self.guilds.items():

            if key == str(ctx.guild.id):
                await value.removeplaylist(value, ctx, playlist_name, url)
                return

        object_name = ctx.guild.id
        object_name = musicbot(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.removeplaylist(object_name, ctx, playlist_name, url)

    @commands.command()
    async def deleteplaylist(self, ctx, playlist_name):
        for key, value in self.guilds.items():

            if key == str(ctx.guild.id):
                await value.deleteplaylist(value, ctx, playlist_name)
                return

        object_name = ctx.guild.id
        object_name = musicbot(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.deleteplaylist(object_name, ctx, playlist_name)

    @commands.command()
    async def clearplaylist(self, ctx, playlist_name):
        for key, value in self.guilds.items():

            if key == str(ctx.guild.id):
                await value.clearplaylist(value, ctx, playlist_name)
                return

        object_name = ctx.guild.id
        object_name = musicbot(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.clearplaylist(object_name, ctx, playlist_name)

    @commands.command()
    async def addplaylist(self, ctx, playlist_name: str, url: str):
        for key, value in self.guilds.items():

            if key == str(ctx.guild.id):

                await value.addplaylist(value, ctx, playlist_name, url)
                return

        object_name = ctx.guild.id
        object_name = musicbot(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.addplaylist(object_name, ctx, playlist_name, url)

    @commands.command()
    async def skip(self, ctx):
        for key, value in self.guilds.items():

            if key == str(ctx.guild.id):

                await value.skip(value, ctx)
                return

        object_name = ctx.guild.id
        object_name = musicbot(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.skip(object_name, ctx)

    @commands.command()
    async def pause(self, ctx):
        for key, value in self.guilds.items():

            if key == str(ctx.guild.id):
                await value.pause(value, ctx)
                return

        object_name = ctx.guild.id
        object_name = musicbot(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.pause(object_name, ctx)

    @commands.command()
    async def stop(self, ctx):
        for key, value in self.guilds.items():

            if key == str(ctx.guild.id):
                await value.stop(value, ctx)
                return

        object_name = ctx.guild.id
        object_name = musicbot(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.stop(object_name, ctx)

    @commands.command()
    async def resume(self, ctx):
        for key, value in self.guilds.items():

            if key == str(ctx.guild.id):
                await value.resume(value, ctx)
                return

        object_name = ctx.guild.id
        object_name = musicbot(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.resume(object_name, ctx)

    @commands.command()
    async def loop(self, ctx):
        for key, value in self.guilds.items():

            if key == str(ctx.guild.id):
                await value.loop(value, ctx)
                return

        object_name = ctx.guild.id
        object_name = musicbot(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.loop(object_name, ctx)

    @commands.command()
    async def leave(self, ctx):
        for key, value in self.guilds.items():

            if key == str(ctx.guild.id):
                await value.leave(value, ctx)
                return

        object_name = ctx.guild.id
        object_name = musicbot(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.leave(object_name, ctx)

    @commands.command()
    async def getsongs(self, ctx):
        for key, value in self.guilds.items():

            if key == str(ctx.guild.id):
                await value.getsongs(value, ctx)
                return

        object_name = ctx.guild.id
        object_name = musicbot(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.getsongs(object_name, ctx)

    @commands.command()
    async def getplaylists(self, ctx):
        for key, value in self.guilds.items():

            if key == str(ctx.guild.id):
                await value.getplaylists(value, ctx)
                return

        object_name = ctx.guild.id
        object_name = musicbot(self.client)
        self.guilds[str(ctx.guild.id)] = object_name

        await object_name.getplaylists(object_name, ctx)

def setup(client):
    client.add_cog(manager(client))
