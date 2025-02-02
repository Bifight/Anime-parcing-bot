from  aiogram.types import  ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from  aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.requests import get_categories, get_categorise_in_items, search_item, get_favorites

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="catalog")],
                                     [KeyboardButton(text="update"), KeyboardButton(text="favorite")],
                                     ],resize_keyboard=True)




async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name_week, callback_data=f"day_{category.name_week}"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="to_main0"))
    return keyboard.adjust(2).as_markup()


async def items(day_week):
    all_items = await get_categorise_in_items(day_week)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"anime_{item.id}"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="to_main1"))
    keyboard.add(InlineKeyboardButton(text="Показать все", callback_data=f"all_{day_week}"))
    return keyboard.adjust(2).as_markup()

async def item(anime_id):
    anme = await search_item(anime_id)
    day = anme.category_day
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=f"to_main2{day}"))
    keyboard.add(InlineKeyboardButton(text="Добавить в избранные", callback_data=f"addfavorite_{anime_id}"))
    keyboard.add(InlineKeyboardButton(text="Удалить из избранного", callback_data=f"deletefavorite_{anime_id}"))
    return keyboard.adjust(2).as_markup()

async def favorite_user(user_id : int):
    favorites = await get_favorites(user_id)
    keyboard = InlineKeyboardBuilder()
    for item in favorites:
        keyboard.add(InlineKeyboardButton(text=f'{item.name}', callback_data=f"anime_{item.id}"))
    return keyboard.adjust(2).as_markup()
    