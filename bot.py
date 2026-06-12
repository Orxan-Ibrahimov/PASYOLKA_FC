import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

users = []
active = False  # əvvəl bağlıdır

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active
    active = True
    await update.message.reply_text("🟢 Siyahı başladıldı!\n+ əlavə et\n- sil\n/end bağla")

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global users, active
    users = []
    active = True
    await update.message.reply_text("🔄 Sistem yenidən başladı!\nSiyahı sıfırlandı.")

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active
    active = False

    if users:
        msg = "🔒 Siyahı tamamlandı!\n\n" + "\n".join([f"{i+1}. {u}" for i, u in enumerate(users)])
    else:
        msg = "🔒 Siyahı tamamlandı!\nSiyahı boşdur"

    await update.message.reply_text(msg)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active

    if not active:
        return

    text = update.message.text.strip()
    name = update.message.from_user.first_name

    if text == "+":
        if name not in users:
            users.append(name)
            await update.message.reply_text(f"➕ {name} əlavə edildi")
        else:
            await update.message.reply_text("Artıq siyahıdasan")

    elif text == "-":
        if name in users:
            users.remove(name)
            await update.message.reply_text(f"➖ {name} silindi")
        else:
            await update.message.reply_text("Sən siyahıda deyilsən")


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("restart", restart))
app.add_handler(CommandHandler("end", end))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()