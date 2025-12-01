import discord
from discord.ext import commands
from discord import app_commands

class BasicCommands(commands.Cog):
    """Comandos básicos do bot"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='avatar', help='Mostra o avatar de um usuário')
    async def avatar(self, ctx, member: discord.Member = None):
        """Mostra o avatar de um usuário"""
        member = member or ctx.author
        embed = discord.Embed(
            title=f'Avatar de {member.name}',
            color=discord.Color.blue()
        )
        embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await ctx.send(embed=embed)
    
    @commands.command(name='userinfo', help='Mostra informações do usuário')
    async def userinfo(self, ctx, member: discord.Member = None):
        """Mostra informações sobre um usuário"""
        member = member or ctx.author
        embed = discord.Embed(
            title=f'Informações de {member.name}',
            color=discord.Color.green()
        )
        embed.add_field(name='ID', value=member.id, inline=False)
        embed.add_field(name='Conta criada em', value=member.created_at.strftime('%d/%m/%Y'), inline=True)
        embed.add_field(name='Entrou no servidor em', value=member.joined_at.strftime('%d/%m/%Y'), inline=True)
        embed.add_field(name='Cargo mais alto', value=member.top_role.mention, inline=False)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='serverinfo', help='Mostra informações do servidor')
    async def serverinfo(self, ctx):
        """Mostra informações sobre o servidor"""
        guild = ctx.guild
        embed = discord.Embed(
            title=f'Informações de {guild.name}',
            color=discord.Color.purple()
        )
        embed.add_field(name='ID', value=guild.id, inline=False)
        embed.add_field(name='Dono', value=guild.owner.mention, inline=True)
        embed.add_field(name='Membros', value=guild.member_count, inline=True)
        embed.add_field(name='Canais', value=len(guild.channels), inline=True)
        embed.add_field(name='Cargos', value=len(guild.roles), inline=True)
        embed.add_field(name='Criado em', value=guild.created_at.strftime('%d/%m/%Y'), inline=False)
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='clear', help='Limpa mensagens do chat')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):
        """Limpa um número específico de mensagens"""
        
        if amount < 1:
            await ctx.send('❌ A quantidade deve ser maior que 0!')
            return
        
        if amount > 100:
            await ctx.send('⚠️ Máximo de 100 mensagens por vez!')
            amount = 100
        
        # Deleta as mensagens
        deleted = await ctx.channel.purge(limit=amount + 1)
        
        embed = discord.Embed(
            title='🧹 Chat Limpo',
            description=f'{len(deleted) - 1} mensagens foram deletadas!',
            color=discord.Color.green()
        )
        embed.set_footer(text=f'Solicitado por {ctx.author.name}')
        
        msg = await ctx.send(embed=embed)
        
        # Deleta a mensagem de confirmação após 3 segundos
        import asyncio
        await asyncio.sleep(3)
        await msg.delete()

async def setup(bot):
    """Carrega o cog"""
    await bot.add_cog(BasicCommands(bot))
