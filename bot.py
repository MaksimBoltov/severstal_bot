import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import tg_api_settings
from crud import get_counterparty
from database import Base, engine
from models import Counterparties
from services import valid_counterparty
from write_counterparty_info import generate_counterparty_report

API_TOKEN = tg_api_settings.api_token

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
Base.metadata.create_all(bind=engine)

menu_message = """
Бот для работы с контрагентами
Вызвать подсказку: /help
Получение информации по контрагенту: /info
"""


class Form(StatesGroup):
    number = State()


@dp.message_handler(commands=['start', 'help'])
async def send_menu(message: types.Message):
    """Функция вызывается когда пользователь ввел `/start` или `/help` и
    передает пользователю список доступных команд.
    """
    await message.answer(menu_message)


@dp.message_handler(commands=['info'])
async def counterparty_info(message: types.Message):
    """Функция вызывается при вводе '/info' и предлагает
    пользователю ввести номер контрагента для получения инфомрации по нему.
    """
    await message.answer("Для получения информации по контрагенту введите его номер")
    await Form.number.set()


@dp.message_handler(
    lambda message: not message.text.isdigit() or not valid_counterparty(int(message.text)),
    state=Form.number
)
async def counterparty_number_invalid(message: types.Message):
    """Вызывается если номер контрагента был введен некорректный или контрагента не существует."""
    if not message.text.isdigit():
        return await message.answer("Введен неверный номер.\nВведите номер повторно (число)")
    return await message.answer(f"Контрагент с номером {message.text} не найден\n"
                                f"Введите номер повторно")


@dp.message_handler(state=Form.number)
async def send_counterparty_info(message: types.Message, state: FSMContext):
    """Отправляет пользователю информацию по контрагенту в виде pdf файла."""

    async with state.proxy():
        number = int(message.text)
        counterparty = get_counterparty(number)
        report_path = generate_counterparty_report(counterparty)
        with open(report_path, 'rb') as file:
            await message.answer_document(file, caption=f'Информация по контрагенту "{counterparty.name}"')

        os.remove(report_path)

    await state.finish()


@dp.message_handler()
async def another_commands(message: types.Message):
    """Обрабатывает любые не предусмотренные сообщения пользователя и
    выдет ему меню из доступных команд.
    """
    await message.answer("Не могу понять введенную команду." + menu_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
