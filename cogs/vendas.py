import discord
from discord.ext import commands
from discord import ui
import json
import os
from datetime import datetime

class Vendas(commands.Cog):
    """Sistema de Vendas com Painel de Produtos e Checkout"""
    
    def __init__(self, bot):
        self.bot = bot
        self.products_file = 'products.json'
        self.orders_file = 'orders.json'
        self.load_products()
        self.load_orders()
    
    def load_products(self):
        """Carrega produtos do JSON"""
        if os.path.exists(self.products_file):
            with open(self.products_file, 'r', encoding='utf-8') as f:
                self.products = json.load(f)
        else:
            self.products = {}
    
    def load_orders(self):
        """Carrega pedidos do JSON"""
        if os.path.exists(self.orders_file):
            with open(self.orders_file, 'r', encoding='utf-8') as f:
                self.orders = json.load(f)
        else:
            self.orders = {}
    
    def save_products(self):
        """Salva produtos no JSON"""
        with open(self.products_file, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, indent=4, ensure_ascii=False)
    
    def save_orders(self):
        """Salva pedidos no JSON"""
        with open(self.orders_file, 'w', encoding='utf-8') as f:
            json.dump(self.orders, f, indent=4, ensure_ascii=False)
    
    @commands.command(name='adicionarproduto')
    @commands.has_permissions(administrator=True)
    async def add_product(self, ctx, nome: str, preco: float, estoque: int, *, descricao: str = "Sem descrição"):
        """Adiciona um produto ao catálogo"""
        
        product_key = nome.lower()
        
        if product_key in self.products:
            await ctx.send(f'❌ Produto "{nome}" já existe!')
            return
        
        self.products[product_key] = {
            'nome': nome,
            'preco': preco,
            'estoque': estoque,
            'descricao': descricao,
            'vendas': 0,
            'criado_em': datetime.now().isoformat()
        }
        
        self.save_products()
        
        embed = discord.Embed(
            title='✅ Produto Adicionado',
            description=f'**{nome}** foi adicionado!',
            color=discord.Color.green()
        )
        embed.add_field(name='Preço', value=f'R$ {preco:.2f}', inline=True)
        embed.add_field(name='Estoque', value=f'{estoque} un', inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='painel')
    async def show_panel(self, ctx):
        """Mostra o painel de produtos"""
        
        if not self.products:
            await ctx.send('❌ Nenhum produto disponível!')
            return
        
        # Criar embeds para cada produto
        embeds = []
        
        for i, (key, product) in enumerate(self.products.items(), 1):
            status = '✅ Em estoque' if product['estoque'] > 0 else '❌ Fora de estoque'
            
            embed = discord.Embed(
                title=f"🛍️ {product['nome']}",
                description=product['descricao'][:100] + '...' if len(product['descricao']) > 100 else product['descricao'],
                color=discord.Color.blurple()
            )
            
            embed.add_field(name='💵 Preço', value=f"R$ {product['preco']:.2f}", inline=True)
            embed.add_field(name='📊 Estoque', value=f"{product['estoque']} un", inline=True)
            embed.add_field(name='Status', value=status, inline=True)
            embed.add_field(name='📈 Vendas', value=f"{product['vendas']} vendidas", inline=False)
            embed.set_footer(text=f'Produto {i} de {len(self.products)}')
            
            embeds.append(embed)
        
        # Enviar primeira página com botão
        view = PainelView(self.products, self)
        await ctx.send(embed=embeds[0], view=view)
    
    @commands.command(name='pedidos')
    @commands.has_permissions(administrator=True)
    async def show_orders(self, ctx):
        """Mostra painel de pedidos pendentes"""
        
        if not self.orders:
            await ctx.send('✅ Nenhum pedido pendente!')
            return
        
        embed = discord.Embed(
            title='📦 Pedidos Pendentes de Confirmação',
            color=discord.Color.orange()
        )
        
        pending_count = 0
        for order_id, order in self.orders.items():
            if order['status'] == 'pendente':
                pending_count += 1
                embed.add_field(
                    name=f"🎫 ID: {order_id}",
                    value=f"Produto: {order['produto']}\nCliente: {order['cliente']}\nValor: R$ {order['total']:.2f}\nData: {order['data']}",
                    inline=False
                )
        
        if pending_count == 0:
            embed.description = "✅ Todos os pedidos foram confirmados!"
        
        view = PedidosView(self.orders, self)
        await ctx.send(embed=embed, view=view)

class PainelView(ui.View):
    """View para o painel de produtos"""
    
    def __init__(self, products, cog):
        super().__init__(timeout=None)
        self.products = products
        self.cog = cog
        self.current_page = 0
        self.product_list = list(products.items())
    
    @ui.button(label='🛒 Comprar', style=discord.ButtonStyle.success)
    async def buy_button(self, interaction: discord.Interaction, button: ui.Button):
        """Abre modal de compra"""
        product_key, product = self.product_list[self.current_page]
        
        # Enviar modal
        modal = CheckoutModal(product_key, product, self.cog)
        await interaction.response.send_modal(modal)
    
    @ui.button(label='❌ Fechar', style=discord.ButtonStyle.danger)
    async def close_button(self, interaction: discord.Interaction, button: ui.Button):
        """Fecha o painel"""
        await interaction.response.defer()
        await interaction.message.delete()

