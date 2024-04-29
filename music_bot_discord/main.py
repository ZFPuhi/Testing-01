import discord
from discord.ext import commands

# Function to read token from .token file
def read_token_from_file():
    with open('.token', 'r') as file:
        return file.read().strip()

bot = commands.Bot(command_prefix='!')

# Remove the default help command
bot.remove_command("help")

# Load extensions
extensions = ["music_help", "music_play"]
for extension in extensions:
    bot.load_extension(extension)

# Get the token from the file
token = read_token_from_file()

# Run the client with the token
bot.run(token)
