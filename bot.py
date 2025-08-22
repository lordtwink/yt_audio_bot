import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from downloader import download_audio, clean_temp
from config import TELEGRAM_BOT_TOKEN, TEMP_DIR

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь команду /get <название видео>, чтобы скачать аудио с YouTube."
    )

async def get_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Отправь название видео после команды.")
        return

    message = await update.message.reply_text("Ищу и скачиваю аудио...")
    try:
        file_path = download_audio(query)
        await update.message.reply_audio(open(file_path, 'rb'))
        clean_temp()  # чистим временные файлы
        await message.edit_text("Готово! 🎵")
    except Exception as e:
        await message.edit_text(f"Ошибка: {e}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get", get_audio))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
