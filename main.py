import asyncio
import logging
import sys
import subprocess

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from functions import *
from config import TOKEN, ADMINS

# Диспетчер для хендлеров
dp = Dispatcher()


@dp.message(Command(commands=['memory']), F.from_user.id.in_(ADMINS))
async def memory_handler(message: Message) -> None:
    """
    Отправляет информацию о потреблении ОЗУ
    """
    memory = memory_usage()
    await message.answer(str(memory))


@dp.message(Command(commands=['cpu']), F.from_user.id.in_(ADMINS))
async def cpu_handler(message: Message) -> None:
    """
    Отправляет информацию о потреблении процессора
    """
    cpu = cpu_usage()
    await message.answer(f"Потребление процессора: {cpu}%")


@dp.message(Command(commands=['localhost']), F.from_user.id.in_(ADMINS))
async def localhost_handler(message: Message) -> None:
    """
    Отправляет информацию о лоакльном хосте
    """
    localhost = get_localhost()
    await message.answer(f"Локальный хост: {localhost}")


@dp.message(Command(commands=['disk']), F.from_user.id.in_(ADMINS))
async def disk_handler(message: Message, command: CommandObject) -> None:
    """
    Отправляет информацию о потреблении памяти диска
    """
    if not command.args:
        await message.answer("Пожалуйста укажите путь которую хотите проверить")
        return
    
    route = command.args
    disk = disk_usage(route)
    await message.answer(str(disk))


@dp.message(Command(commands=['run']), F.from_user.id.in_(ADMINS))
async def run_handler(message: Message, command: CommandObject) -> None:
    """
    Запускает команды от пользователя
    """
    if not command.args:
        await message.answer("Пожалуйста укажите команду для запуска")
        return

    answer = subprocess.check_output(command.args.split(" "), text=True)
    try:
        await message.answer(f"Ответ:\n{answer}", parse_mode=None)
    except Exception as e:
        await message.answer(f"Ошибка:\n{e}")


@dp.message()
async def help_handler(message: Message) -> None:
    """
    Хендлер для прочего
    """
    if message.from_user.id in ADMINS:
        await message.answer(
            f"Привет {html.bold(message.from_user.full_name)}!\n"\
            "Я помогу следить за статистикой нагруженности твоего сервера, а так же буду уведомлять если ресурсов остается мало\n\n"\
            "Существуют следующие команды:\n"\
            "/cpu - информация о потреблении процессора\n"\
            "/memory - информатия о потреблении памяти ОЗУ\n"\
            "/disk (путь) - информатия о потреблении памяти диска по указанному пути\n"\
            "/localhost - проверка IP адреса локального хоста\n"\
            "/run (команда) - запуск указанной команды"
            )
    else:
        await message.answer("Не доступно для вас!")


async def main() -> None:
    # Инициализация объекта бота с настройками по умолчанию
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Начать планировку задач
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_system, 'interval', args=[bot], seconds=60)
    scheduler.start()

    # Запуск обработки событий
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())