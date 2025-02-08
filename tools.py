import json
import sqlite3


def start():
    try:
        open('config.json', 'r')
    except:
        with open('config.json', 'w') as f:
            json.dump({
                'bot_token': 'token',
                'payment_token': 'token',
                'admin_username': '@telegram'
            }, f)
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    
    cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
chat_id INTEGER NOT NULL,
username TEXT NOT NULL,
balance INTEGER
)
''')


def create_user(chat_id:int, username:str, balance:int=0):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT chat_id FROM Users WHERE chat_id = {chat_id}')
    is_user = cursor.fetchone()
    if is_user == None:
        cursor.execute('INSERT INTO Users (chat_id, username, balance) VALUES (?, ?, ?)', (chat_id, username, balance))
    connection.commit()
    connection.close()


def get_user_info(info:str, chat_id:int=0, username:str=''):
    if chat_id != 0:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(f'SELECT {info} FROM Users WHERE chat_id = {chat_id}')
        ans = cursor.fetchone()[0]
        connection.commit()
        connection.close()
    
    
def get_data_json(key:str):
    with open('config.json', 'r') as f:
        return json.load(f)[key]


start()