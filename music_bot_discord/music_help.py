import discord
from discord.ext import commands

class music_help(commands.Bot):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = ""
        self.text_channel_list = []
        self.set_message()

    def set_message(self):
        self.help_message = """"
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

@commands.bot.listener()
async def on_ready(self):
    for guild in self.bot.guilds:
        for channel in guild.text_channels:
            self.text_channel_text.append(channel)

        await self.send_to_all(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_text:
            await text_channel.send(msg)

@commands.command(name="help", help="Display all the available commands")
async def help(self, ctx):
    await ctx.send(self.help_message)