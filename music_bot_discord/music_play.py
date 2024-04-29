import discord
from discord.ext import commands

from youtube_dl import YoutubeDL
from spotify_dl import SpotifyDL

class MusicPlay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'nonplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnected_delay_max 5', 'options': '-vn' }
        self.vc = None

    def search_yt_spotify(self, item):
        ydl = YoutubeDL(self.YDL_OPTIONS)
        with ydl:
            try:
                # Attempt to search in YouTube
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
                return {'source': info['formats'][0]['url'], 'title': info['title']}
            except Exception:
                # If searching in YouTube fails, try searching in Spotify
                try:
                    info = SpotifyDL().search_song(item)
                    return {'source': info['url'], 'title': info['title']}
                except Exception:
                    return False

    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.bot.loop.create_task(self.play_next()))
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.vc is None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc is None:
                    await ctx.send("I am afraid I could not join the voice channel")
                    return
                else:
                    await self.vc.move_to(self.music_queue[0][1])

                self.music_queue.pop(0)
                self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.bot.loop.create_task(self.play_next()))
            else:
                self.is_playing = False

    @commands.command(name="play", aliases=["p", "playing"], help="Play the selected song")
    async def play(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("You have to be in a Voice Channel in order to play some music, so please connect or get slapped!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt_spotify(query)
            if type(song) == type(True):
                await ctx.send("Could not find the song. Incorrect format, try a different song")
            else:
                await ctx.send("Song was successfully added to the Queue")
                self.music_queue.append([song, voice_channel])
                if not self.is_playing:
                    await self.play_music(ctx)

    @commands.command(name="pause", help="The current track/song has been paused")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name="resume", aliases=["r"], help="Resume playing the current track/song")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False

    @commands.command(name="skip", aliases=["s"], help="Skip the current track/song")
    async def skip(self, ctx, *args):
        if self.vc is not None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name="queue", aliases=["q"], help="Display all the songs currently in the queue")
    async def queue(self, ctx):
        if self.music_queue:
            await ctx.send("\n".join([song[0]['title'] for song in self.music_queue[:5]]))
        else:
            await ctx.send("No music currently in the Queue.")

    @commands.command(name="clear", aliases=["c", "bin"], help="Stop the current track/song and clear the Queue")
    async def clear(self, ctx):
        if self.vc is not None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("The music queue has been cleared.")

    @commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Kick the bot from the Voice Channel")
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = False
        if self.vc is not None and self.vc.is_connected():
            await self.vc.disconnect()