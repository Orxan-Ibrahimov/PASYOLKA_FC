import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

users = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Futbol botu aktivdir. '+' yazın.")

async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.strip() == "+":
        name = update.message.from_user.first_name
        if name not in users:
            users.append(name)
            await update.message.reply_text(f"{name} qeyd olundu ✔")
        else:
            await update.message.reply_text(f"{name} artıq siyahıda var ✅")
                                                                             

async def siyahi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if users:
        msg = "\n".join([f"{i+1}. {u}" for i, u in enumerate(users)])
    else:
        msg = "Siyahı boşdur"
    await update.message.reply_text(msg)


async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("siyahi", siyahi))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_user))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    await asyncio.Event().wait()   # botu açıq saxlayır


if __name__ == "__main__":
    asyncio.run(main())