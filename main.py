import os
from aiogram.utils import executor
from dotenv import load_dotenv
import requests
import json
from aiogram import Bot, Dispatcher, types

load_dotenv()

# Replace 'YOUR_BOT_TOKEN' with your Telegram bot token
TOKEN = os.getenv('TG_TOKEN')


# Create instances of the Bot and Dispatcher classes
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Handler for the /start command
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Я бот, который показывает температуру в заданном городе. Просто напиши название города!")

# Handler for text messages
@dp.message_handler(content_types=types.ContentType.TEXT)
async def echo(message: types.Message):
    city = message.text
    temperature = get_temperature(city)
    if temperature is not None:
        await message.answer(f"Температура в городе {city} сейчас {temperature}°C.")
    else:
        await message.answer("Извините, не удалось получить информацию о погоде.")

# Get temperature using the OpenWeatherMap API
def get_temperature(city):
    api_key = os.getenv('WEATHER_API')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = json.loads(response.text)
    if response.status_code == 200:
        temperature = data['main']['temp']
        return temperature
    else:
        return None

def main():
    # Start the bot
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()
