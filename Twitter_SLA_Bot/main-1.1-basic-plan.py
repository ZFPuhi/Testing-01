import discord
import tweepy
import asyncio
import os
import time
from tweepy.errors import TweepyException, Forbidden

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

# Read Twitter credentials and accounts
twitter_credentials = read_credentials(TWITTER_FILE_PATH)
CONSUMER_KEY = twitter_credentials['CONSUMER_KEY']
CONSUMER_SECRET = twitter_credentials['CONSUMER_SECRET']
ACCESS_TOKEN = twitter_credentials.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = twitter_credentials.get('ACCESS_TOKEN_SECRET')
TWITTER_ACCOUNTS = twitter_credentials['TWITTER_ACCOUNTS'].split(',')

# Read Discord token and channel ID
discord_credentials = read_credentials(DISCORD_FILE_PATH)
DISCORD_TOKEN = discord_credentials['DISCORD_TOKEN']
DISCORD_CHANNEL_ID = int(discord_credentials['DISCORD_CHANNEL_ID'])

# Print the loaded configuration for verification
print(f"Discord Channel ID: {DISCORD_CHANNEL_ID}")
print(f"Twitter Accounts to Monitor: {TWITTER_ACCOUNTS}")

# Initialize Twitter API Client for v1.1
auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        self.bg_task = self.loop.create_task(self.check_tweets())

    async def check_tweets(self):
        await self.wait_until_ready()
        channel = self.get_channel(DISCORD_CHANNEL_ID)
        while not self.is_closed():
            try:
                for account in TWITTER_ACCOUNTS:
                    print(f"Checking tweets for account: {account}")
                    tweets = api.user_timeline(screen_name=account, count=1, tweet_mode="extended")
                    if tweets:
                        latest_tweet = tweets[0]
                        tweet_url = f"https://twitter.com/{account}/status/{latest_tweet.id}"
                        await channel.send(f"New tweet from {account}: {tweet_url}")
                    await asyncio.sleep(15)  # Wait for 15 seconds before checking the next account
            except tweepy.TweepyException as e:
                if 'Rate limit exceeded' in str(e):
                    print("Rate limit reached. Sleeping for 15 minutes.")
                    await asyncio.sleep(15 * 60)
                else:
                    print(f"Error fetching tweets: {e}")
            except Forbidden as e:
                print(f"Access forbidden: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
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
            try:
                print(f"Manually checking tweets for account: {account}")
                tweets = api.user_timeline(screen_name=account, count=1, tweet_mode="extended")
                if tweets:
                    latest_tweet = tweets[0]
                    tweet_url = f"https://twitter.com/{account}/status/{latest_tweet.id}"
                    await channel.send(f"New tweet from {account}: {tweet_url}")
                await asyncio.sleep(15)  # Wait for 15 seconds before checking the next account
            except tweepy.TweepyException as e:
                if 'Rate limit exceeded' in str(e):
                    await channel.send("Rate limit reached. Please try again later.")
                    break
                else:
                    await channel.send(f"Error fetching tweets for {account}: {e}")
            except Forbidden as e:
                await channel.send(f"Access forbidden: {e}")
                break
            except Exception as e:
                await channel.send(f"An error occurred while fetching tweets for {account}: {e}")

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
client = MyClient(intents=intents)

client.run(DISCORD_TOKEN)