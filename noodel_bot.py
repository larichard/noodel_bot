import asyncio

from discord.enums import ActivityType
from constants import SETTINGS_FILE
import reply
import music
import os
import json
import playlist

import discord
import youtube_dl

from discord.ext import commands
from music import Music

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description="i am noodel bot",
                   intents=intents)

settings = json.load(open(SETTINGS_FILE))

@bot.event
async def on_ready():
    print("Logged in as {0} ({0.id})".format(bot.user))
    print("------")
    await bot.change_presence( activity = discord.Activity(type = ActivityType.listening, name = "!commands"))
    for module in settings:
        print(f"{module} is {settings[module]}")
    
    if settings.get("enableReply"):
        await bot.add_cog(reply.Reply(bot))
    
    if settings.get("enablePlaylist") and settings.get("playlistId"):
        playlist_id = settings.get("playlistId")
        await bot.add_cog(playlist.Playlist(bot, playlist_id))

    if settings.get("enableMusic"):
        songs = asyncio.Queue()
        music_bot = Music(bot, songs)
        task = music_bot.audio_player_task()
        await bot.add_cog(music_bot)
        await bot.loop.create_task(task)
    
bot.run(os.environ.get("KEY"))
