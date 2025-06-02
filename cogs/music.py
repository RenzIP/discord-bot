import discord
from discord.ext import commands
import youtube_dl
import asyncio

ytdl_format_options = {
    'format': 'bestaudio/best',
    'quiet': True,
    'extractaudio': True,
    'audioformat': 'mp3',
    'noplaylist': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_looping = False
        self.current_source = None

    @commands.command(name='play', help='Play a song from YouTube')
    async def play(self, ctx, *, url):
        if not ctx.voice_client:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                return await ctx.send("You are not connected to a voice channel.")

        vc = ctx.voice_client

        async def after_playing(error):
            if error:
                print(f'Error in playback: {error}')
            if self.is_looping:
                # play again the same song
                source = await YTDLSource.from_url(self.current_source.url, loop=self.bot.loop, stream=True)
                vc.play(source, after=after_playing)
                self.current_source = source
            else:
                await vc.disconnect()

        source = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        self.current_source = source
        vc.play(source, after=after_playing)
        await ctx.send(f'Now playing: {source.title}')

    @commands.command(name='stop', help='Stop the music and clear the queue')
    async def stop(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_playing():
            return await ctx.send("No audio is playing.")
        vc.stop()
        await ctx.send("Music stopped.")

    @commands.command(name='leave', help='Make the bot leave the voice channel')
    async def leave(self, ctx):
        vc = ctx.voice_client
        if not vc:
            return await ctx.send("I'm not connected to a voice channel.")
        await vc.disconnect()
        await ctx.send("Disconnected from the voice channel.")

    @commands.command(name='loop', help='Toggle looping the current song')
    async def loop(self, ctx):
        self.is_looping = not self.is_looping
        status = "enabled" if self.is_looping else "disabled"
        await ctx.send(f"Looping has been {status}.")

async def setup(bot):
    await bot.add_cog(Music(bot))
