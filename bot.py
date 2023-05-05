import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import wavelink


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)
    
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!!', intents=intents)

@client.event
async def setup_hook():
    node = wavelink.Node(uri = "http://localhost:2333", password = "youshallnotpass")
    await wavelink.NodePool.connect(client = client, nodes = [node])
    
@client.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f'Node {node.id} is ready!')
    
@client.command()
async def play(ctx: commands.Context, *, track: wavelink.YouTubeTrack):
    print(track)
    if ctx.voice_client:
        vc: wavelink.Player = ctx.voice_client
    elif ctx.author.voice:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls = wavelink.Player)
    else:
        return
    await vc.play(track)
    
    embed = discord.Embed(title= "Now playing", description= track, color= 2123412)
    embed.set_thumbnail(url= await track.fetch_thumbnail())
    
@client.command()
async def disc(ctx: commands.Context):
    vc: wavelink.Player = ctx.voice_client
    await vc.disconnect()
    vc.queue.clear()

client.run(TOKEN)
