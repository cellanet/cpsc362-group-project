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

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@client.event
async def on_ready():
    # print(f'{client.user} has connected to Discord!')
    # for guild in client.guilds:
    #     print(f"guild.name: {guild.name}, guild.id: {guild.id}")
    guild = discord.utils.find(lambda g: g.name == GUILD_NAME, client.guilds)
    if guild is None:
        print("Error: guild not found")
        exit()
    print(
        f'{client.user} has connected to Discord!\n'
        f'{client.user} is connected to the {guild.name}: {guild.id}\n'
    )

    
client.run(TOKEN)
# import wavelink
# token = 'MTA4MTQ0NjY4NTc2NDQ5MzM0Mg.GhWQTK.IGuLfnuzc7TdHb1GEL0kHclZnK3QPVtZ8D00fs'
# client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


# # # Connects to wavelink
# # @client.event
# # async def on_ready():
# #     client.loop.create_task(connect_nodes())

# # async def connect_nodes():
# #     await client.wait_until_ready()
# #     await wavelink.NodePool.create_node(
# #         bot=client,
# #         host='0.0.0.0',
# #         port = 2333,
# #         password='youshallnotpass'
# #     )

# # @client.event
# # async def on_wavelink_node_ready(node: wavelink.Node):
# #     print(f"Node: <{node.identifier}>")