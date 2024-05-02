import discord
from discord.ext import commands
import asyncio
import spotify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_dl import YoutubeDL
import yt_dlp as youtube_dl
import os
import googleapiclient.discovery
import re

SPOTIFY_FILE_PATH = ".spotify"

class MusicPlay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio/best'}
        self.FFMPEG_OPTIONS = {'options': '-vn'}
        self.vc = None
        self.ytdl = YoutubeDL(self.YDL_OPTIONS)

        # Extract Spotify credentials from .spotify file
        self.spotify_client_id, self.spotify_client_secret = self.read_spotify_credentials()

        # Print loaded Spotify credentials
        print(f"Spotify Client ID: {self.spotify_client_id}")
        print(f"Spotify Client Secret: {self.spotify_client_secret}")

    def read_spotify_credentials(self):
        # Initialize variables to store client ID and client secret
        spotify_client_id = None
        spotify_client_secret = None
        try:
            # Open the .spotify file and read its contents
            with open(SPOTIFY_FILE_PATH, 'r') as file:
                for line in file:
                    # Split each line into key-value pairs based on the '=' delimiter
                    key, value = line.strip().split('=')

                    # Check if the key is SPOTIPY_CLIENT_ID
                    if key == 'SPOTIPY_CLIENT_ID':
                        spotify_client_id = value
                    # Check if the key is SPOTIPY_CLIENT_SECRET
                    elif key == 'SPOTIPY_CLIENT_SECRET':
                        spotify_client_secret = value

            # Return the extracted Spotify credentials
            return spotify_client_id, spotify_client_secret
        except FileNotFoundError:
            # Handle the case when the .spotify file is not found
            print(".spotify file not found.")
            return None, None
        except Exception as e:
            # Handle any other exceptions that may occur during file reading
            print(f"Error reading .spotify file: {e}")
            return None, None

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
                    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=self.spotify_client_id, client_secret=self.spotify_client_secret))
                    results = sp.search(q=item, limit=1, type='track')
                    track_uri = results['tracks']['items'][0]['uri']
                    track_info = sp.track(track_uri)
                    return {'source': track_info['preview_url'], 'title': track_info['name']}
                except Exception as e:
                    print(e)
                    return False
    async def get_song_playtime(self, song):
        if 'youtube' in song['source']:
            try:
                with open('.youtubeapi', 'r') as api_file:
                    api_key = api_file.read().strip()
                    # Print the API key
                    print(f"YouTube API key loaded: {api_key}")
            except FileNotFoundError:
                print("YouTube API key file not found.")
                return "Unknown"

            print(f"Song source URL: {song['source']}")
            video_id = song['source'].split("watch?v=")[1]
            print(f"Extracted video ID: {video_id}")

            youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
            request = youtube.videos().list(part="contentDetails", id=video_id)
            response = request.execute()
            duration = response['items'][0]['contentDetails']['duration']

            # Parse the duration to get the playtime in HH:MM:SS format
            playtime = self.parse_duration(duration)
            return playtime
        else:
            return "Unknown"
        
    def parse_duration(self, duration):
        match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration)
        hours = int(match.group(1)[0]) if match.group(1) else 0
        minutes = int(match.group(2)[0]) if match.group(2) else 0
        seconds = int(match.group(3)[0]) if match.group(3) else 0

        # Convert duration to HH:MM:SS format
        playtime = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return playtime
            
    async def play_next(self):
        if not self.is_playing and self.music_queue:
            self.is_playing = True
            song = self.music_queue.pop(0)
            m_url = song[0]['source']
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.bot.loop.create_task(self.check_queue()))

    async def check_queue(self):
        while self.vc.is_playing():
            await asyncio.sleep(1)
        else:
            await self.play_next()

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
                
                # Send a message indicating the current song that is playing
                await ctx.send(f"Now playing: {self.music_queue[0][0]['title']}")
            else:
                self.is_playing = False

    @commands.command(name="play_puhinator", aliases=["p_puhinator", "playing_puhinator"], help="Play the selected song")
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
                # Send a message containing the details of the song that was added to the queue
                playtime = await self.get_song_playtime(song)
                await ctx.send(f"Song added to queue: **{song['title']}**\nPlaytime: {playtime}\nLink: {song['source']}")
                self.music_queue.append([song, voice_channel])
                if not self.is_playing:
                    await self.play_music(ctx)

    @commands.command(name="pause_puhinator", help="The current track/song has been paused")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name="resume_puhinator", aliases=["r_puhinator"], help="Resume playing the current track/song")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False

    @commands.command(name="skip_puhinator", aliases=["s_puhinator"], help="Skip the current track/song")
    async def skip(self, ctx, *args):
        if self.vc is not None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name="queue_puhinator", aliases=["q_puhinator"], help="Display all the songs currently in the queue")
    async def queue(self, ctx):
        if self.music_queue:
            await ctx.send("\n".join([song[0]['title'] for song in self.music_queue[:5]]))
        else:
            await ctx.send("No music currently in the Queue.")

    @commands.command(name="clear_puhinator", aliases=["c_puhinator", "bin_puhinator"], help="Stop the current track/song and clear the Queue")
    async def clear(self, ctx):
        if self.vc is not None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("The music queue has been cleared.")

    @commands.command(name="leave_puhinator", aliases=["disconnect_puhinator", "l_puhinator", "d_puhinator"], help="Kick the bot from the Voice Channel")
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = False
        if self.vc is not None and self.vc.is_connected():
            await self.vc.disconnect()

    @commands.command(name="display_queue_puhinator", aliases=["dq_puhinator"], help="Display all the songs in the queue and delete after 60 seconds")
    async def display_queue(self, ctx):
        if self.music_queue:
            songs = "\n".join([song[0]['title'] for song in self.music_queue])
            message = await ctx.send(f"Songs in Queue:\n{songs}")

# Wait for 60 seconds and then delete the message
            await asyncio.sleep(60)
            await message.delete()
        else:
            await ctx.send("No music currently in the Queue.")

    @commands.command(name="remove_puhinator", aliases=["rm_puhinator"], help="Remove a song from the queue")
    async def remove(self, ctx, position: int):
        if 0 <= position < len(self.music_queue):
            removed_song = self.music_queue.pop(position)
            await ctx.send(f"Removed '{removed_song[0]['title']}' from the queue at position {position}.")
        else:
            await ctx.send("Invalid queue position. Please specify a valid position in the queue.")

    @commands.command(name="play_from_queue_puhinator", aliases=["pfq_puhinator"], help="Play a song from a specific position in the queue")
    async def play_from_queue(self, ctx, position: int):
        if 0 <= position < len(self.music_queue):
            song = self.music_queue[position]
            await ctx.send(f"Playing '{song[0]['title']}' from the queue at position {position}.")
            if not self.is_playing:
                await self.play_music(ctx)
        else:
            await ctx.send("Invalid queue position. Please specify a valid position in the queue.")

async def setup(bot):
    await bot.add_cog(MusicPlay(bot))