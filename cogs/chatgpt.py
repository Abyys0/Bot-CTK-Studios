import discord
from discord.ext import commands
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class ChatGPT(commands.Cog):
    """Integração com ChatGPT/OpenAI"""
    
    def __init__(self, bot):
        self.bot = bot
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-3.5-turbo"
    
    @commands.command(name='chat', help='Conversa com ChatGPT')
    async def chat(self, ctx, *, message: str):
        """Envia uma mensagem para o ChatGPT e retorna a resposta"""
        
        # Mostra que está digitando
        async with ctx.typing():
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": message
                        }
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                
                reply = response.choices[0].message.content
                
                # Se a resposta é muito longa, dividir em múltiplas mensagens
                if len(reply) > 2000:
                    for i in range(0, len(reply), 2000):
                        await ctx.send(reply[i:i+2000])
                else:
                    embed = discord.Embed(
                        title='🤖 ChatGPT',
                        description=reply,
                        color=discord.Color.green()
                    )
                    embed.set_footer(text=f'Pergunta de {ctx.author.name}')
                    await ctx.send(embed=embed)
            
            except Exception as e:
                embed = discord.Embed(
                    title='❌ Erro',
                    description=f'Erro ao conectar com ChatGPT: {str(e)}',
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
    
    @commands.command(name='ia', help='Alias para o comando chat')
    async def ia(self, ctx, *, message: str):
        """Alias para chat"""
        await self.chat(ctx, message=message)
    
    @commands.command(name='pergunta', help='Faz uma pergunta para a IA')
    async def pergunta(self, ctx, *, question: str):
        """Faz uma pergunta para ChatGPT"""
        await self.chat(ctx, message=question)
    
    @commands.command(name='translate', help='Traduz um texto')
    async def translate(self, ctx, lang: str, *, text: str):
        """Traduz um texto para outro idioma"""
        
        async with ctx.typing():
            try:
                prompt = f"Traduza o seguinte texto para {lang}:\n\n{text}"
                
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                
                translation = response.choices[0].message.content
                
                embed = discord.Embed(
                    title=f'🌐 Tradução para {lang}',
                    description=translation,
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
            
            except Exception as e:
                await ctx.send(f'❌ Erro na tradução: {str(e)}')
    
    @commands.command(name='resumo', help='Faz um resumo de um texto')
    async def resumo(self, ctx, *, text: str):
        """Faz um resumo de um texto"""
        
        async with ctx.typing():
            try:
                prompt = f"Faça um resumo conciso do seguinte texto:\n\n{text}"
                
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                
                summary = response.choices[0].message.content
                
                embed = discord.Embed(
                    title='📝 Resumo',
                    description=summary,
                    color=discord.Color.purple()
                )
                await ctx.send(embed=embed)
            
            except Exception as e:
                await ctx.send(f'❌ Erro ao fazer resumo: {str(e)}')
    
    @commands.command(name='criativo', help='Gera um texto criativo')
    async def criativo(self, ctx, *, prompt: str):
        """Gera um texto criativo baseado em um prompt"""
        
        async with ctx.typing():
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=800,
                    temperature=0.9  # Mais criativo
                )
                
                text = response.choices[0].message.content
                
                if len(text) > 2000:
                    for i in range(0, len(text), 2000):
                        await ctx.send(text[i:i+2000])
                else:
                    embed = discord.Embed(
                        title='✨ Criação IA',
                        description=text,
                        color=discord.Color.gold()
                    )
                    await ctx.send(embed=embed)
            
            except Exception as e:
                await ctx.send(f'❌ Erro na criação: {str(e)}')
    
    @commands.command(name='piada', help='Gera uma piada')
    async def piada(self, ctx):
        """Gera uma piada aleatória"""
        
        async with ctx.typing():
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": "Conte uma piada engraçada e divertida"}],
                    max_tokens=300,
                    temperature=0.8
                )
                
                joke = response.choices[0].message.content
                
                embed = discord.Embed(
                    title='😂 Piada da IA',
                    description=joke,
                    color=discord.Color.orange()
                )
                await ctx.send(embed=embed)
            
            except Exception as e:
                await ctx.send(f'❌ Erro ao gerar piada: {str(e)}')

async def setup(bot):
    """Carrega o cog"""
    await bot.add_cog(ChatGPT(bot))
