from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

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