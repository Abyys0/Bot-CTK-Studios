# 🚀 GUIA RENDER - BOT DISCORD 24/7

## ✅ O QUE VOCÊ TEM PRONTO

Seu bot está **100% pronto** para rodar no Render!

- ✓ Arquivo `Procfile` ✓ `requirements.txt` ✓ `main.py`
- ✓ Sistema de tickets ✓ Logs automáticos ✓ Painel ADM
- ✓ Comandos completos

---

## 🎯 PASSO A PASSO (Super simples)

### 1️⃣ CRIAR CONTA NO RENDER
1. Entre em https://render.com
2. Clique em "Sign up"
3. Crie conta (pode usar GitHub)

### 2️⃣ PREPARAR GITHUB
Você precisa fazer upload do seu código no GitHub:

1. Crie conta em https://github.com (se não tiver)
2. Crie um repositório novo chamado `bot-discord`
3. Copie estes comandos no PowerShell (em sua pasta do bot):

```powershell
cd C:\Users\rigob\Desktop\BOTS\ GGMAX
git init
git add .
git commit -m "Bot Discord"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/bot-discord.git
git push -u origin main
```

**Substitua `SEU_USUARIO` pelo seu nome GitHub!**

### 3️⃣ FAZER DEPLOY NO RENDER

1. Volte em https://render.com (logado)
2. Clique em **"New"** (canto superior direito)
3. Escolha **"Web Service"**
4. Conecte seu repositório GitHub
5. Preencha assim:
   - **Name**: `bot-discord` (qualquer nome)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Instance Type**: `Free` (para economizar)

6. Role até **"Environment"**
7. Clique em **"Add Environment Variable"**
8. Adicione EXATAMENTE assim:
   ```
   Key: DISCORD_TOKEN
   Value: seu_token_aqui
   ```

9. Clique em **"Create Web Service"**

### 4️⃣ AGUARDAR E VERIFICAR

1. Render vai começar a fazer deploy (leva 2-3 min)
2. Quando a barra ficar verde = ✅ Funcionando!
3. Seu bot aparecerá **ONLINE** no Discord

---

## 🔑 OBTER SEU TOKEN DISCORD

1. Entre em https://discord.com/developers/applications
2. Clique em **"New Application"**
3. Vá para a aba **"Bot"**
4. Clique em **"Add Bot"**
5. Copie o token (está em "TOKEN")

⚠️ **NÃO COMPARTILHE este token com ninguém!**

---

## ✨ SEU BOT ESTARÁ 24/7!

Depois que estiver no Render:
- ✅ Roda 24/7 grátis
- ✅ Reboota automaticamente se cair
- ✅ Reboota a cada 15 dias (normal)
- ✅ Sem limite de uptime

---

## 📊 MONITORAR BOT

No Render, clique no seu Web Service e veja:
- Status (verde = online)
- Logs em tempo real
- Mensagens de erro

---

## 💡 DICAS

**Se o bot não ligar no Discord:**
1. Verifique o log no Render (procure por erro)
2. Confirme que o token está correto
3. Certifique-se que copiou EXATAMENTE os comandos git

**Se aparecer "Build failed":**
1. Verifique se `requirements.txt` está correto
2. Tente fazer git push novamente
3. Veja o erro no log do Render

---

## 🆘 PRECISA FAZER ATUALIZAÇÕES?

Quando quiser adicionar algo ao bot:

1. Edite o arquivo localmente
2. Execute no PowerShell:
   ```powershell
   git add .
   git commit -m "Descrição da mudança"
   git push origin main
   ```
3. Render detecta automaticamente e redeploy! 🔄

---

## 📱 COMANDOS DO BOT

```
!ping - Latência
!hello - Sauda
!info - Info do bot
!avatar - Avatar
!userinfo - Info do usuário
!serverinfo - Info do servidor
!clear [n] - Limpa chat
!setup_tickets - Cria tickets
!setup_admin_panel - Painel ADM
!logs - Mostra logs
```

---

**Tudo pronto? Bora colocar online! 🚀**
