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


path_file = '/root/tg_bot'
db_host = "93.93.207.52"
db_user = "gen_user" 
db_password = "PUQC7sa$"
db_name = "default_db"



token = '5766763452:AAG14hwIr0o3pxAN1JRYlnk7hhIeH1CobXM'
bot = Bot(token)
app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.post("/get_photo")
async def webhook2(photo: str = Form(...),
        user_id: str = Form(...),):
    await bot.send_photo(user_id, FSInputFile(photo))
        
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

        mycursor.close()
        mydb.close()

        if subscription > 0:
            await send_telegram_photo(user_id, photo, redirect_url)
        else:
            photo_path = await save_image(photo, "data/images")

         
        
            kb_list = [
              [types.InlineKeyboardButton(text='Открыть фото', callback_data=f'ph_{str(photo_path)}')]
            ]


            keyboard =  InlineKeyboardMarkup(inline_keyboard=kb_list)


            await send_telegram_message(user_id, f"Вам пришло новое фото!\nТикток: {redirect_url}", reply_markup=keyboard)

    return {"status": "Success"}


async def send_telegram_message(user_id, text, reply_markup):
    await bot.send_message(user_id, text, reply_markup=reply_markup, disable_web_page_preview=True)


async def send_telegram_photo(user_id, photo, redirect_url):
    photo_path = await save_image(photo, "data/images")
    await bot.send_photo(user_id, FSInputFile(photo_path), caption=f'Вам пришло новое фото!\nТикток: {redirect_url}')


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
