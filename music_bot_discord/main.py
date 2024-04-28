import discord
from discord.ext import commands
import os

# Function to read token from .token file
def read_token_from_file():
    with open('.token', 'r') as file:
        token = file.read().strip()  # Read the token as a string and remove any leading/trailing whitespace
        return token

from music_help import music_help
from music_play import music_play

bot = commands.Bot(command_prefix='!')

bot.remove_command("help")

bot.add_cog(music_help(bot))
bot.add_cog(music_play(bot))

# Get the token from the file
token = read_token_from_file()

# Run the client with the token
bot.run(token)