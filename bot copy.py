import discord
from discord.ext import commands
import wavelink
from wavelink.ext import spotify
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
        if ctx.author.voice is None:
            return await ctx.send("Not in voice channel")
        vc: wavelink.Player = ctx.voice_client or await ctx.author.voice.channel.connect(cls=wavelink.Player)
        # vc.auto_queue = True
        vc.autoplay = True
        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
        else:
            await vc.queue.put_wait(search)
            await ctx.send(f'Added `{search.title}` to the queue...')

    @commands.command()
    async def skip(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        if not vc.queue.is_empty:
            await vc.stop()
            await ctx.send(f"Now playing: {vc.queue[0]}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    await bot.add_cog(Music(bot))

bot.run(TOKEN)
