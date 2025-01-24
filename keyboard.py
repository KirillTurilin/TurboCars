from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config

import database

kb_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🟢Включить", callback_data="goup"),
                                                 InlineKeyboardButton(text="🔴Выключить", callback_data="godown")]])


async def select_all_autoreply_kb():
    try:
        idis = await database.select_all_autoreply()
        lst = []
        data = (config.names).copy()
        print(idis)
        for i in idis:
            if i[0] in config.names:
                data.pop(i[0])
        for i in data:
            print(i, f"⏺️{config.names[i]}")
            print(10)
            btn = [InlineKeyboardButton(text=f"⏺️{config.names[i]}", callback_data=f"{i}")]
            lst.append(btn)
        lst.append([InlineKeyboardButton(text=f"↩️назад", callback_data="exit")])
    except Exception as ex:
        print(ex)
    return InlineKeyboardMarkup(inline_keyboard=lst)


async def select_all_autoreply_kb_no():
    data = await database.select_all_autoreply()
    print(data)
    lst = []
    if not data:
        print(2)
        lst.append([InlineKeyboardButton(text=f"↩️назад", callback_data="exit")])
        return InlineKeyboardMarkup(inline_keyboard=lst)
    for i in data:
        print(type(i[0]))
        print(i, f"⏺️{config.names}")
        btn = [InlineKeyboardButton(text=f"✅{config.names[int(i[0])]}", callback_data=f"n{i[0]}")]
        if btn in lst:
            continue
        lst.append(btn)
    lst.append([InlineKeyboardButton(text=f"↩️назад", callback_data="exit")])
    return InlineKeyboardMarkup(inline_keyboard=lst)


kb_up = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🟢Включить", callback_data="yes")],
                                                [InlineKeyboardButton(text="Изменить текст авто-ответа", callback_data="rename")],
                                                [InlineKeyboardButton(text=f"↩️назад", callback_data="exit")]])


print(config.names[5726620258])