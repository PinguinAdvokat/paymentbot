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
username TEXT NOT NULL
)
''')
    
    
def get_data_json(key:str):
    with open('config.json', 'r') as f:
        return json.load(f)[key]


start()