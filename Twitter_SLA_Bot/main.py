import discord
import asyncio
import os
import requests
from bs4 import BeautifulSoup

# Function to read credentials from a file
def read_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            credentials[key] = value
    return credentials

# Paths to the credentials files
TWITTER_FILE_PATH = '.twitter'
DISCORD_FILE_PATH = '.discord'

# Read Twitter accounts
twitter_credentials = read_credentials(TWITTER_FILE_PATH)
TWITTER_ACCOUNTS = twitter_credentials['TWITTER_ACCOUNTS'].split(',')

# Read Discord token and channel ID
discord_credentials = read_credentials(DISCORD_FILE_PATH)
DISCORD_TOKEN = discord_credentials['DISCORD_TOKEN']
DISCORD_CHANNEL_ID = int(discord_credentials['DISCORD_CHANNEL_ID'])

# Print the loaded configuration for verification
print(f"Discord Channel ID: {DISCORD_CHANNEL_ID}")
print(f"Twitter Accounts to Monitor: {TWITTER_ACCOUNTS}")

# Function to get the latest tweet from a Twitter profile
def get_latest_tweet(username):
    try:
        url = f"https://twitter.com/{username}"
        print(f"Fetching tweets for {username} from {url}")
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for tweet text within a specific tag and class
        tweets = soup.find_all('div', {'data-testid': 'tweet'})
        if tweets:
            latest_tweet = tweets[0]
            tweet_id = latest_tweet['data-tweet-id']
            tweet_url = f"https://twitter.com/{username}/status/{tweet_id}"
            print(f"Found tweet for {username}: {tweet_url}")
            return tweet_url
        else:
            print(f"No tweets found for {username}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching tweets for {username}: {e}")
        return None

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        self.bg_task = self.loop.create_task(self.check_tweets())

    async def check_tweets(self):
        await self.wait_until_ready()
        channel = self.get_channel(DISCORD_CHANNEL_ID)
        while not self.is_closed():
            for account in TWITTER_ACCOUNTS:
                print(f"Checking tweets for account: {account}")
                tweet_url = get_latest_tweet(account)
                if tweet_url:
                    await channel.send(f"New tweet from {account}: {tweet_url}")
                await asyncio.sleep(15)  # Wait for 15 seconds before checking the next account
            await asyncio.sleep(300)  # Check every 5 minutes

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == '!checktweets':
            print(f"Received command from {message.author}: {message.content}")
            await self.manual_check_tweets()

    async def manual_check_tweets(self):
        channel = self.get_channel(DISCORD_CHANNEL_ID)
        for account in TWITTER_ACCOUNTS:
            print(f"Manually checking tweets for account: {account}")
            tweet_url = get_latest_tweet(account)
            if tweet_url:
                await channel.send(f"New tweet from {account}: {tweet_url}")
            await asyncio.sleep(15)  # Wait for 15 seconds before checking the next account

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
client = MyClient(intents=intents)

client.run(DISCORD_TOKEN)
