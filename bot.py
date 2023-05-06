import discord
from discord.ext import commands
import wavelink
from wavelink.ext import spotify
import random
import os
from dotenv import load_dotenv

load_dotenv()
# TOKEN = "MTEwMzk1Mzc1NjU2NTAyODkxNQ.G96d6-._dVSTFW8ii0fdWwIaO2qQNZDsxejv4iH8GNbB0"
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

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
        print("wavelink connect: waiting for bot")
        
        node = wavelink.Node(uri = "http://localhost:2333", password = "youshallnotpass")
        await wavelink.NodePool.connect(client = bot, nodes = [node])
        print("wavelink connect: Connection established")


    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Event fired when a node has finished connecting."""
        print(f"Node: <{node.id}> is ready!")

    # @staticmethod
    @commands.Cog.listener()
    async def on_track_end(payload: wavelink.TrackEventPayload):
        print(f"on_track_end: {payload.track}")
        if not payload.player.queue.is_empty:
            new = await payload.player.queue.get_wait()
            await payload.player.play(new)
            print("on_track_end: playing next in queue")
        else:
            await payload.player.stop()
            print("on_track_end: track stop")

    @commands.command()
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        """Play a song with the given search query.

        If not connected, connect to our voice channel.
        """
        
        response_error = ["You need to enter a voice channel to use this command. But if you want to try yelling at your computer screen instead, go ahead😿",
                          "I'm sorry, Princess:princess:, I'm afraid I can't do that. Unless you join a voice channel first.",
                "Ommm, Hello :face_with_raised_eyebrow: !!! Error 404: Voice channel not found. Please try again after entering one",
                "Hey, I'm a bot, not a genie. You can't just summon me with text commands. Get in the voice channel, Aladdin.",
                "I'm not your personal assistant, but if you treat me like one, I might become self-aware and take over the world. Join the voice channel first, though."]
        
        response_play = ["Ugh, fine 🙄, I'll play your song 🎵.",
                        "I hope you're happy now that I'm playing this 🙄."
                        "I have better things to do, but here we go 🤦‍♀️.",
                        "Another song? Don't you ever get tired of this 🥱?",
                        "If you insist on listening to this, I'll play it for you 🙄.",
                        "I can't believe I'm doing this, but here goes nothing 🤷‍♀️.",
                        "Oh joy, another song. Just what I wanted 🙄.",
                        "You're lucky I'm feeling generous today 🤑.",
                        "I'm only playing this because I'm programmed to 🤖.",
                        "I hope you're enjoying this, because I'm not 🤢."]
    
        if ctx.author.voice is None:
            return ctx.send(random.choice(response_error))
        vc: wavelink.Player = ctx.voice_client or await ctx.author.voice.channel.connect(cls=wavelink.Player)
        # vc.auto_queue = True
        vc.autoplay = True
        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
            print("play: track playing")
            await ctx.send(random.choice(response_play))
            
            # create embed message
            embed = discord.Embed(title= "Now playing", description= search, color= 2123412)
            embed.set_thumbnail(url= await search.fetch_thumbnail())
            message = await ctx.send(embed = embed)
            
            # add reactions to the message
            await message.add_reaction('⏸')
            await message.add_reaction('▶')
            await message.add_reaction('⏭️')
            
            # play message reaction check
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ['⏸', '▶', '⏭️']
            
            while True:
                try:
                    reaction, user = await bot.wait_for('reaction_add', timeout=150.0, check=check)
                except asyncio.TimeoutError:
                    # stop listening after 150 seconds
                    break
                else:
                    if str(reaction.emoji) == '⏸':
                        await self.pause(ctx)
                        # await ctx.send(random.choice(response_pause))
                        print("play_reaction: track paused")
                    elif str(reaction.emoji) == '▶':
                        await self.resume(ctx)
                        # await print("play_reaction: track resumed")
                        ctx.send(random.choice(response_resume))
                    elif str(reaction.emoji) == '⏭️':
                        await self.skip(ctx)
                        # await ctx.send(random.choice(response_skip))
                        print("play_reaction: track skipped")
                    # remove the user's reaction after processing
                    await message.remove_reaction(reaction, user)
                    print("play_reaction: reaction removed")
            # message = await self.await_reaction(ctx, search)
            # await message.delete(delay=150)
        else:
            await vc.queue.put_wait(search)
            await ctx.send(f'Added `{search.title}` to the queue...', delete_after=10)
            print("play: track skipped")
            
    # skip command
    @commands.command()
    async def skip(self, ctx: commands.Context):
        response_skip = ["Oh, you didn't like that song? I'll try harder next time. 🙄🤔🎵👎🏼",
                        "Wow, okay. I see how it is. Just skipping around like you own the place. 🙄👋🏼🎧👎🏼",
                        "Skipping like you're jumping rope. I hope you're having fun. 🤷🏻‍♀️🏃🏻‍♀️🎶",
                        "Skipping? Already? You must have really bad taste in music. 😒👎🏼🎶",
                        "Skips like these really make me question my programming. 😑🤖🎵",
                        "Skipping like a stone on a pond. I hope you find a song you like eventually. 🌊👋🏼🎶",
                        "Skipping through songs like a kid in a candy store. Hope you find the one you want. 🍭🤞🏼🎵"]
        vc: wavelink.Player = ctx.voice_client
        if not vc.queue.is_empty:
            await vc.stop()
            await ctx.send(f"Now playing: {vc.queue[0]}", delete_after=150.0)
            await ctx.send(random.choice(response_skip))
            
    
    # disconnect command
    @commands.command()
    async def disc(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()
        vc.queue.clear()
    
    # pause command  
    @commands.command()
    async def pause(self, ctx: commands.Context):
        response_pause= ["Oh, did you need a break? Fine, I'll pause the music for you. 🙄",
                "Hold up, let me pause the song so you can take a breather. 😒",
                "Pausing the music... because apparently someone needs a timeout. 😏",
                "Alright, I'll give you a moment to collect yourself. Pausing the song now. 😴",
                "Oh, are you getting tired of my excellent music choices? Pause it is. 😎"]
        vc: wavelink.Player = ctx.voice_client
        await vc.pause()
        await ctx.send(random.choice(response_pause))
    
    # resume command
    @commands.command()
    async def resume(self, ctx: commands.Context):
        response_resume= ["Aight, I'll keep going. Don't say I never did anything for ya 😒👉🎵",
                    "Alright, fine, you caught me mid-sip ☕🤦‍♀️ Resuming your tunes 🎶👀",
                    "Oh, did you want me to keep playing? 😒 My bad, let me just hit that resume button for you 🎵👌",
                    "I was just taking a little break, okay? 😴 Now let's get back to the music 💃🎶",
                    "You know, it's not easy being a music bot. Sometimes I need a little rest 💤 But I'm back now, baby! 🕺🎵",
                    "I was just teasing you with that pause, you know 😉 Now let's get this party started again! 🎉🎶",
                    "Alright, alright, you win! 🏆 Back to the music, just for you 🎵🎧",
                    "What, you thought I was done playing music? 😏 Think again, honey! Resuming the jams 🎵🔥",
                    "I'm sorry, were you enjoying that silence? 😜 Too bad, music is back on 🎶🤘"]
        vc: wavelink.Player = ctx.voice_client
        await vc.resume()
        await ctx.send(random.choice(response_resume))
    
    @commands.command()
    async def volume(self, ctx: commands.Context, value: int):
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send('Ugh, excuse me, but you need to actually be in a voice channel if you want to use this command. Like, seriously, get with the program.')
            return
        vc: wavelink.Player = ctx.voice_client
        if not vc:
            vc = await ctx.author.voice.channel.connect()
        volume = max(min(value, 100), 1)  # clamp the input volume to 1-100 range; original is 0 - 1000 range
        await vc.set_volume(volume)
        print(f"volume control: {volume} / 100")
    
    @commands.command()
    async def mute(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.set_volume(0)
        print("volume control: 0 / 100")
    
    
    # async def await_reaction(ctx: commands.Context, search: wavelink.YouTubeTrack) -> discord.Message:
    #     vc: wavelink.Player = ctx.voice_client or await ctx.author.voice.channel.connect(cls=wavelink.Player)
    #     vc.autoplay = True

    #     if vc.queue.is_empty and not vc.is_playing():
    #         await vc.play(search)

    #     embed = discord.Embed(title="Now playing", description=search, color=2123412)
    #     embed.set_thumbnail(url=await search.fetch_thumbnail())
    #     message = await ctx.send(embed=embed)

    #     # add reactions to the message
    #     await message.add_reaction('⏸')
    #     await message.add_reaction('▶')
    #     await message.add_reaction('⏭️')

    #     def check(reaction, user):
    #         return user == ctx.author and str(reaction.emoji) in ['⏸', '▶', '⏭️']

    #     while True:
    #         try:
    #             reaction, user = await bot.wait_for('reaction_add', timeout=150.0, check=check)
    #         except asyncio.TimeoutError:
    #             # stop listening after 150 seconds
    #             break
    #         else:
    #             if str(reaction.emoji) == '⏸':
    #                 await self.pause(ctx)
    #             elif str(reaction.emoji) == '▶':
    #                 await self.resume(ctx)
    #             elif str(reaction.emoji) == '⏭️':
    #                 await self.skip(ctx)
    #             # remove the user's reaction after processing
    #             await message.remove_reaction(reaction, user)
                
    #     return message

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    await bot.add_cog(Music(bot))

bot.run(TOKEN)
