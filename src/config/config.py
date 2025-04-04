import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env

class Config:
    DB_URL = (
        f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

config = Config()


