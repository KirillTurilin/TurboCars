from pyrogram import Client, filters
from pyrogram.types import Message
import database

ADMIN_ID = 406675702
CHAT_ID = 1001934227821
MY_ID = 6148439050
bot = Client(name="AutoReplyTurboCars",
             api_id=19584363,
             api_hash="c8247fbf45c56ca820c5b44b3ae78abf",
             phone_number="89853470136")


#хендлер входящих сообщений от пользователя
@bot.on_message()
async def message_handler(client: Client, message: Message):
    if message.from_user.is_bot or message.from_user.id == MY_ID:
        return
    check = database.check_autoreply(MY_ID)
    if check:
        check_is_first = database.check_is_first(message.chat.id, MY_ID)
        print(check_is_first)
        if not check_is_first:
            database.add_users(message.chat.id, MY_ID)
            with open("text_reply.txt", mode="r") as file:
                text = file.read()
            await client.send_message(chat_id=message.chat.id, text=text)
        elif check_is_first == ["True"]:
            with open("text_reply.txt", mode="r", encoding="utf-8") as file:
                text = file.read()
            await client.send_message(chat_id=message.chat.id, text=text)
        if message.text:
            await client.send_message(chat_id=CHAT_ID, text=message.text)
            await client.send_message(chat_id=CHAT_ID, text=f"Пересланно от {message.from_user.username}")
        elif message.video:
            await client.send_video(chat_id=CHAT_ID, video=message.video.file_id)
            await client.send_message(chat_id=CHAT_ID, text=f"Пересланно от {message.from_user.username}")
        elif message.audio:
            await client.send_audio(chat_id=CHAT_ID, audio=message.audio.file_id)
            await client.send_message(chat_id=CHAT_ID, text=f"Пересланно от {message.from_user.username}")
        elif message.photo:
            await client.send_photo(chat_id=CHAT_ID, photo=message.photo.file_id)
            await client.send_message(chat_id=CHAT_ID, text=f"Пересланно от {message.from_user.username}")
        elif message.document:
            await client.send_document(chat_id=CHAT_ID, document=message.document.file_id)
            await client.send_message(chat_id=CHAT_ID, text=f"Пересланно от {message.from_user.username}")

@bot.on_message(filters.reply)
async def reply_handler(client: Client, message: Message):
    if message.chat.id != CHAT_ID or message.from_user.id != ADMIN_ID:
        return

    if message.text == "+":
        database.del_autoreply(MY_ID)
        database.zeroing_users(MY_ID)
        await client.send_message(chat_id=CHAT_ID, text="🚫Автоответ ОТКЛЮЧЕН")
    if message.text[0] == "-":
        text = message.text[1::]
        database.add_autoreply(MY_ID)
        with open("text_reply.txt", mode="w", encoding="utf-8") as file:
            file.write(text)
        await client.send_message(chat_id=CHAT_ID, text=f"✅Автоответ ЗАПУЩЕН\nтеперь автоответ:\n{text}")


try:
    bot.run()
except Exception as ex:
    print(ex)


