# Created by Delitel

import pyautogui
from random import choice
import webbrowser
import requests
import wget
import os


def make_screenshot(): # Сделать скриншот
	login = os.getlogin()
	name_file = f"C:\\Users\\{login}\\AppData\\Roaming\\systemAdapter\\screenshotes"
	for i in range(20):
		name_file += choice("1234567890QWERTYUIOPASDFGHJKLZXZCVBNMqwertyuiiopasdfghjklzxcvbnm")
	name_file += ".png"
	pyautogui.screenshot(name_file)
	return name_file


def open_site(site): # Открыть сайт в браузере
	webbrowser.open(site)


def get_ip(): # Получить ip
	ip = requests.get("https://ramziv.com/ip").text
	return ip

def download_file(link ,file_path=None): # Скачать файл
	login = os.getlogin()
	if file_path:
		wget.download(link, file_path)
	else:
		wget.download(link[0], f"C:\\Users\\{login}\\Downloads")


def open_dir(dirs):
	os.system(f"start {dirs}")


