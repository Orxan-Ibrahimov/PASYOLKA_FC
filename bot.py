import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

users = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Futbol botu aktivdir. '+' yazın və ya '-' silmək üçün.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    name = update.message.from_user.first_name

    # ADD USER
    if text == "+":
        if name not in users:
            users.append(name)
            await update.message.reply_text(f"{name} qeyd olundu ✔")
        else:
            await update.message.reply_text(f"{name} artıq siyahıda var ✅")

    # REMOVE USER
    elif text == "-":
        if name in users:
            users.remove(name)
            await update.message.reply_text(f"{name} silindi ❌")
        else:
            await update.message.reply_text(f"{name} siyahıda yoxdur ⚠")

async def siyahi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if users:
        msg = "\n".join([f"{i+1}. {u}" for i, u in enumerate(users)])
    else:
        msg = "Siyahı boşdur"
    await update.message.reply_text(msg)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("siyahi", siyahi))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()