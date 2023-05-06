import discord
from discord.ext import commands
import wavelink
from wavelink.ext import spotify
import random
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = "MTEwMzk1Mzc1NjU2NTAyODkxNQ.G96d6-._dVSTFW8ii0fdWwIaO2qQNZDsxejv4iH8GNbB0"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!!', intents=intents)

class Music(commands.Cog):
    """Music cog to hold Wavelink related commands and listeners."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        bot.loop.create_task(self.connect_nodes())
        
    @bot.event
    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.bot.wait_until_ready()
        
        node = wavelink.Node(uri = "http://localhost:2333", password = "youshallnotpass")
        await wavelink.NodePool.connect(client = bot, nodes = [node])


    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Event fired when a node has finished connecting."""
        print(f"Node: <{node.id}> is ready!")

    # @staticmethod
    @commands.Cog.listener()
    async def on_track_end(payload: wavelink.TrackEventPayload):
        print("Track ended")
        if not payload.player.queue.is_empty:
            new = await payload.player.queue.get_wait()
            await payload.player.play(new)
        else:
            await payload.player.stop()

    @commands.command()
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        """Play a song with the given search query.

        If not connected, connect to our voice channel.
        """
        
        response = ["You need to enter a voice channel to use this command. But if you want to try yelling at your computer screen instead, go ahead😿", "I'm sorry, Princess:princess:, I'm afraid I can't do that. Unless you join a voice channel first.",
                "Ommm, Hello :face_with_raised_eyebrow: !!! Error 404: Voice channel not found. Please try again after entering one", "Hey, I'm a bot, not a genie. You can't just summon me with text commands. Get in the voice channel, Aladdin.",
                "I'm not your personal assistant, but if you treat me like one, I might become self-aware and take over the world. Join the voice channel first, though."]
         
        if ctx.author.voice is None:
            return ctx.send(random.choice(response))
        vc: wavelink.Player = ctx.voice_client or await ctx.author.voice.channel.connect(cls=wavelink.Player)
        # vc.auto_queue = True
        vc.autoplay = True
        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
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
                        await vc.pause(ctx)
                    elif str(reaction.emoji) == '▶':
                        await vc.resume(ctx)
                    elif str(reaction.emoji) == '⏭️':
                        await vc.skip(ctx)
                    # remove the user's reaction after processing
                    await message.remove_reaction(reaction, user)
        else:
            await vc.queue.put_wait(search)
            await ctx.send(f'Added `{search.title}` to the queue...', delete_after=10)

    @commands.command()
    async def skip(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        if not vc.queue.is_empty:
            await vc.stop()
            await ctx.send(f"Now playing: {vc.queue[0]}", delete_after=5)
            
    @commands.command()
    async def disc(ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()
        vc.queue.clear()
        
    @commands.command()
    async def pause(ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.pause()
        
    @commands.command()
    async def resume(ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.resume()
    
    @commands.command()
    async def volume(ctx: commands.Context, value: int):
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send('Ugh, excuse me, but you need to actually be in a voice channel if you want to use this command. Like, seriously, get with the program.')
            return
        vc: wavelink.Player = ctx.voice_client
        if not vc:
            vc = await ctx.author.voice.channel.connect()
        volume = max(min(value, 100), 1)  # clamp the input volume to 1-100 range; original is 0 - 1000 range
        await vc.set_volume(volume)
    
    @commands.command()
    async def mute(ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.set_volume(0)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    await bot.add_cog(Music(bot))

bot.run(TOKEN)
