import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class TicketSystem(commands.Cog):
    """Sistema de Tickets para suporte"""
    
    def __init__(self, bot):
        self.bot = bot
        self.tickets_file = 'tickets.json'
        self.load_tickets()
    
    def load_tickets(self):
        """Carrega os tickets do arquivo"""
        if os.path.exists(self.tickets_file):
            with open(self.tickets_file, 'r') as f:
                self.tickets = json.load(f)
        else:
            self.tickets = {}
    
    def save_tickets(self):
        """Salva os tickets no arquivo"""
        with open(self.tickets_file, 'w') as f:
            json.dump(self.tickets, f, indent=4)
    
    @commands.command(name='setup_tickets', help='Configura o painel de tickets')
    @commands.has_permissions(administrator=True)
    async def setup_tickets(self, ctx):
        """Configura o sistema de tickets no servidor"""
        
        # Cria um embed bonito
        embed = discord.Embed(
            title='🎫 Sistema de Tickets',
            description='Clique no botão abaixo para abrir um ticket e falar com a staff!',
            color=discord.Color.blue()
        )
        embed.add_field(
            name='Como funciona?',
            value='1. Clique em "Abrir Ticket"\n2. Explique seu problema\n3. Aguarde a resposta da staff',
            inline=False
        )
        
        # Envia a mensagem com o botão
        view = TicketButtonView(self.bot)
        await ctx.send(embed=embed, view=view)
        await ctx.send('✅ Painel de tickets configurado!')
    
    @commands.command(name='close_ticket', help='Fecha o ticket atual')
    async def close_ticket(self, ctx):
        """Fecha um ticket"""
        channel_id = str(ctx.channel.id)
        
        if channel_id not in self.tickets:
            await ctx.send('❌ Este não é um canal de ticket!')
            return
        
        # Cria um embed de confirmação
        embed = discord.Embed(
            title='Fechar Ticket?',
            description='Clique em "Confirmar" para fechar este ticket permanentemente.',
            color=discord.Color.red()
        )
        
        view = CloseTicketView(self, ctx.channel, channel_id)
        await ctx.send(embed=embed, view=view)
    
    @commands.command(name='add_user', help='Adiciona um usuário ao ticket')
    async def add_user(self, ctx, user: discord.User):
        """Adiciona um usuário ao ticket"""
        channel_id = str(ctx.channel.id)
        
        if channel_id not in self.tickets:
            await ctx.send('❌ Este não é um canal de ticket!')
            return
        
        # Adiciona permissão ao usuário
        await ctx.channel.set_permissions(user, view_channel=True, send_messages=True)
        embed = discord.Embed(
            title='✅ Usuário Adicionado',
            description=f'{user.mention} foi adicionado ao ticket.',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='remove_user', help='Remove um usuário do ticket')
    async def remove_user(self, ctx, user: discord.User):
        """Remove um usuário do ticket"""
        channel_id = str(ctx.channel.id)
        
        if channel_id not in self.tickets:
            await ctx.send('❌ Este não é um canal de ticket!')
            return
        
        # Remove permissão do usuário
        await ctx.channel.set_permissions(user, overwrite=None)
        embed = discord.Embed(
            title='❌ Usuário Removido',
            description=f'{user.mention} foi removido do ticket.',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

class TicketButtonView(discord.ui.View):
    """Botão para abrir tickets"""
    
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    
    @discord.ui.button(label='Abrir Ticket', style=discord.ButtonStyle.green, emoji='🎫')
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Abre um novo ticket"""
        user = interaction.user
        guild = interaction.guild
        
        # Verifica se o usuário já tem um ticket aberto
        # (Você pode adicionar essa lógica depois)
        
        # Cria um canal privado
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
        }
        
        ticket_channel = await guild.create_text_channel(
            name=f'ticket-{user.name}',
            overwrites=overwrites,
            category=None  # Você pode especificar uma categoria aqui
        )
        
        # Salva o ticket
        ticket_system = interaction.client.get_cog('TicketSystem')
        ticket_system.tickets[str(ticket_channel.id)] = {
            'user_id': user.id,
            'created_at': str(discord.utils.utcnow())
        }
        ticket_system.save_tickets()
        
        # Envia uma mensagem no ticket
        embed = discord.Embed(
            title='🎫 Ticket Aberto',
            description=f'Olá {user.mention}! Bem-vindo ao seu ticket de suporte.\n\n'
                       f'Descreva seu problema aqui e a staff responderá em breve!',
            color=discord.Color.green()
        )
        embed.add_field(name='ID do Ticket', value=ticket_channel.id, inline=False)
        
        view = TicketMenuView()
        msg = await ticket_channel.send(f'{user.mention}', embed=embed, view=view)
        
        # Responde ao usuário
        await interaction.response.send_message(
            f'✅ Ticket criado: {ticket_channel.mention}',
            ephemeral=True
        )

class TicketMenuView(discord.ui.View):
    """Menu de opções do ticket"""
    
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Fechar', style=discord.ButtonStyle.red, emoji='❌')
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para fechar o ticket"""
        embed = discord.Embed(
            title='❌ Fechar Ticket?',
            description='Tem certeza que deseja fechar este ticket?',
            color=discord.Color.red()
        )
        
        view = CloseConfirmView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class CloseTicketView(discord.ui.View):
    """Confirmação para fechar ticket"""
    
    def __init__(self, ticket_system, channel, channel_id):
        super().__init__(timeout=None)
        self.ticket_system = ticket_system
        self.channel = channel
        self.channel_id = channel_id
    
    @discord.ui.button(label='Confirmar', style=discord.ButtonStyle.red)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Confirma o fechamento"""
        # Remove o ticket do arquivo
        if self.channel_id in self.ticket_system.tickets:
            del self.ticket_system.tickets[self.channel_id]
            self.ticket_system.save_tickets()
        
        embed = discord.Embed(
            title='✅ Ticket Fechado',
            description='O ticket será deletado em 5 segundos...',
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # Deleta o canal após 5 segundos
        await asyncio.sleep(5)
        await self.channel.delete(reason='Ticket fechado')
    
    @discord.ui.button(label='Cancelar', style=discord.ButtonStyle.gray)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Cancela o fechamento"""
        await interaction.response.send_message('❌ Fechamento cancelado!', ephemeral=True)

class CloseConfirmView(discord.ui.View):
    """Confirmação rápida do fechamento"""
    
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Sim, fechar', style=discord.ButtonStyle.red)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Fecha o ticket"""
        channel = interaction.channel
        
        embed = discord.Embed(
            title='✅ Ticket Fechado',
            description='O ticket será deletado em 5 segundos...',
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
        
        # Deleta o canal
        import asyncio
        await asyncio.sleep(5)
        await channel.delete(reason='Ticket fechado pelo usuário')
    
    @discord.ui.button(label='Não', style=discord.ButtonStyle.gray)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Cancela"""
        await interaction.response.send_message('❌ Cancelado!', ephemeral=True)

import asyncio

async def setup(bot):
    """Carrega o cog"""
    await bot.add_cog(TicketSystem(bot))
