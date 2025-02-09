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
    try:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(f'SELECT chat_id FROM Users WHERE chat_id = {chat_id}')
        is_user = cursor.fetchone()
        if is_user == None:
            cursor.execute('INSERT INTO Users (chat_id, username, balance) VALUES (?, ?, ?)', (chat_id, username, balance))
        connection.commit()
        connection.close()
        return True
    except sqlite3.Error:
        return False


def is_user_in_database(username:str='', chat_id:int=0):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    if username != '':
        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM Users WHERE username = {username} LIMIT 1);")
    else:
        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM Users WHERE chat_id = {chat_id} LIMIT 1);")
        conn.close()
        return False
    result = cursor.fetchone()[0]
    print(result)
    conn.close()
    return bool(result)



def get_user_info(chat_id:int, info:str, username:str=''):
    try:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        if username == '':
            cursor.execute(f'SELECT {info} FROM Users WHERE chat_id = {chat_id}')
        else:
            cursor.execute(f'SELECT {info} FROM Users WHERE username = {username}')
        ans = cursor.fetchone()[0]
        connection.commit()
        connection.close()
        return ans
    except sqlite3.Error:
        return False


def add_balance(chat_id:int, summ:int):
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute(f'UPDATE Users SET balance = balance + {summ} WHERE chat_id = {chat_id}')
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error:
        return False
    
    
def get_data_json(key:str):
    with open('config.json', 'r') as f:
        return json.load(f)[key]


start()