class CheckoutModal(ui.Modal):
    """Modal para checkout de produtos"""
    
    def __init__(self, product_key, product, cog):
        super().__init__(title=f'Comprar: {product["nome"]}')
        self.product_key = product_key
        self.product = product
        self.cog = cog
        
        # Adicionar campos do formulário
        self.add_item(ui.TextInput(
            label='Nome Completo',
            placeholder='Seu nome aqui',
            required=True
        ))
        
        self.add_item(ui.TextInput(
            label='Email',
            placeholder='seu@email.com',
            required=True
        ))
        
        self.add_item(ui.TextInput(
            label='Quantidade',
            placeholder='1',
            required=True
        ))
    
    async def on_submit(self, interaction: discord.Interaction):
        """Processa o checkout"""
        
        nome = self.children[0].value
        email = self.children[1].value
        
        try:
            quantidade = int(self.children[2].value)
        except:
            await interaction.response.send_message('❌ Quantidade inválida!', ephemeral=True)
            return
        
        if quantidade > self.product['estoque']:
            await interaction.response.send_message(f'❌ Estoque insuficiente! Disponível: {self.product["estoque"]}', ephemeral=True)
            return
        
        total = self.product['preco'] * quantidade
        
        # Gerar ID do pedido
        order_id = f"PED_{interaction.user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Salvar pedido
        self.cog.orders[order_id] = {
            'usuario_id': interaction.user.id,
            'usuario': interaction.user.name,
            'produto': self.product['nome'],
            'cliente': nome,
            'email': email,
            'quantidade': quantidade,
            'total': total,
            'preco_unitario': self.product['preco'],
            'status': 'pendente',
            'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'comprovante': None
        }
        self.cog.save_orders()
        
        embed = discord.Embed(
            title='⏳ Pagamento Pendente',
            description='Seu pedido foi registrado! Agora siga os passos abaixo:',
            color=discord.Color.orange()
        )
        
        embed.add_field(name='🛍️ Produto', value=self.product['nome'], inline=False)
        embed.add_field(name='💵 Preço Unitário', value=f"R$ {self.product['preco']:.2f}", inline=True)
        embed.add_field(name='📦 Quantidade', value=f'{quantidade} un', inline=True)
        embed.add_field(name='💰 Total', value=f"R$ {total:.2f}", inline=True)
        embed.add_field(name='🎫 ID do Pedido', value=f"`{order_id}`", inline=False)
        
        embed.add_field(
            name='📋 Próximos Passos:',
            value=f"1. Aguarde o PIX no privado\n2. Faça o pagamento\n3. Envie o comprovante como resposta\n4. Admin confirma\n5. Você recebe o produto!",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # Enviar DM com PIX
        try:
            dm_embed = discord.Embed(
                title='💳 Dados para Pagamento',
                description='Escaneie o QR Code abaixo ou use a chave PIX',
                color=discord.Color.gold()
            )
            dm_embed.add_field(name='Valor', value=f"R$ {total:.2f}", inline=False)
            dm_embed.add_field(name='Chave PIX (Exemplo)', value="`123e4567-e89b-12d3-a456-426614174000`", inline=False)
            dm_embed.add_field(name='📌 Importante', value=f"Cole este ID no comprovante:\n`{order_id}`", inline=False)
            
            await interaction.user.send(embed=dm_embed)
        except:
            pass

class PedidosView(ui.View):
    """View para gerenciar pedidos"""
    
    def __init__(self, orders, cog):
        super().__init__(timeout=None)
        self.orders = orders
        self.cog = cog
    
    @ui.button(label='✅ Confirmar Pedido', style=discord.ButtonStyle.success)
    async def confirm_button(self, interaction: discord.Interaction, button: ui.Button):
        """Abre modal para confirmar pedido"""
        
        modal = ConfirmarPedidoModal(self.orders, self.cog)
        await interaction.response.send_modal(modal)

class ConfirmarPedidoModal(ui.Modal):
    """Modal para confirmar pedido"""
    
    def __init__(self, orders, cog):
        super().__init__(title='Confirmar Pagamento')
        self.orders = orders
        self.cog = cog
        
        self.add_item(ui.TextInput(
            label='ID do Pedido',
            placeholder='PED_123456789_20251201120000',
            required=True
        ))
    
    async def on_submit(self, interaction: discord.Interaction):
        """Confirma o pedido"""
        
        order_id = self.children[0].value
        
        if order_id not in self.orders:
            await interaction.response.send_message(f'❌ Pedido "{order_id}" não encontrado!', ephemeral=True)
            return
        
        order = self.orders[order_id]
        
        if order['status'] != 'pendente':
            await interaction.response.send_message(f'❌ Este pedido já foi {order["status"]}!', ephemeral=True)
            return
        
        # Confirmar pedido
        order['status'] = 'confirmado'
        order['confirmado_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
        order['confirmado_por'] = interaction.user.name
        self.cog.save_orders()
        
        embed = discord.Embed(
            title='✅ Pedido Confirmado!',
            description=f'Pedido {order_id} foi confirmado com sucesso!',
            color=discord.Color.green()
        )
        
        embed.add_field(name='Produto', value=order['produto'], inline=True)
        embed.add_field(name='Cliente', value=order['cliente'], inline=True)
        embed.add_field(name='Valor', value=f"R$ {order['total']:.2f}", inline=True)
        
        await interaction.response.send_message(embed=embed)
        
        # Notificar usuário
        try:
            user = await interaction.client.fetch_user(int(order['usuario_id']))
            notif_embed = discord.Embed(
                title='✅ Pagamento Confirmado!',
                description=f'Seu pedido foi confirmado! Aqui está seu produto:',
                color=discord.Color.green()
            )
            notif_embed.add_field(name='🎫 ID', value=order_id, inline=False)
            notif_embed.add_field(name='📦 Produto', value=order['produto'], inline=False)
            
            await user.send(embed=notif_embed)
        except:
            pass

async def setup(bot):
    """Carrega o cog"""
    await bot.add_cog(Vendas(bot))

