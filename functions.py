import socket
import shutil
import psutil
from aiogram import Bot

from objects import Usage
from config import ADMINS

def check_localhost() -> bool:
    """Проверяет локальный хост"""
    localhost = socket.gethostbyname('localhost')
    return localhost== "127.0.0.1"

def check_disk_usage(disk) -> bool:
    """Проверяет, свободно ли 20% памяти диска"""
    du = shutil.disk_usage(disk)
    free = du.free / du.total * 100
    return free > 20

def check_memory_usage() -> bool:
    """Проверяет, свободно ли 500 МБ в ОЗУ"""
    mu = psutil.virtual_memory().available
    total = mu / (1024.0 ** 2)
    return total > 500

def check_cpu_usage() -> bool:
    """Проверяет нагруженность процессора, что был менее 80%"""
    usage = psutil.cpu_percent(1)
    return usage < 80

async def check_system(bot: Bot) -> None:
    """Проверяет систему и отправляет сообщение администраторам"""
    text = ""
    if not check_cpu_usage() :
        text += "Процессор нагружен на более чем 80%"

    if not check_memory_usage():
        text += "\nСвободная память в ОЗУ меньше 500 МБ"

    if not check_disk_usage('/home/dilmurod') :
        text += "\nМесто в памяти диска меньше 20%"

    if not check_localhost():
        text += "\nЛокальный хост не обнаружен на 127.0.0.1"
    
    if text == "":
        return
    
    for i in ADMINS:
        await bot.send_message(i, text)

def get_localhost() -> str:
    """
    Возвращает IP адрес локального хоста
    """
    localhost = socket.gethostbyname('localhost')
    return localhost

def disk_usage(disk) -> Usage:
    """
    Возвращает объект Usage с МБ и % памяти диска
    """
    values = shutil.disk_usage(disk)
    available = values.free / (1024*1024)
    used = values.used / (1024*1024)
    total = values.total / (1024*1024)
    
    available_percent = available / total * 100
    used_percent = used / total * 100
    return Usage(f"Диск по пути \"{disk}\"", available, used, total, available_percent, used_percent)

def memory_usage() -> Usage:
    """
    Возвращает объект Usage с МБ и % памяти ОЗУ
    """
    values = psutil.virtual_memory()
    available = values.available >> 20
    used = values.used >> 20
    total = values.total >> 20
    
    available_percent = available / total * 100
    used_percent = used / total * 100
    return Usage("ОЗУ", available, used, total, available_percent, used_percent)

def cpu_usage() -> float:
    """
    Возвращает % нагруженности процессора
    """
    usage = psutil.cpu_percent(1)
    return usage