import discord
from discord.ext import commands
import asyncio
import spotify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import youtube_dl
import os
import googleapiclient.discovery
import re
import pytube

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
        self.ytdl = youtube_dl.YoutubeDL(self.YDL_OPTIONS)

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

    #Search on Youtube / Spotify
    def search_yt_spotify(self, item):
        ydl = youtube_dl.YoutubeDL(self.YDL_OPTIONS)
        with ydl:
            try:
                # Check if the provided item is a Spotify URL
                if 'open.spotify.com' in item:
                    print("Processing Spotify URL...")
                    # Extract the track ID from the Spotify URL
                    track_id = item.split('/')[-1].split('?')[0]
                    print("Track ID:", track_id)
                    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=self.spotify_client_id, client_secret=self.spotify_client_secret))
                    # Get track details using the track ID
                    track_info = sp.track(track_id)
                    print("Track Info:", track_info)
                    if track_info and 'preview_url' in track_info:
                        source_url = track_info['preview_url']
                        print("Preview URL:", source_url)
                        return {'source': source_url, 'title': track_info['name']}
                    else:
                        print("Preview URL not found for the Spotify track.")
                        return False
                else:
                    # Attempt to search in YouTube
                    info = ydl.extract_info("ytsearch:%s" % item, download=False)
                    if 'entries' in info and info['entries']:
                        youtube_result = info['entries'][0]
                        if 'formats' in youtube_result and youtube_result['formats']:
                            # Extract the video URL from the search results
                            source_url = youtube_result['formats'][0]['url']
                            return {'source': source_url, 'title': youtube_result['title']}
                        else:
                            print("Video URL not found in the search results.")
                    else:
                        print("No entries found in YouTube search results.")
                    return False
            except spotipy.SpotifyException as e:
                print(f"Spotify API error: {e}")
                return False
            except Exception as e:
                print(f"Error searching in YouTube and Spotify: {e}")
                return False

    # Get song playtime
    async def get_song_playtime(self, song):
        if 'youtube' in song['source']:
            try:
                with open('.youtubeapi', 'r') as api_file:
                    api_key = api_file.read().strip()
            except FileNotFoundError:
                print("YouTube API key file not found.")
                return "Unknown", song['source']

            if "watch?v=" in song['source']:
                video_id = song['source'].split("watch?v=")[1].split("&")[0]
            else:
                print("Video ID not found in the source URL.")
                return "Unknown", song['source']

            youtube_url = f"https://www.youtube.com/watch?v={video_id}"

            try:
                video = pytube.YouTube(youtube_url)
                duration = video.length
                print(f"Video duration: {duration} seconds")

                playtime = self.format_duration(duration)
                print(f"Parsed playtime: {playtime}")
                return playtime, youtube_url
            except Exception as e:
                print(f"Error fetching video duration: {e}")
                return "Unknown", song['source']
        else:
            return "Unknown", song['source']
        
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
            return
        elif self.is_paused:
            self.vc.resume()
            return

        song = self.search_yt_spotify(query)
        if song:
            if type(song) == type(True):
                await ctx.send("Could not find the song. Incorrect format, try a different song")
            else:
                playtime, source_url = await self.get_song_playtime(song)
                if source_url:
                    # Send a message containing the details of the song that was added to the queue
                    await ctx.send(f"Song added to queue: **{song['title']}**\nPlaytime: {playtime}\n")
                    self.music_queue.append([song, voice_channel])
                    if not self.is_playing:
                        await self.play_music(ctx)
                else:
                    await ctx.send("Failed to retrieve the source URL of the song. Please try again later.")
        else:
            await ctx.send("Could not find the song. Please try a different song name or keywords.")

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