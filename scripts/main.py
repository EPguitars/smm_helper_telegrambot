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

from keyboards import main_kb, categories_kb, get_cancel
from dboperations import add_category, get_categories


load_dotenv()
colorama.init(autoreset=True)

TOKEN = os.getenv("TG_BOT_TOKEN")
storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot,
                storage=storage)


class States(StatesGroup):
    navigation = State()
    inputing = State()


async def on_startup(_):
    print(f"{Fore.GREEN}{Style.BRIGHT}BOT HAS BEEN STARTED!")

@dp.message_handler(commands=['cancel'])
async def cancel_command(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await bot.send_message(chat_id=message.from_user.id,
                           text='Вы отменили',
                           reply_markup=main_kb)
    await message.delete()
    await state.finish()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Welcome',
                           reply_markup=main_kb)
    await message.delete()


@dp.message_handler(Text(equals="Категории"))
async def categories_menu(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Меню категорий",
                           reply_markup=categories_kb)
    await message.delete()


@dp.message_handler(Text(equals="Добавить\nкатегорию"), state=None)
async def new_category(message: types.Message) -> None:
    await States.inputing.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите название категории...",
                           reply_markup=get_cancel())


@dp.message_handler(lambda message: message.text, state=States.inputing)
async def add_category_command(message: types.Message, state: FSMContext):
    add_category(message.text)

    await state.finish()
    await message.reply("Категория добавлена!",
                        reply_markup=categories_kb)
    
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


if __name__ == '__main__':
    executor.start_polling(dp, 
                           skip_updates=True, 
                           on_startup=on_startup)