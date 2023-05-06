import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import wavelink


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
REC = os.getenv('RECOMMENDATION')
    
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
    # ctx.send('You need to be in a voice channel to use this command!')
    await ctx.send(f'Total length: {track.duration()} seconds')
    await vc.play(track)

    embed = discord.Embed(title= "Now playing", description= track, color= 2123412)
    embed.set_thumbnail(url= await track.fetch_thumbnail())
    message = await ctx.send(embed = embed)

    # add reactions to the message
    await message.add_reaction('⏸')
    await message.add_reaction('▶')
    await message.add_reaction('⏭️')

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['⏸', '▶', '⏭️']

    while True:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=120.0, check=check)
        except asyncio.TimeoutError:
            # stop listening after 60 seconds
            break
        else:
            if str(reaction.emoji) == '⏸':
                await pause(ctx)
            elif str(reaction.emoji) == '▶':
                await resume(ctx)
            elif str(reaction.emoji) == '⏭️':
                await next(ctx)
            # remove the user's reaction after processing
            await message.remove_reaction(reaction, user)

@client.command()
async def disc(ctx: commands.Context):
    vc: wavelink.Player = ctx.voice_client
    await vc.disconnect()
    vc.queue.clear()
    
@client.command()
async def pause(ctx: commands.Context):
    vc: wavelink.Player = ctx.voice_client
    await vc.pause()
    
@client.command()
async def resume(ctx: commands.Context):
    vc: wavelink.Player = ctx.voice_client
    await vc.resume()

@client.command()
async def rec(ctx: commands.Context):
    vc: wavelink.Player = ctx.voice_client
    await ctx.send(REC)

@client.command()
async def volume(ctx: commands.Context, value: int):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send('You need to be in a voice channel to use this command!')
        return
    vc: wavelink.Player = ctx.voice_client
    if not vc:
        vc = await ctx.author.voice.channel.connect()
    volume = max(min(value, 100), 1)  # clamp the input volume to 1-100 range; original is 0 - 1000 range
    await vc.set_volume(volume)
    
@client.command()
async def help(ctx: commands.Context):
    vc: wavelink.Player = ctx.voice_client
    await ctx.send(
        
    )

# Use only if we retain 0 - 1000 for finer control, code scales the volume proportionally
# @client.command()
# async def set_volume(ctx: commands.Context, value: int):
#     if not ctx.author.voice or not ctx.author.voice.channel:
#         await ctx.send('You need to be in a voice channel to use this command!')
#         return
#     vc: wavelink.Player = ctx.voice_client
#     if not vc:
#         vc = await ctx.author.voice.channel.connect()
#     volume = max(min(value, 1000), 0)  # scale down the input volume to 0-100 range
#     volume_scaled = int(volume / 10)  # scale the volume to 0-10 range for wavelink
#     await vc.set_volume(volume_scaled)

@client.command()
async def mute(ctx: commands.Context):
    vc: wavelink.Player = ctx.voice_client
    await vc.set_volume(0)

client.run(TOKEN)
