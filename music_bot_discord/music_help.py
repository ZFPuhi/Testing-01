import discord
from discord.ext import commands
import asyncio

class MusicHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.help_message = """
```
General commands, please use common sense:
/help
/p <keywords> - finds the song on youtube and plays it
/q - Displays the current music in Queue
/skip - skips current song
/clear - Stops current song and clears Queue
/leave - Bot disconnects
/pause - pauses the current song/track
/resume - resumes the current song/track
```
"""
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                await channel.send(self.help_message)

    @commands.command(name="help_puhinator", help="Display all the available commands")
    async def help_puhinator(self, ctx):  # Changed command name
        await ctx.send(self.help_message)

def setup(bot):
    bot.add_cog(MusicHelp(bot))
