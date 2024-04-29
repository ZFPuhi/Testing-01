import discord
from discord.ext import commands
import asyncio

# Function to read token from .token file
def read_token_from_file():
    with open('.tokens', 'r') as file:
        return file.read().strip()

# Define intents
intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)

# Remove the default help command
bot.remove_command("help")

# Load extensions
extensions = ["music_help", "music_play"]
for extension in extensions:
    bot.load_extension(extension)

# Get the token from the file
token = read_token_from_file()

# Run the client with the token
async def main():
    await bot.start(token)

# Call the main coroutine directly
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())