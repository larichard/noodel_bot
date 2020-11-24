import asyncio

from discord.ext import commands

class Reply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
  
    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello!')

    @commands.command()
    async def gay(self, ctx):
        await ctx.send('stream taemin criminal')

    @commands.command()
    async def marry_me (self, ctx):
        await ctx.send(':flushed:')
