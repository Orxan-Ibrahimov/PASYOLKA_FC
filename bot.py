import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

users = []
active = False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active
    active = True
    await update.message.reply_text(
        "🟢 Siyahı başladıldı!\n\n"
        "+ əlavə et\n"
        "- sil\n"
        "/end bağla\n"
        "/restart sıfırla"
    )


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global users, active
    users = []
    active = True
    await update.message.reply_text("🔄 Sistem yenidən başladı!\nSiyahı sıfırlandı.")


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active
    active = False

    if users:
        msg = "🔒 Siyahı tamamlandı!\n\n" + "\n".join(
            [f"{i+1}. {u}" for i, u in enumerate(users)]
        )
    else:
        msg = "🔒 Siyahı tamamlandı!\nSiyahı boşdur"

    await update.message.reply_text(msg)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active

    # ❗ siyahı bağlıdırsa heç nə etmə
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


async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("restart", restart))
    app.add_handler(CommandHandler("end", end))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())