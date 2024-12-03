import discord
from discord.ext import commands

class MusicHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.help_message = """
```
General commands, please use common sense:
!help_puhinator
Description: Display all the available commands

!play_puhinator <keywords>
Aliases: !p_puhinator, !playing_puhinator
Description: Finds and plays a song/track from YouTube or Spotify.

!pause_puhinator
Description: Pauses the current playing track.

!resume_puhinator
Aliases: !r_puhinator
Description: Resumes playing the paused track.

!skip_puhinator
Aliases: !s_puhinator
Description: Skips the current track and plays the next one in the queue.

!queue_puhinator
Aliases: !q_puhinator
Description: Displays the songs currently in the queue.

!clear_puhinator
Aliases: !c_puhinator, !bin_puhinator
Description: Stops the current track and clears the queue.

!leave_puhinator
Aliases: !disconnect_puhinator, !l_puhinator, !d_puhinator
Description: Disconnects the bot from the voice channel.

!display_queue_puhinator
Aliases: !dq_puhinator
Description: Displays all songs in the queue and deletes the message after 60 seconds.

!remove_puhinator <position>
Aliases: !rm_puhinator
Description: Removes a song from the queue at the specified position.

!play_from_queue_puhinator <position>
Aliases: !pfq_puhinator
Description: Plays a song from a specific position in the queue.
```
"""
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready.')
        
    @commands.command(name="help_puhinator", help="Display all the available commands")
    async def help_puhinator(self, ctx):
        await ctx.send(self.help_message)

async def setup(bot):
    await bot.add_cog(MusicHelp(bot))