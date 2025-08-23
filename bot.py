import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from async_utils import download_audio_async, clean_temp_async


user_tasks = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь команду /get <название видео>, чтобы скачать аудио с YouTube."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start - начать работу\n"
        "/get <название> - скачать аудио с YouTube\n"
        "/status - статус ваших загрузок"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_tasks:
        await update.message.reply_text("📊 У вас есть активная задача загрузки.")
    else:
        await update.message.reply_text("✅ У вас нет активных задач.")

async def get_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    query = " ".join(context.args)
    
    if not query:
        await update.message.reply_text("Отправь название видео после команды.")
        return


    if user_id in user_tasks:
        await update.message.reply_text("⏳ У вас уже есть активная загрузка. Дождитесь её завершения.")
        return

    try:
        status_message = await update.message.reply_text("✅ Запрос принят. Начинаю загрузку...")
        user_tasks[user_id] = {
            'status_message': status_message,
            'query': query
        }

        asyncio.create_task(process_download(update, user_id, query))
        
    except Exception as e:
        if user_id in user_tasks:
            del user_tasks[user_id]
        await update.message.reply_text(f"❌ Ошибка: {e}")

async def process_download(update: Update, user_id: int, query: str):
    try:
        if user_id in user_tasks:
            await user_tasks[user_id]['status_message'].edit_text("🔍 Ищу видео...")

        file_path = await download_audio_async(query)

        if user_id in user_tasks:
            await user_tasks[user_id]['status_message'].edit_text("📤 Отправляю файл...")

        with open(file_path, 'rb') as audio_file:
            await update.message.reply_audio(audio=audio_file)

        await clean_temp_async()

        if user_id in user_tasks:
            await user_tasks[user_id]['status_message'].edit_text("✅ Готово! Наслаждайтесь!")
            
    except Exception as e:
        error_msg = f"❌ Ошибка при загрузке: {e}"
        if user_id in user_tasks:
            await user_tasks[user_id]['status_message'].edit_text(error_msg)
        else:
            await update.message.reply_text(error_msg)
    finally:
        if user_id in user_tasks:
            del user_tasks[user_id]

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("get", get_audio))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()

