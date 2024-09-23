from flask import Flask, jsonify, request, redirect
import asyncio
from aiogram import Bot
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



token = '5766763452:AAG14hwIr0o3pxAN1JRYlnk7hhIeH1CobXM'


bot = Bot(token)


async def gg(user_id, text):

    

    await bot.send_message(user_id, f'{text}!')


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def webhook():

    try:
        data = request.args.get("tiktok")

        asyncio.get_event_loop().run_until_complete(gg(5779182088, str(data)))

    except Exception as e:
        asyncio.get_event_loop().run_until_complete(gg(5779182088, str(e)))


    try:
        data = request.get_json(force=False, silent=False, cache=True)

        asyncio.get_event_loop().run_until_complete(gg(5779182088, str(data)))

   
    except Exception as e:
        asyncio.get_event_loop().run_until_complete(gg(5779182088, str(e)))




if __name__ == '__main__':
    app.run(debug=True)
