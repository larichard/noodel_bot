import asyncio

import discord
from discord.ext import commands

description = '''
            An example bot to showcase the discord.ext.commands extension module.
            There are a number of utility commands being showcased here.
            '''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

class Reply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
  
    @bot.command()
    async def hello(self, ctx):
        await ctx.send('Hello!')

    @bot.command(aliases=["grass"])
    async def w(self, ctx):
        await ctx.send('草')

    @bot.command()
    async def gay(self, ctx):
        await ctx.send('stream taemin criminal')

    @bot.command()
    async def marry_me (self, ctx):
        await ctx.send(':flushed:')

    @bot.command()
    async def commands (self, ctx):
        await ctx.send('Music:\n'
                       '!join (channel name) \n' 
                       '!play (url or name) \n'
                       '!volume (int) \n'
                       '!pause\n'
                       '!resume\n'
                       '!skip\n'
                       '!queue\n'
                       '!stop\n'
                       '!np\n'
                       '!clear\n\n'
                       'Other:\n'
                       '!hello\n'
                       '!gay\n'
                       '!marry_me\n'
                       '!w')
