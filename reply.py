import asyncio

from discord.ext import commands

class Reply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
  
    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello!')

    @commands.command(aliases=["grass"])
    async def w(self, ctx):
        await ctx.send('草')

    @commands.command()
    async def gay(self, ctx):
        await ctx.send('stream taemin criminal')

    @commands.command()
    async def marry_me (self, ctx):
        await ctx.send(':flushed:')

    @commands.command()
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
