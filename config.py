import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TOKEN = os.getenv("BOT_TOKEN", "8778234751:AAG7T3iomebXrrZYWfDfUSVxmIgnrbaqCvY")

# URL вашего Mini App
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://alnino18.github.io/Hisobchi_app/index.html")

# FastAPI настройки
FASTAPI_HOST = "0.0.0.0"
FASTAPI_PORT = int(os.getenv("PORT", 8000))