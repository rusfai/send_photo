from flask import Flask, jsonify, request, redirect
import asyncio
from aiogram import Bot
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



token = '5766763452:AAG14hwIr0o3pxAN1JRYlnk7hhIeH1CobXM'


bot = Bot(token)


async def gg(user_id, text):

    

    await bot.send_message(user_id, f'{text}!')

    return 'sucsess'


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def webhook():
    try:
        data = request.get_json(force=False, silent=False, cache=True)

        asyncio.get_event_loop().run_until_complete(gg(5779182088, str(data)))

        return 'sucsess'
    except:
        asyncio.get_event_loop().run_until_complete(gg(5779182088, str('Ошибка')))
        return 'warning' 



if __name__ == '__main__':
    app.run(debug=True)
