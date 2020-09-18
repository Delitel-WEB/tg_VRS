# Created by Delitel

import sqlite3
import time


class SQLither:

	def __init__(self, database):
		self.conn = sqlite3.connect(database)
		self.c = self.conn.cursor()

		self.c.execute('''CREATE TABLE IF NOT EXISTS PC_STARTS
			(id INTEGER PRIMARY KEY AUTOINCREMENT, time TEXT)''')
		self.c.execute('''CREATE TABLE IF NOT EXISTS deletions_messages
			(id INTEGER PRIMARY KEY AUTOINCREMENT, message_id INTEGER)''')
		self.c.execute('''CREATE TABLE IF NOT EXISTS users
				(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, status TEXT)''')
		self.c.execute('''CREATE TABLE IF NOT EXISTS temporary_download_file_data
			(user_id INTEGER, link TEXT, file_path TEXT)''')

		if not bool(self.c.execute("SELECT * FROM PC_STARTS").fetchone()):
			self.c.execute("INSERT INTO PC_STARTS ('time') VALUES(?)", (time.time(),))
			self.conn.commit()

	def add_message_id(self, message_id):
		self.c.execute("INSERT INTO deletions_messages ('message_id') VALUES(?)", (message_id,))
		self.conn.commit()

	def get_deletions_messages(self):
		res = self.c.execute("SELECT * FROM deletions_messages").fetchall()
		return res

	def delete_deletions_message(self, message_id):
		self.c.execute("DELETE FROM deletions_messages WHERE message_id=?", (message_id,))
		self.conn.commit()

	def exists_user(self, user_id):
		return bool(self.c.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone())

	def add_user(self, user_id):
		self.c.execute("INSERT INTO users ('user_id', 'status') VALUES(?,?)", (user_id, 0,))
		self.conn.commit()

	def get_status(self, user_id):
		return self.c.execute("SELECT status FROM users WHERE user_id=?", (user_id,)).fetchone()[0]

	def set_status(self, user_id, status):
		self.c.execute("UPDATE users SET status=? WHERE user_id=?", (status, user_id,))
		self.conn.commit()

	def delete_all_temporary_download_file_data(self, user_id):
		self.c.execute("DELETE FROM temporary_download_file_data WHERE user_id=?", (user_id,))
		self.conn.commit()

	def add_link_to_temporary_download_file_data(self, user_id, link):
		self.c.execute("INSERT INTO temporary_download_file_data ('user_id', 'link') VALUES(?,?)", (user_id,link,))
		self.conn.commit()

	def add_file_path_to_temporary_download_file_data(self, user_id, file_path):
		self.c.execute("UPDATE temporary_download_file_data SET file_path=? WHERE user_id=?", (file_path, user_id,))
		self.conn.commit()

	def get_temporary_download_file_data(self, user_id):
		link = self.c.execute("SELECT link FROM temporary_download_file_data WHERE user_id=?", (user_id,)).fetchone()[0]
		file_path = self.c.execute("SELECT file_path FROM temporary_download_file_data WHERE user_id=?", (user_id,)).fetchone()[0]
		return link, file_path



class bat:

	def __init__(self, database):
		self.conn = sqlite3.connect(database)
		self.c = self.conn.cursor()

		self.c.execute('''CREATE TABLE IF NOT EXISTS temporary_bat_fiiles
				(id INTEGER PRIMARY KEY AUTOINCREMENT, name_file TEXT)''')


	def get_bat_files(self):
		return self.c.execute("SELECT * FROM temporary_bat_fiiles").fetchone()

	def add_bat_file(self, file):
		self.c.execute("INSERT INTO temporary_bat_fiiles ('name_file') VALUES(?)", (file,))
		self.conn.commit()

	def delete_bat_file(self, file):
		self.c.execute("DELETE FROM temporary_bat_fiiles WHERE name_file=?", (file,))
		self.conn.commit()

	def get_all_bat_files(self):
		return self.c.execute("SELECT * FROM temporary_bat_fiiles").fetchall()
		




