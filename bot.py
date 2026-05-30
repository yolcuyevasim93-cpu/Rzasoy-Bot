import os
from aiogram import Bot, Dispatcher
from flask import Flask
from threading import Thread

# Botun sazlamaları
TOKEN = "8421111075:AAGCv5a7M1YyrCrHsrS11780ca17dNDHHKI"
bot = Bot(token=TOKEN)
dp = Dispatcher()
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot aktivdir!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Botu işə salmaq üçün (sadəcə polling)
if __name__ == "__main__":
    Thread(target=run_flask).start()
    dp.run_polling(bot)
    
