import os  
from dotenv import load_dotenv  
import nextcord  
from nextcord.ext import commands  
  
from keep_alive import keep_alive  
from webserver import start_web  
  
load_dotenv()  
  
intents = nextcord.Intents.default()  
intents.message_content = True  
  
bot = commands.Bot(command_prefix='!', intents=intents)  
  
keep_alive()  
start_web()  
  
@bot.event  
async def on_ready():  
    print(f'{bot.user} online!')  
    for filename in os.listdir('./cogs'):  
        if filename.endswith('.py'):  
            try:  
                bot.load_extension(f'cogs.{filename[:-3]}')  
            except:  
                pass  
  
@bot.command()  
async def ping(ctx):  
    await ctx.send('Pong!')  
  
if __name__ == '__main__':  
    bot.run(os.getenv('DISCORD_TOKEN')) 
