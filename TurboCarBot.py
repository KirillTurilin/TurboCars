import asyncio
import datetime
import logging
from aiogram.filters import PROMOTED_TRANSITION, LEAVE_TRANSITION, IS_MEMBER, IS_ADMIN
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import URLInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, Chat, Message, CallbackQuery
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

import database
import keyboard as kb
import config
from config import names

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class FilterUp(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        try:
            print(callback.data)
            if int(callback.data) in config.names:
                return True
            return False
        except Exception:
            return False


class FilterDown(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        try:
            print(callback.data)
            if int(f"{callback.data}"[1::]) in config.names:
                return True
            return False
        except Exception:
            return False


class States(StatesGroup):
    id = State()
    text = State()


async def set_commands(bot: Bot):
    commands = [BotCommand(command='start', description='Отключить/Включить автоответ')]
    await bot.set_my_commands(commands)


@dp.message(Command("start"))
async def start_cmd(message: Message, bot: Bot):
    await message.answer("🤖Привет я бот TurboCarsBot создан для включения и выключения автоответов",
                         reply_markup=kb.kb_menu)


@dp.callback_query(F.data == "goup")
async def goup(callback: CallbackQuery):
    await callback.message.edit_text("Выбери сотрудника для кого мне <b>включить</b> автоответ⬇️",
                                     reply_markup=await kb.select_all_autoreply_kb(), parse_mode="HTML")


@dp.callback_query(F.data == "godown")
async def godown(callback: CallbackQuery):
    await callback.message.edit_text("Выбери сотрудника для кого мне <b>отключить</b> автоответ⬇️",
                                     reply_markup=await kb.select_all_autoreply_kb_no(), parse_mode="HTML")


@dp.callback_query(F.data == "exit")
async def exit(callback: CallbackQuery):
    await callback.message.edit_text("🤖Привет я бот TurboCarsBot создан для включения и выключения автоответов",
                                     reply_markup=kb.kb_menu)


@dp.callback_query(FilterUp())
async def add_cmd(callback: CallbackQuery, state: FSMContext):
    print(11)
    await state.update_data(id=callback.data)
    await callback.message.edit_text(
        f"Вы выбрали сотрудника {config.names[int(callback.data)]} включить для него автоответ?", reply_markup=kb.kb_up)


@dp.callback_query(F.data == "yes")
async def yes_cmd(callback: CallbackQuery, state: FSMContext):
    user_id = (await state.get_data())["id"]
    await database.add_autoreply(user_id)
    await callback.message.edit_text("✅Автоответ включен")


@dp.callback_query(F.data == "rename")
async def yes_cmd(callback: CallbackQuery, state: FSMContext):
    await state.set_state(States.text)
    await callback.message.edit_text(
        "Пришлите текст нового автоответа⬇️(после того как вы пришлете сообщение автоответ включится что бы отменить напишите /start)")


@dp.message(States.text)
async def get_text(message: Message, state: FSMContext):
    user_id = int((await state.get_data())["id"])
    print(user_id)
    await database.add_autoreply(user_id)
    if user_id == 852293214:
        with open("Danilenko_Mihail/text_reply.txt", mode="w", encoding="utf-8") as file:
            file.write(message.text)
    elif user_id == 6148439050:
        with open("Kamendov_Bogdan/text_reply.txt", mode="w", encoding="utf-8") as file:
            file.write(message.text)
    elif user_id == 6047837420:
        with open("Nazarenco_Nikita/text_reply.txt", mode="w", encoding="utf-8") as file:
            file.write(message.text)
    elif user_id == 6292818106:
        with open("Shashurin_Andrey/text_reply.txt", mode="w", encoding="utf-8") as file:
            file.write(message.text)
    elif user_id == 5726620258:
        with open("Shishenco_Denis/text_reply.txt", mode="w", encoding="utf-8") as file:
            file.write(message.text)
    await message.answer("✅Автоответ включен")


@dp.callback_query(FilterDown())
async def add_cmd(callback: CallbackQuery, state: FSMContext):
    await database.del_autoreply(int(f"{callback.data}"[1::]))
    await callback.message.edit_text("Выбери сотрудника для кого мне <b>включить</b> автоответ⬇️",
                                     reply_markup=await kb.select_all_autoreply_kb_no(), parse_mode="HTML")


async def main():
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("EXIT")
