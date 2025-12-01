# Bot Discord GGMAX

Um bot Discord moderno e funcional criado com discord.py.

## 📋 Requisitos

- Python 3.8+
- discord.py
- python-dotenv (para gerenciar variáveis de ambiente)

## 🚀 Instalação

1. Clone ou extraia o projeto
2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   ```

3. Ative o ambiente virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure seu token do Discord no arquivo `.env`

## ⚙️ Configuração

1. Crie um arquivo `.env` na raiz do projeto:
   ```
   DISCORD_TOKEN=seu_token_aqui
   ```

2. Para obter seu token:
   - Acesse https://discord.com/developers/applications
   - Clique em "New Application"
   - Vá para "Bot" e clique em "Add Bot"
   - Copie o token em "TOKEN"

## ▶️ Executar o Bot

```bash
python main.py
```

## 📝 Comandos Disponíveis

- `!ping` - Responde com pong (teste de latência)
- `!hello` - Sauda o usuário
- `!info` - Mostra informações do bot

## 📁 Estrutura do Projeto

```
BOTS GGMAX/
├── main.py           # Arquivo principal do bot
├── cogs/             # Comandos organizados em módulos
│   └── basic.py      # Comandos básicos
├── .env              # Variáveis de ambiente
├── requirements.txt  # Dependências do projeto
└── README.md         # Este arquivo
```
