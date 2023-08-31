import asyncio

from discord.enums import ActivityType
import reply
import music
import os

import discord
import youtube_dl

from discord.ext import commands
from music import Music

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='i am noodel bot',
                   intents=intents)

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')
    await bot.change_presence( activity = discord.Activity(type = ActivityType.listening, name = "!commands"))
    
    await bot.add_cog(reply.Reply(bot))
    songs = asyncio.Queue()
    music_bot = Music(bot, songs)
    task = music_bot.audio_player_task()
    await bot.add_cog(music_bot)
    await bot.loop.create_task(task)

bot.run(os.environ.get('KEY'))
