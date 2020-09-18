# Created by Delitel

from aiogram import types

main_keyboard = types.InlineKeyboardMarkup()
main_keyboard_1 = types.InlineKeyboardButton(text = "Сделать скриншот 📺", callback_data = "make_screen")
main_keyboard_2 = types.InlineKeyboardButton(text = "Открыть сайт 🌐", callback_data = "open_browser")
main_keyboard_3 = types.InlineKeyboardButton(text = "Скачать файл 📄", callback_data = "download_file")
main_keyboard_4 = types.InlineKeyboardButton(text = "Открыть 📂", callback_data = "open_file")
main_keyboard_5 = types.InlineKeyboardButton(text = "Добавить сценарий 🖼", callback_data = "add_scene")
main_keyboard_6 = types.InlineKeyboardButton(text = "Проверка ip 🍭", callback_data = "check_ip")
main_keyboard_7 = types.InlineKeyboardButton(text = "Список процессов 📃", callback_data = "list_proccess")
main_keyboard_8 = types.InlineKeyboardButton(text = "Обновление 🔄", callback_data="update_")
main_keyboard.add(main_keyboard_1)
main_keyboard.add(main_keyboard_2, main_keyboard_3)
main_keyboard.add(main_keyboard_5, main_keyboard_6, main_keyboard_7)

cancel_keyboard = types.InlineKeyboardMarkup()
cancel_keyboard.add(types.InlineKeyboardButton(text= "Отмена ❌", callback_data = "cancel"))

use_file_path = types.InlineKeyboardMarkup()
use_file_path_1 = types.InlineKeyboardButton(text = "Да", callback_data="use_file_path")
use_file_path_2 = types.InlineKeyboardButton(text = "Нет", callback_data="no_use_file_path")
use_file_path.add(use_file_path_1, use_file_path_2)