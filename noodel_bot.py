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

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')
    bot.loop.create_task(Music(bot).audio_player_task())

bot.add_cog(reply.Reply(bot))
bot.add_cog(music.Music(bot))
bot.run(os.environ.get('KEY'))