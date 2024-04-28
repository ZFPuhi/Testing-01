import discord
from discord.ext import commands

from youtube_dl import YoutubeDL
from spotify_dl import SpotifyDL

class music_play(commands.Bot):
    def __init__(self, bot):
        self.bot = bot
        
        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'nonplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnected_delay_max 5', 'options': '-vn' }

        self.vc = None

#def search_yt(self, item):
#    with YoutubeDL(self.YDL_OPTIONS) as ydl:
#        try:
#            info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
#        except Exception:
#            return False
#    return {'source': info['formats'[0]['url']], 'title': info['title']}

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

def play_next(self):
    if len(self.music_queue) > 0:
        self.is_playing = True

        m_url = self.music_queue[0][0]['source']
        self.music_queue.pop(0)
        self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
    else:
        self.is_playing = False

async def play_music(self, ctx):
    if len(self.music_queue) > 0:
        self.is_playing = True
        m_url = self.music_queue[0][0]['source']

        if self.vc == None or not self.vc.is_connected():
            self.vc == await self.music_queue[0][1].connect()

            if self.vc == None:
                await ctx.send("I am afraid I could not join the voice channel")
                return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e:self.play_next())

        else:
            self.is_playing = False

# Command that will play the desired track/song.
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
                if self.is_playing == False:
                    await self.play_music(ctx)

# Command that will Pause the current track/song that is playing.
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

# Command that will Resume and continue to play the current song.
    @commands.command(name="resume", aliases=["r"], help="Resume playing the current track/song")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.pause()

# Command that will Skip the current song.
    @commands.command(name="skip", aliases=["s"], help="Skip the current track/song")
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

# Command that will display the next 4 songs, in order to not fill the chat if there are too many songs in the Queue.
@commands.command(name="queue", aliases=["q"], help="Display all the songs currently in the queue")
async def queue(self, ctx):
    retval = ""
    for i in range(0, len(self.music_queue)):
        if i > 4: break
        retval += self.music_queue[i][0]['title'] + '\n'
    if retval != "":
        await ctx.send(retval)
    else:
        await ctx.send("No music curerntly in the Queue.")

# Command that will stop and clear the current Queue
@commands.command(name="clear", aliases=["c", "bin"], help="Will stop the current track/song that is playing and clear the Queue")
async def clear(self, ctx):
    if self.vc != None and self.is_playing:
        self.vc.stop()
    self.music_queue = []
    await ctx.send("The music queue has been cleared.")

# Command that will kick the bot from the Voice Channel
@commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Kick the bot from the Voice Channel")
async def leave(self, ctx):
    self.is_playing = False
    self.is_paused = False
    await self.vc.disconnect()