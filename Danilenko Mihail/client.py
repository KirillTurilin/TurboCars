from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
import database

ADMIN_ID = 406675702
CHAT_ID =-1001934227821
MY_ID = 852293214
bot = Client(name="AutoReplyTurboCars",
             api_id=19584363,
             api_hash="c8247fbf45c56ca820c5b44b3ae78abf",
             phone_number="+79494882300")


# хендлер входящих сообщений от пользователя и админа группы
@bot.on_message()
async def message_handler(client: Client, message: Message):
    print(message.reply_to_message)
    if message.reply_to_message and message.chat.id == CHAT_ID and message.reply_to_message.from_user.id == MY_ID and message.from_user.id != MY_ID:
        if message.from_user.id != ADMIN_ID:
            return
        if message.text == "+":
            database.del_autoreply(MY_ID)
            database.zeroing_users(MY_ID)
            await client.send_message(chat_id=CHAT_ID, text="🚫Автоответ ОТКЛЮЧЕН")
        if message.text[0] == "-":
            text = message.text[2::]
            print(text)
            database.add_autoreply(MY_ID)
            with open("text_reply.txt", mode="w", encoding="utf-8") as file:
                file.write(text)
            await client.send_message(chat_id=CHAT_ID, text=f"✅Автоответ ЗАПУЩЕН\nтеперь автоответ:\n{text}")
    elif message.chat.type == ChatType.PRIVATE and message.from_user.id != MY_ID:
        if message.from_user.is_bot or message.from_user.id == MY_ID or message.from_user.id != message.chat.id:
            return
        check = database.check_autoreply(MY_ID)
        if check:
            check_is_first = database.check_is_first(message.chat.id, MY_ID)
            print(check_is_first)
            if message.from_user.id != MY_ID:
                with open("text_reply.txt", mode="r", encoding="utf-8") as file:
                    text = file.read()
                msg = await client.send_message(chat_id=message.chat.id, text=text)
                await client.forward_messages(chat_id=CHAT_ID, from_chat_id=message.chat.id, message_ids=message.id)
                if not check_is_first:
                    database.add_users(message.chat.id, MY_ID)
                    await client.forward_messages(chat_id=CHAT_ID, from_chat_id=message.chat.id, message_ids=msg.id)
                elif check_is_first == "True":
                    await client.forward_messages(chat_id=CHAT_ID, from_chat_id=message.chat.id, message_ids=msg.id)


try:
    bot.run()
except Exception as ex:
    print(ex)



