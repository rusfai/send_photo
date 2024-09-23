from flask import Flask, jsonify, request, redirect
import asyncio
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

token = '5766763452:AAG14hwIr0o3pxAN1JRYlnk7hhIeH1CobXM'
bot = Bot(token)

async def gg(user_id, text):
    await bot.send_message(user_id, f'{text}!')

app = Flask(__name__)

@app.route('/tiktok', methods=['POST', 'GET'])
def webhook():
    print("Received request")
    asyncio.get_event_loop().run_until_complete(gg(5779182088, "Получен запрос"))

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

    asyncio.get_event_loop().run_until_complete(gg(5779182088, f"Данные запроса: {str(log_data)}"))

    # Обработка параметров запроса
    tiktok_param = request.args.get("tiktok")
    if tiktok_param:
        asyncio.get_event_loop().run_until_complete(gg(5779182088, f"Параметр tiktok: {tiktok_param}"))

    # Обработка JSON-данных
    try:
        json_data = request.get_json(force=False, silent=False, cache=True)
        if json_data:
            asyncio.get_event_loop().run_until_complete(gg(5779182088, f"JSON данные: {str(json_data)}"))
    except Exception as e:
        asyncio.get_event_loop().run_until_complete(gg(5779182088, f"Ошибка при обработке JSON: {str(e)}"))

    return 'Success'

if __name__ == '__main__':
    app.run(debug=True)
