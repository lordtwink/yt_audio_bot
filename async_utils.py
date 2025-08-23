# async_utils.py
import asyncio
from concurrent.futures import ThreadPoolExecutor
from downloader import download_audio_sync, clean_temp_sync

# Создаем пул потоков для выполнения блокирующих операций
download_executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="Downloader")
cleanup_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="Cleanup")

async def download_audio_async(query: str) -> str:
    """Асинхронная обертка для скачивания аудио"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(download_executor, download_audio_sync, query)

async def clean_temp_async():
    """Асинхронная обертка для очистки временных файлов"""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(cleanup_executor, clean_temp_sync)