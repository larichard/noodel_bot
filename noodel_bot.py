import asyncio
import reply
import music

import discord
import youtube_dl

from discord.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='i am noodel bot')

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

bot.add_cog(reply.Reply(bot))
bot.add_cog(music.Music(bot))
bot.run('NzQ2OTI1ODEyNzM3MTE0MTMz.X0Ha3g.1hPVklPkqt7520IP0y6E13I4cF4')
