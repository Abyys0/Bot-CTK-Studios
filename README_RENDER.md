# Bot Discord GGMAX 🤖

Um bot Discord moderno, completo e pronto para produção.

## ✨ Funcionalidades

- ✅ **Comandos Básicos**: ping, hello, info, avatar, userinfo, serverinfo
- ✅ **Sistema de Tickets**: Suporte e gerenciamento de tickets
- ✅ **Painel ADM Privado**: Canal exclusivo para administradores
- ✅ **Logs Automáticos**: Registra todas as ações do servidor
- ✅ **Limpeza de Chat**: Comando para limpar mensagens
- ✅ **Exportação de Logs**: Gera arquivo com histórico completo

## 📋 Requisitos

- Python 3.8+
- discord.py
- python-dotenv

## 🚀 Instalação Local

```bash
# 1. Clonar ou extrair projeto
cd BOTS\ GGMAX

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Configurar .env (ver seção abaixo)

# 6. Executar bot
python main.py
```

## ⚙️ Configuração (.env)

Crie um arquivo `.env` na raiz do projeto:

```env
DISCORD_TOKEN=seu_token_discord_aqui
OPENAI_API_KEY=sua_chave_openai_aqui
```

### Obter Token Discord
1. Acesse https://discord.com/developers/applications
2. Clique em "New Application"
3. Vá para "Bot" → "Add Bot"
4. Copie o token em "TOKEN"
5. Ative as "Privileged Gateway Intents":
   - MESSAGE CONTENT INTENT
   - SERVER MEMBERS INTENT

## 🌐 Deploy no Render (Recomendado)

### Passo 1: Preparar GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### Passo 2: Deploy no Render
1. Entre em https://render.com
2. Clique em "New" → "Web Service"
3. Conecte seu repositório GitHub
4. Configure:
   - **Name**: seu-bot-discord
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
5. Em "Environment", adicione:
   ```
   DISCORD_TOKEN=seu_token
   OPENAI_API_KEY=sua_chave (opcional)
   ```
6. Clique em "Create Web Service"

## 📝 Comandos Disponíveis

### 🎮 Básicos
- `!ping` - Latência do bot
- `!hello` - Sauda você
- `!info` - Info do bot
- `!avatar` - Mostra avatar
- `!userinfo` - Info do usuário
- `!serverinfo` - Info do servidor

### 🎫 Tickets
- `!setup_tickets` - Cria painel de tickets

### 🔐 Admin
- `!setup_admin_panel` - Cria painel ADM
- `!clear [número]` - Limpa mensagens
- `!logs` - Mostra logs
- `!logs_user @usuario` - Logs de um usuário
- `!export_logs` - Exporta logs em arquivo

### 🤖 ChatGPT (opcional)
- `!chat <pergunta>` - Conversa com IA
- `!translate <idioma> <texto>` - Traduz
- `!resumo <texto>` - Resume texto
- `!piada` - Gera piada

## 📁 Estrutura

```
BOTS GGMAX/
├── main.py                 # Entrada principal
├── cogs/                   # Módulos de comandos
│   ├── basic.py           # Comandos básicos
│   ├── tickets.py         # Sistema de tickets
│   ├── event_logger.py    # Logs e painel ADM
│   ├── chatgpt.py         # Integração IA (opcional)
│   └── __init__.py
├── .env                    # Variáveis de ambiente
├── .gitignore             # Arquivos ignorados
├── Procfile               # Deploy config
├── requirements.txt       # Dependências
└── README.md             # Este arquivo
```

## 🛠️ Adicionar Novo Comando

Crie um arquivo em `cogs/novo_comando.py`:

```python
from discord.ext import commands
import discord

class MeuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='meucomando')
    async def meu_comando(self, ctx):
        """Descrição do comando"""
        await ctx.send('Resposta!')

async def setup(bot):
    await bot.add_cog(MeuCog(bot))
```

## 🔄 Variáveis de Ambiente

| Variável | Obrigatório | Descrição |
|----------|-------------|-----------|
| `DISCORD_TOKEN` | ✅ Sim | Token do bot Discord |
| `OPENAI_API_KEY` | ❌ Não | Chave OpenAI para ChatGPT |

## 📊 Logs e Monitoramento

O bot registra automaticamente:
- Membros entrando/saindo
- Mensagens deletadas/editadas
- Cargos adicionados/removidos
- Ações em tickets

Todos os logs são salvos em `server_logs.json` e também enviados para um canal configurável.

## 🚨 Troubleshooting

### Bot não responde
- Verifique se o token está correto
- Ative as "Privileged Gateway Intents"
- Verifique as permissões do bot

### Erro ao carregar cogs
- Remova arquivos `.pyc` em `__pycache__`
- Reinstale dependências: `pip install -r requirements.txt --upgrade`

### Render não inicia
- Verifique o `Procfile`
- Veja os logs em Render Dashboard
- Confirme as variáveis de ambiente

## 💡 Dicas

- Use `!setup_admin_panel` para monitorar o servidor
- Configure `!setup_tickets` para suporte
- Verifique logs regularmente com `!logs`

## 📞 Suporte

Para problemas ou sugestões, abra uma issue ou entre em contato.

---

**Desenvolvido com ❤️ usando discord.py**
