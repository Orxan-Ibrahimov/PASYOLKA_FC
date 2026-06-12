from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = "BURAYA_BOT_TOKEN"

users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Futbol botu aktivdir. + yazın.")

async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "+":
        users.add(update.message.from_user.first_name)
        await update.message.reply_text("Qeyd olundun ✔")

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if users:
        msg = "\n".join([f"{i+1}. {u}" for i, u in enumerate(users)])
    else:
        msg = "Hələ heç kim yoxdur."
    await update.message.reply_text(msg)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_user))
app.add_handler(CommandHandler("siyahi", list_users))

app.run_polling()