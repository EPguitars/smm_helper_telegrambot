from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from dboperations import get_categories

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text="Категории")
b2 = KeyboardButton(text="Статистика") 
main_kb.add(b1, b2)

categories_kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text="Список категорий")
b2 = KeyboardButton(text="Добавить\nкатегорию")
b3 = KeyboardButton(text="Удалить\nкатегорию")
b4 = KeyboardButton(text="Главное меню")
categories_kb.add(b1).add(b2, b3).add(b4)


def get_cancel() -> ReplyKeyboardMarkup:
    cancel = KeyboardButton('/cancel')
    return ReplyKeyboardMarkup(resize_keyboard=True).add(cancel)


def get_delete_categories() -> InlineKeyboardMarkup:
    delete_categories = InlineKeyboardMarkup(row_width=1)
    categories = get_categories()

    for category in categories:
        delete_categories.add(InlineKeyboardButton(text=category, callback_data=category))

    cancel = InlineKeyboardButton(text="Отмена", callback_data='cancel')
    delete_categories.add(cancel)
    
    return delete_categories 