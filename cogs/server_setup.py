import discord
from discord.ext import commands
import asyncio

class ServerSetup(commands.Cog):
    """Configuração e Estrutura do Servidor"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='estruturarservidor')
    @commands.has_permissions(administrator=True)
    async def setup_server(self, ctx):
        """Cria a estrutura completa do servidor"""
        
        guild = ctx.guild
        
        # Definir a estrutura
        structure = {
            "📋 INFO": {
                "canals": ["📌-regras", "📌-anúncios", "📌-bem-vindas"]
            },
            "💼 VENDAS": {
                "canals": ["📢-promoções", "🛍️-catálogo", "💳-checkout", "📦-rastreamento"]
            },
            "🎫 SUPORTE": {
                "canals": ["🎯-tickets", "❓-faq", "💬-dúvidas"]
            },
            "👥 COMUNIDADE": {
                "canals": ["💬-geral", "📸-fotos", "🎮-off-topic"]
            }
        }
        
        await ctx.send("🔄 Criando estrutura do servidor...")
        
        # Criar categorias e canais
        for category_name, data in structure.items():
            try:
                # Criar categoria
                category = await guild.create_category(category_name)
                await asyncio.sleep(0.5)  # Pequeno delay para evitar rate limit
                
                # Criar canais dentro da categoria
                for channel_name in data["canals"]:
                    try:
                        await guild.create_text_channel(channel_name, category=category)
                        await asyncio.sleep(0.3)
                    except Exception as e:
                        print(f"❌ Erro ao criar canal {channel_name}: {e}")
                
                print(f"✅ Categoria criada: {category_name}")
            except Exception as e:
                print(f"❌ Erro ao criar {category_name}: {e}")
        
        embed = discord.Embed(
            title="✅ Estrutura Criada!",
            description="Servidor estruturado com sucesso!",
            color=discord.Color.green()
        )
        
        embed.add_field(name="📋 INFO", value="• 📌-regras\n• 📌-anúncios\n• 📌-bem-vindas", inline=False)
        embed.add_field(name="💼 VENDAS", value="• 📢-promoções\n• 🛍️-catálogo\n• 💳-checkout\n• 📦-rastreamento", inline=False)
        embed.add_field(name="🎫 SUPORTE", value="• 🎯-tickets\n• ❓-faq\n• 💬-dúvidas", inline=False)
        embed.add_field(name="👥 COMUNIDADE", value="• 💬-geral\n• 📸-fotos\n• 🎮-off-topic", inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    """Carrega o cog"""
    await bot.add_cog(ServerSetup(bot))
