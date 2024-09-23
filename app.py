from flask import Flask, jsonify, request, redirect
import asyncio
from aiogram import Bot
import mysql
import mysql.connector
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



token = '7213796949:AAEXU9wzXOWAvR_qkI_zxjIm_C30Z0EeKAA'

db_host = "185.247.185.204"
db_user = "gen_user" 
db_password = "HTXFmxM6=ri\+"
db_name = "default_db"


bot = Bot(token)

def connect():
    mydb = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
    )
    return mydb

async def gg(user_id, account, amount, message_id):

    text = "После оплаты деньги как правило поступают моментально! Если нет, обратитесь в поддержку."
    
    kb_list = [
            [InlineKeyboardButton(text="Задать вопрос", url="https://t.me/anypayservice")],
            [InlineKeyboardButton(text="Пополнить еще", callback_data="start")]
            ]
    
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)

    kb = [
      [types.InlineKeyboardButton(text="Подписаться", url=f'''https://t.me/anypaymentTG''')]
      ]

    keyboard_channel = InlineKeyboardMarkup(inline_keyboard=kb)


    await bot.edit_message_text(text=text, chat_id=user_id, message_id=message_id, reply_markup=keyboard)
    await bot.send_message(user_id, f'Аккаунт {account} успешно пополнен на {amount} рублей!\n\n<a href=https://t.me/anypaymentTG>Не забудь подписаться на наш ТГ канал</a>', reply_markup=keyboard_channel, parse_mode="HTML")

    return 'sucsess'


app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    mydb = connect()
    mycursor = mydb.cursor(buffered=True)
    try:
        data = request.get_json(force=False, silent=False, cache=True)
  
        mycursor.execute("SELECT * FROM kwork16_payments WHERE transaction_id = '{}'".format(data['order_uuid']))
        payment_info = mycursor.fetchone()


        mycursor.execute("SELECT * FROM kwork16_users WHERE user_id = '{}'".format(payment_info[1]))
        user_info = mycursor.fetchone()
        bonus = int(user_info[2])
        if bonus >= 0:
            bonus = bonus - 1
        
        mycursor.execute("UPDATE kwork16_users SET bonuses = '{}' WHERE user_id = '{}' ".format(bonus, int(payment_info[1])))
        mydb.commit()

        mycursor.close()
        mydb.close()

        asyncio.get_event_loop().run_until_complete(gg(payment_info[1], payment_info[2], payment_info[3], payment_info[5]))


    
        return 'sucsess'
    except:
        mycursor.close()
        mydb.close()
        return 'warning' 




if __name__ == '__main__':
    app.run(debug=True)