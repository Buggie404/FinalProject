import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('LibraryManagementApp/Database/library.db')
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()