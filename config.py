import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TEMP_DIR = os.getenv("TEMP_DIR", "temp")


PROXY_IP = os.getenv("PROXY_IP")
PROXY_PORT = os.getenv("PROXY_PORT")
PROXY_LOGIN = os.getenv("PROXY_LOGIN")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")


if all([PROXY_IP, PROXY_PORT, PROXY_LOGIN, PROXY_PASSWORD]):
    PROXY_URL = f"socks5://{PROXY_LOGIN}:{PROXY_PASSWORD}@{PROXY_IP}:{PROXY_PORT}"
else:

    PROXY_URL = None
