import discord
from discord.ext import commands

# Function to read token from .token file
def read_token_from_file():
    with open('.token', 'r') as file:
        return file.read().strip()

bot = commands.Bot(command_prefix='!')

bot.remove_command("help")

bot.load_extension("music_help")
bot.load_extension("music_play")

# Get the token from the file
token = read_token_from_file()

# Run the client with the token
bot.run(token)
