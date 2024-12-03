import discord
from discord.ext import commands
import traceback
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

# Function to read token from .tokens file
def read_token_from_file():
    with open('.tokens', 'r') as file:
        return file.read().strip()
    
# Define intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Remove the default help command
bot.remove_command("help")

# Load extensions
async def load_extensions():
    extensions = ["music_help", "music_play"]
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            print(f"Extension '{extension}' loaded successfully.")
        except Exception as e:
            print(f"Failed to load extension '{extension}': {e}")
            traceback.print_exc()

# Get the token from the file
token = read_token_from_file()


# Event loop
async def main():
    try:
        await load_extensions()
        await bot.start(token)
    except KeyboardInterrupt:
        await bot.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        await bot.close()

# Bot event for starting to play a song
@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None and after.channel.guild.voice_client is not None and not bot.voice_clients:
        vc = after.channel.guild.voice_client
        if not vc.is_playing():
            # Send a message indicating that the bot has started playing the next song
            await after.channel.send("Now playing the next song.")
            vc.resume()

# Call the main coroutine directly
if __name__ == "__main__":
    asyncio.run(main())