import asyncio
import reply
import music
import os

import discord
import youtube_dl

from discord.ext import commands
from music import Music


bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='i am noodel bot')

music_bot = Music(bot)

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')
    task = music_bot.audio_player_task()
    await bot.loop.create_task(task)

bot.add_cog(reply.Reply(bot))
bot.add_cog(music_bot)
bot.run(os.environ.get('KEY'))
