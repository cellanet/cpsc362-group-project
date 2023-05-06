import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import wavelink
import random


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
    response = ["You need to enter a voice channel to use this command. But if you want to try yelling at your computer screen instead, go ahead😿", "I'm sorry, Princess:princess:, I'm afraid I can't do that. Unless you join a voice channel first.",
                "Ommm, Hello :face_with_raised_eyebrow: !!! Error 404: Voice channel not found. Please try again after entering one", "Hey, I'm a bot, not a genie. You can't just summon me with text commands. Get in the voice channel, Aladdin.",
                "I'm not your personal assistant, but if you treat me like one, I might become self-aware and take over the world. Join the voice channel first, though."]
    print(track)
    if ctx.voice_client:
        vc: wavelink.Player = ctx.voice_client
        print("Using existing voice client")
    elif ctx.author.voice:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls = wavelink.Player)
        print("Connecting to voice channel")
    else:
        await ctx.send(random.choice(response))
        return
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
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
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
async def volume(ctx: commands.Context, value: int):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send('line 88')
        return
    vc: wavelink.Player = ctx.voice_client
    if not vc:
        vc = await ctx.author.voice.channel.connect()
    volume = max(min(value, 100), 1)  # clamp the input volume to 1-100 range; original is 0 - 1000 range
    await vc.set_volume(volume)

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