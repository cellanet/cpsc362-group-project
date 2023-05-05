import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import wavelink


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_NAME = os.getenv('DISCORD_GUILD_SERVER_NAME')
LAVA_ADDRESS = os.getenv("LAVA_ADDRESS", "localhost")
LAVA_PORT = os.getenv("LAVA_PORT", "2333")
LAVA_PASS = os.getenv("LAVA_PASS", "youshallnotpass")
    
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!!', intents=intents)

# Connect to WaveLink
async def on_ready():
    print(f'Logged in {bot.user} | {bot.user.id}')
    guild = discord.utils.find(lambda g: g.name == GUILD_NAME, bot.guilds)
    if guild is None:
        print("Error: guild not found")
        exit()
    print(
        f'{bot.user} has connected to Discord!\n'
        f'{bot.user} is connected to the {guild.name}: {guild.id}\n'
    )
    await connect_nodes()

async def connect_nodes():
    node = wavelink.Node(uri=f'ws://{LAVA_ADDRESS}:{LAVA_PORT}', password=LAVA_PASS)
    await wavelink.NodePool.connect(client=bot, nodes=[node])
    print("Wavelink connected.")

async def on_node_ready(node: wavelink.Node):
    print(f"Node <{node.identifier}> is ready.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.name == "new-channel":
        author_voice = message.author.voice
        if author_voice is not None:
            print(f"Received message from {message.author.name} in voice channel {author_voice.channel.name}")
            await message.channel.send("I received your message!")
        else:
            print(f"Received message from {message.author.name} but they are not in a voice channel")
            await message.channel.send(f"{message.author.mention}, you need to join a voice channel first!")
    await bot.process_commands(message)

@bot.event
async def on_connect():
    print(f'Connected to Discord (latency: {bot.latency*1000:.0f}ms).')

@bot.event
async def on_disconnect():
    print('Disconnected from Discord')

@bot.event
async def on_resumed():
    print('Resumed session with Discord')

bot.run(TOKEN)
