import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, executor
import colorama
from colorama import Fore, Style
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from keyboards import main_kb, categories_kb, get_cancel, get_delete_categories
from dboperations import add_category, get_categories, delete_category


load_dotenv()
colorama.init(autoreset=True)

TOKEN = os.getenv("TG_BOT_TOKEN")
storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot,
                storage=storage)

cb = CallbackData('delete_categories', 'action')

class States(StatesGroup):
    navigation = State()
    inputing = State()
    del_category = State()


""" Действия при запуске """
async def on_startup(_):
    print(f"{Fore.GREEN}{Style.BRIGHT}BOT HAS BEEN STARTED!")


""" Кнопка отмены (сброс состояний) """
@dp.message_handler(commands=['cancel'], state=States.inputing)
async def cancel_command(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await bot.send_message(chat_id=message.from_user.id,
                           text='Вы отменили',
                           reply_markup=main_kb)
    await message.delete()
    await state.finish()


""" Обработчик команды старт """
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Welcome',
                           reply_markup=main_kb)
    await message.delete()



""" Переход в меню "Категории" """
@dp.message_handler(Text(equals="Категории"))
async def categories_menu(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Меню категорий",
                           reply_markup=categories_kb)
    await message.delete()
    



""" Начать добавление категории (изменение состояния) """
@dp.message_handler(Text(equals="Добавить\nкатегорию"), state=None)
async def new_category(message: types.Message) -> None:
    await States.inputing.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите название категории...",
                           reply_markup=get_cancel())


""" Завершение добавления категории """
@dp.message_handler(lambda message: message.text, state=States.inputing)
async def add_category_command(message: types.Message, state: FSMContext):
    add_category(message.text)

    await state.finish()
    await message.reply("Категория добавлена!",
                        reply_markup=categories_kb)
    

""" Получение списка категорий """
@dp.message_handler(Text(equals="Список категорий"))
async def print_categories(message: types.Message):
    await message.delete()
    inline_categories = InlineKeyboardMarkup(row_width=1)
    categories = get_categories()

    for category in categories:
        
        inline_categories.add(InlineKeyboardButton(text=category, callback_data=category))

    await bot.send_message(chat_id=message.from_user.id,
                           text='Ваши категории',
                           reply_markup=inline_categories)



""" Начать удаление категории """
@dp.message_handler(Text(equals='Удалить\nкатегорию'), state=None)
async def delete_cat(message:types.Message):
    await States.del_category.set()
    await message.delete()
   

    await bot.send_message(chat_id=message.from_user.id,
                            text='Выберите категорию для удаления',
                            reply_markup=get_delete_categories())   

""" Выбор категории для удаления"""
@dp.callback_query_handler(state=States.del_category)
async def accept_deleting(callback: types.CallbackQuery, state=FSMContext) -> None:
    request = callback.data
    if request == 'cancel':
        await bot.send_message(chat_id=callback.message.chat.id,
                           text='Вы отменили',
                           reply_markup=main_kb)
        await state.finish()    
    
    else:    
        delete_category(request)

        await bot.send_message(chat_id=callback.message.chat.id,
                                text="Категория удалена",
                                reply_markup=categories_kb)
        await state.finish()
    

if __name__ == '__main__':
    executor.start_polling(dp, 
                           skip_updates=True, 
                           on_startup=on_startup)