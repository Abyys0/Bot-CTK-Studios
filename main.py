import os  
from dotenv import load_dotenv  
import discord  
from discord.ext import commands  
  
# Sistema de keep alive  
from keep_alive import keep_alive  
from webserver import start_web  
  
load_dotenv()  
  
# Intents sem voice  
intents = discord.Intents.default()  
intents.message_content = True  
intents.members = True  
intents.voice_states = False  
  
bot = commands.Bot(command_prefix='!', intents=intents)  
  
keep_alive()  
start_web() 
  
@bot.event  
async def on_ready():  
    print(f'{bot.user} online!')  
  
@bot.command()  
async def ping(ctx):  
    await ctx.send('Pong!')  
  
async def load_cogs():  
    for filename in os.listdir('./cogs'):  
        if filename.endswith('.py') and filename != '__init__.py':  
            try:  
                await bot.load_extension(f'cogs.{filename[:-3]}')  
            except:  
                pass  
  
async def main():  
    async with bot:  
        await load_cogs()  
        await bot.start(os.getenv('DISCORD_TOKEN'))  
  
if __name__ == '__main__':  
    import asyncio  
    asyncio.run(main()) 
