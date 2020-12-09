import asyncio

import discord
import youtube_dl

from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes    
}

ffmpeg_options = {
    #before options fixes disconnect errors
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.songs = asyncio.Queue()
        self.is_playing = False
        # mutex for if current song is playing
        # clear if ready to play, set when processing next song
        self.play_next_song = asyncio.Event()
        # current url of song, synced with mutxed
        self.current_song = None

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            ctx, current = await self.songs.get()
            #play process
            try:
                self.current_song = current
                self.is_playing = True    
                ctx.voice_client.play(current, after=self.after_playing_song)
                await ctx.send('Now playing: "{}" ({}m:{}s)'.format(current.title, (int(current.duration//60)), int(current.duration%60)))
                await self.play_next_song.wait()

            except youtube_dl.utils.DownloadError as e:    
                await ctx.send('An error occurred while processing this request: {}'.format(str(e)))

    #next song process
    def after_playing_song(self, error):
        if error:
            print("error during song")
            return
        self.play_next_song.set()
        self.is_playing = False
        self.current_song = None

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports) or adds to queue"""

        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")

        current = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)

        if self.is_playing:
            await ctx.send( ('Added {} to the queue! ({}m:{}s)').format(current.title), int(current.duration//60), int(current.duration%60) )
        await self.songs.put((ctx, current))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def pause(self, ctx):
        """Pauses current item"""    
        if self.is_playing:
            ctx.voice_client.pause()
            return await ctx.send('Paused!')
        else:
            return await ctx.send('Nothing is Playing!')

    @commands.command()
    async def resume(self, ctx):
        """Resumes currently paused item"""
        if ctx.voice_client.is_paused and self.is_playing == True:
            ctx.voice_client.resume()
            return await ctx.send('Resumed!')
        else:
            return await ctx.send('Nothing is paused')

    @commands.command()
    async def skip(self, ctx):
        """Skips the current item playing"""
        if self.is_playing:
            ctx.voice_client.stop()
            return await ctx.send('Skipped!')
        else:
            return await ctx.send('Nothing is playing!')

    @commands.command()
    async def queue(self, ctx):
        """Returns # and name of items in the queue"""
        if self.songs.qsize() == 0:
            return await ctx.send('Queue is empty!')

        #probably a better way to do this
        queue = []
        ret_to_songs = []
        while not self.songs.empty():       
            ctx, indiv = await self.songs.get()
            queue.append(indiv)
            ret_to_songs.append( (ctx, indiv) )
        while ret_to_songs:
            await self.songs.put( (ret_to_songs.pop(0)) )

        await ctx.send('Queue:')
        for i in queue:
            await ctx.send( '{}. "{}" ({}m:{}s)'.format(queue.index(i) + 1, i.title, int(i.duration//60),  int(i.duration%60) ) )

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        await ctx.voice_client.disconnect()
        return await ctx.send('watch liz and the blue bird')