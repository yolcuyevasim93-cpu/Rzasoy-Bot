import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from flask import Flask
from threading import Thread

# Bot sazlamaları
BOT_TOKEN = "8421111075:AAGCv5a7M1YyrCrHsrS11780ca17dNDHHKI"
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Flask sazlaması (Render-in servisi dayandırmaması üçün)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot aktivdir!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Botun işə düşməsi
async def main():
    print("Bot işə düşdü...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Flask-ı arxa planda işə salırıq
    Thread(target=run_flask).start()
    # Botu əsas dövrədə işə salırıq
    asyncio.run(main())
  
