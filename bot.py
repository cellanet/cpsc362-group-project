import discord
from discord.ext import commands
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    print("Error: DISCORD_TOKEN is not set")
    exit()

GUILD = os.getenv('DISCORD_GUILD')
if GUILD is None:
    print("Error: DISCORD_GUILD is not set")
    exit()

GUILD_NAME = os.getenv('DISCORD_GUILD_SERVER_NAME')
if GUILD is None:
    print("Error: DISCORD_GUILD is not set")
    exit()

client = commands.Bot(command_prefix="!!", intents=discord.Intents.all())

@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD_NAME, client.guilds)
    if guild is None:
        print("Error: guild not found")
        exit()
    print(
        f'{client.user} has connected to Discord!\n'
        f'{client.user} is connected to the {guild.name}: {guild.id}\n'
    )
    
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.name == "new-channel":
        # check if the author of the message is in a voice channel
        author_voice = message.author.voice
        if author_voice is not None:
            # do something with the message here
            await message.channel.send("I received your message!")
        else:
            # send a message to the channel telling the user to join a voice channel first
            await message.channel.send(f"{message.author.mention}, you need to join a voice channel first!")
    await client.process_commands(message)

    
client.run(TOKEN)