import nextcord  
from nextcord.ext import commands  
  
class BasicCommands(commands.Cog):  
    def __init__(self, bot):  
        self.bot = bot  
  
    @commands.command(name='hello')  
    async def hello(self, ctx):  
        await ctx.send(f'Olá {ctx.author.mention}!')  
  
def setup(bot):  
    bot.add_cog(BasicCommands(bot)) 
