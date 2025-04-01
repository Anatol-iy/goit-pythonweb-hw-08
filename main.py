from fastapi import FastAPI
import logging
from src.api import contacts, utils
from datetime import datetime
import pytz

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

@app.on_event("startup")
async def startup():
    # Логування при старті сервера
    timezone = pytz.timezone("Europe/Kiev")  # Задайте правильний часовий пояс
    current_time = datetime.now(timezone)
    logging.debug(f"Server started at: {current_time}")

app.include_router(utils.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)