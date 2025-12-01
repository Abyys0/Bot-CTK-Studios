import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Importa e inicia o sistema de keep_alive para Render
from keep_alive import keep_alive

# Inicia o webserver Flask para Render
from webserver import start_web

# Carrega as variáveis de ambiente
load_dotenv()

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Inicia o sistema de ping para não dormir no Render
keep_alive()

# Inicia o webserver Flask
start_web()

@bot.event
async def on_ready():
    """Evento disparado quando o bot está pronto"""
    print(f'{bot.user} está online!')
    print(f'Conectado como: {bot.user.id}')
    try:
        synced = await bot.tree.sync()
        print(f'Sincronizados {len(synced)} comandos de barra /')
    except Exception as e:
        print(f'Erro ao sincronizar comandos: {e}')

@bot.event
async def on_message(message):
    """Evento disparado quando uma mensagem é enviada"""
    # Ignora mensagens do próprio bot
    if message.author == bot.user:
        return
    
    # Processa APENAS comandos com prefixo
    if message.content.startswith('!'):
        await bot.process_commands(message)

@bot.command(name='ping', help='Responde com o latência do bot')
async def ping(ctx):
    """Comando ping - mostra a latência do bot"""
    latency = bot.latency * 1000
    await ctx.send(f'🏓 Pong! Latência: {latency:.0f}ms')

@bot.command(name='hello', help='Sauda você')
async def hello(ctx):
    """Comando hello - sauda o usuário"""
    await ctx.send(f'Olá {ctx.author.mention}! 👋')

@bot.command(name='info', help='Mostra informações do bot')
async def info(ctx):
    """Comando info - mostra informações sobre o bot"""
    embed = discord.Embed(
        title='Informações do Bot',
        description='Bot Discord GGMAX',
        color=discord.Color.blue()
    )
    embed.add_field(name='Nome', value=bot.user.name, inline=True)
    embed.add_field(name='ID', value=bot.user.id, inline=True)
    embed.add_field(name='Versão', value='1.0.0', inline=True)
    embed.add_field(name='Servidores', value=len(bot.guilds), inline=True)
    
    await ctx.send(embed=embed)

# Carrega comandos dos cogs (extensões)
async def load_cogs():
    """Carrega todos os cogs da pasta cogs"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Carregado: {filename}')

async def main():
    """Função principal - carrega cogs e inicia o bot"""
    async with bot:
        await load_cogs()
        # Substitua com seu token do arquivo .env
        token = os.getenv('DISCORD_TOKEN')
        if not token:
            print('❌ Erro: Token do Discord não encontrado no arquivo .env')
            return
        await bot.start(token)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
