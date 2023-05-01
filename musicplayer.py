import discord
import wavelink
from discord.ext import commands

token = 'MTA4MTQ0NjY4NTc2NDQ5MzM0Mg.GhWQTK.IGuLfnuzc7TdHb1GEL0kHclZnK3QPVtZ8D00fs'
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


# Connects to wavelink
@client.event
async def on_ready():
    client.loop.create_task(connect_nodes())

async def connect_nodes():
    await client.wait_until_ready()
    await wavelink.NodePool.create_node(
        bot=client,
        host='0.0.0.0',
        port = 2333,
        password='youshallnotpass'
    )

@client.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node: <{node.identifier}>")



client.run(token)