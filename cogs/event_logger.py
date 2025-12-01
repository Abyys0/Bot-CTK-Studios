import discord
from discord.ext import commands
from datetime import datetime
import json
import os

class EventLogger(commands.Cog):
    """Sistema unificado de logs e painel ADM - Sem duplicatas"""
    
    def __init__(self, bot):
        self.bot = bot
        self.logs_file = 'server_logs.json'
        self.logs_channel_id = 1444849196849954966
        self.processed_events = set()  # Rastreia eventos já processados
        self.load_logs()
    
    def load_logs(self):
        """Carrega os logs do arquivo"""
        if os.path.exists(self.logs_file):
            with open(self.logs_file, 'r', encoding='utf-8') as f:
                self.logs = json.load(f)
        else:
            self.logs = {}
    
    def save_logs(self):
        """Salva os logs no arquivo"""
        with open(self.logs_file, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, indent=4, ensure_ascii=False)
    
    def add_log(self, guild_id: str, action: str, user_id: str, username: str, details: str):
        """Adiciona um log"""
        if guild_id not in self.logs:
            self.logs[guild_id] = []
        
        log_entry = {
            'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'action': action,
            'user_id': user_id,
            'username': username,
            'details': details
        }
        
        self.logs[guild_id].append(log_entry)
        self.save_logs()
    
    async def send_log_to_channel(self, guild, action: str, user: discord.User, details: str):
        """Envia um log para o canal de logs configurado"""
        try:
            channel = self.bot.get_channel(self.logs_channel_id)
            if channel:
                embed = discord.Embed(
                    title=f'📋 {action}',
                    description=details,
                    color=discord.Color.blue(),
                    timestamp=discord.utils.utcnow()
                )
                embed.set_author(name=f'{user.name}#{user.discriminator}', icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
                embed.add_field(name='Servidor', value=guild.name, inline=False)
                embed.add_field(name='Usuário ID', value=user.id, inline=False)
                
                await channel.send(embed=embed)
        except Exception as e:
            print(f'Erro ao enviar log: {e}')
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Quando alguém entra no servidor"""
        event_id = f"join_{member.id}_{datetime.now().timestamp()}"
        
        if event_id in self.processed_events:
            return
        
        self.processed_events.add(event_id)
        
        guild_id = str(member.guild.id)
        self.add_log(
            guild_id,
            'MEMBER_JOIN',
            str(member.id),
            member.name,
            f'{member.mention} entrou no servidor'
        )
        
        await self.send_log_to_channel(
            member.guild,
            '👋 Novo Membro',
            member,
            f'{member.mention} entrou no servidor'
        )
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Quando alguém sai do servidor"""
        event_id = f"remove_{member.id}_{datetime.now().timestamp()}"
        
        if event_id in self.processed_events:
            return
        
        self.processed_events.add(event_id)
        
        guild_id = str(member.guild.id)
        self.add_log(
            guild_id,
            'MEMBER_LEAVE',
            str(member.id),
            member.name,
            f'{member.name} saiu do servidor'
        )
        
        await self.send_log_to_channel(
            member.guild,
            '👋 Membro Saiu',
            member,
            f'{member.name} saiu do servidor'
        )
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Quando uma mensagem é deletada"""
        if message.author.bot:
            return
        
        event_id = f"msg_delete_{message.id}_{datetime.now().timestamp()}"
        
        if event_id in self.processed_events:
            return
        
        self.processed_events.add(event_id)
        
        guild_id = str(message.guild.id)
        self.add_log(
            guild_id,
            'MESSAGE_DELETE',
            str(message.author.id),
            message.author.name,
            f'Mensagem deletada em {message.channel.mention}: "{message.content[:100]}"'
        )
        
        await self.send_log_to_channel(
            message.guild,
            '🗑️ Mensagem Deletada',
            message.author,
            f'Canal: {message.channel.mention}\nMensagem: "{message.content[:100]}"'
        )
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Quando uma mensagem é editada"""
        if before.author.bot or before.content == after.content:
            return
        
        event_id = f"msg_edit_{before.id}_{datetime.now().timestamp()}"
        
        if event_id in self.processed_events:
            return
        
        self.processed_events.add(event_id)
        
        guild_id = str(before.guild.id)
        self.add_log(
            guild_id,
            'MESSAGE_EDIT',
            str(before.author.id),
            before.author.name,
            f'Mensagem editada em {before.channel.mention}\nAntes: "{before.content[:100]}"\nDepois: "{after.content[:100]}"'
        )
        
        await self.send_log_to_channel(
            before.guild,
            '✏️ Mensagem Editada',
            before.author,
            f'Canal: {before.channel.mention}\nAntes: "{before.content[:100]}"\nDepois: "{after.content[:100]}"'
        )
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Quando um membro é atualizado"""
        
        if before.roles != after.roles:
            guild_id = str(before.guild.id)
            new_roles = set(after.roles) - set(before.roles)
            removed_roles = set(before.roles) - set(after.roles)
            
            if new_roles:
                role = list(new_roles)[0]
                event_id = f"role_add_{after.id}_{role.id}_{datetime.now().timestamp()}"
                
                if event_id not in self.processed_events:
                    self.processed_events.add(event_id)
                    
                    self.add_log(
                        guild_id,
                        'ROLE_ADDED',
                        str(after.id),
                        after.name,
                        f'{after.mention} recebeu o cargo {role.mention}'
                    )
                    
                    await self.send_log_to_channel(
                        before.guild,
                        '⭐ Cargo Adicionado',
                        after,
                        f'{after.mention} recebeu o cargo {role.mention}'
                    )
            
            if removed_roles:
                role = list(removed_roles)[0]
                event_id = f"role_remove_{after.id}_{role.id}_{datetime.now().timestamp()}"
                
                if event_id not in self.processed_events:
                    self.processed_events.add(event_id)
                    
                    self.add_log(
                        guild_id,
                        'ROLE_REMOVED',
                        str(after.id),
                        after.name,
                        f'{after.mention} perdeu o cargo {role.mention}'
                    )
                    
                    await self.send_log_to_channel(
                        before.guild,
                        '❌ Cargo Removido',
                        after,
                        f'{after.mention} perdeu o cargo {role.mention}'
                    )
    
    @commands.command(name='setup_admin_panel', help='Cria o painel de administração')
    @commands.has_permissions(administrator=True)
    async def setup_admin_panel(self, ctx):
        """Cria um canal privado só para ADMs"""
        
        guild = ctx.guild
        
        # Verifica se já existe
        for channel in guild.channels:
            if channel.name == 'painel-adm':
                await ctx.send('⚠️ Painel ADM já existe!')
                return
        
        # Cria permissões: apenas ADMs
        admin_role = discord.utils.get(guild.roles, name='Moderator')
        if not admin_role:
            admin_role = discord.utils.get(guild.roles, permissions=discord.Permissions(administrator=True))
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
        }
        
        if admin_role:
            overwrites[admin_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
        
        # Cria o canal
        admin_channel = await guild.create_text_channel(
            name='painel-adm',
            overwrites=overwrites,
            topic='🔐 Painel de Administração - Apenas para ADMs'
        )
        
        # Envia mensagem inicial
        embed = discord.Embed(
            title='🔐 Painel de Administração',
            description='Bem-vindo ao painel de administração!\n\nAqui você pode monitorar todas as ações do servidor.',
            color=discord.Color.red()
        )
        embed.add_field(name='📊 Estatísticas', value='Monitore atividades do servidor', inline=False)
        embed.add_field(name='⚠️ Avisos', value='Receba notificações de eventos importantes', inline=False)
        embed.add_field(name='📝 Logs', value='Use `!logs` para ver todos os eventos', inline=False)
        
        await admin_channel.send(embed=embed)
        await ctx.send(f'✅ Painel ADM criado: {admin_channel.mention}')
    
    @commands.command(name='logs', help='Mostra todos os logs do servidor')
    @commands.has_permissions(administrator=True)
    async def show_logs(self, ctx, limit: int = 10):
        """Mostra os últimos logs"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.logs or not self.logs[guild_id]:
            await ctx.send('❌ Nenhum log encontrado!')
            return
        
        recent_logs = self.logs[guild_id][-limit:]
        
        embed = discord.Embed(
            title=f'📋 Últimos {len(recent_logs)} Logs',
            color=discord.Color.blue()
        )
        
        for log in recent_logs:
            embed.add_field(
                name=f"{log['action']} - {log['timestamp']}",
                value=f"👤 {log['username']}\n{log['details']}",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='logs_user', help='Mostra logs de um usuário específico')
    @commands.has_permissions(administrator=True)
    async def logs_user(self, ctx, user: discord.User):
        """Mostra logs de um usuário"""
        guild_id = str(ctx.guild.id)
        user_id = str(user.id)
        
        if guild_id not in self.logs:
            await ctx.send('❌ Nenhum log encontrado!')
            return
        
        user_logs = [log for log in self.logs[guild_id] if log['user_id'] == user_id]
        
        if not user_logs:
            await ctx.send(f'❌ Nenhum log encontrado para {user.mention}')
            return
        
        embed = discord.Embed(
            title=f'📋 Logs de {user.name}',
            description=f'Total: {len(user_logs)} ações',
            color=discord.Color.blue()
        )
        
        for log in user_logs[-10:]:
            embed.add_field(
                name=f"{log['action']} - {log['timestamp']}",
                value=log['details'],
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='export_logs', help='Exporta todos os logs para um arquivo')
    @commands.has_permissions(administrator=True)
    async def export_logs(self, ctx):
        """Exporta os logs"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.logs:
            await ctx.send('❌ Nenhum log para exportar!')
            return
        
        filename = f'logs_{ctx.guild.name}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f'=== LOGS DO SERVIDOR {ctx.guild.name} ===\n\n')
            
            for log in self.logs[guild_id]:
                f.write(f"[{log['timestamp']}] {log['action']}\n")
                f.write(f"Usuário: {log['username']} (ID: {log['user_id']})\n")
                f.write(f"Detalhes: {log['details']}\n")
                f.write('-' * 80 + '\n')
        
        with open(filename, 'rb') as f:
            await ctx.send(file=discord.File(f, filename))
        
        os.remove(filename)

async def setup(bot):
    """Carrega o cog"""
    await bot.add_cog(EventLogger(bot))
