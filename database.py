import os
import sqlite3

# Используем абсолютный путь к файлу базы данных — тогда поведение не будет
# зависеть от того, из какой папки запускают скрипт.
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'bot.db')

connection = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = connection.cursor()


def init_db():
    """Создаёт необходимые таблицы, если их ещё нет. Безопасно вызывать многократно."""
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        chat_id BIGINT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS translation(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lang_from TEXT,
        lang_to TEXT,
        original_text TEXT,
        translated_text TEXT,
        user_id INTEGER REFERENCES users(id)
    );
    """)
    connection.commit()


# Инициализируем базу при импорте модуля
init_db()
def is_user_exists(chat_id):
    sql = 'SELECT id FROM users WHERE chat_id=?'
    cursor.execute(sql, (chat_id,))
    user_id = cursor.fetchone()
    return user_id is not None



def add_user(first_name, chat_id):
    sql = 'INSERT INTO users(first_name, chat_id) VALUES (?, ?)'
    if not is_user_exists(chat_id):
        cursor.execute(sql, (first_name, chat_id))
        connection.commit()


def add_trans(lang_from, lang_to, original_text, translated_text, chat_id):
    sql1 = 'SELECT id FROM users WHERE chat_id=?'
    cursor.execute(sql1, (chat_id,))
    row = cursor.fetchone()
    if not row:
        # Пользователь не найден — не падаем, возвращаем False
        return False
    user_id = row[0]
    sql = 'INSERT INTO translation(lang_from, lang_to, original_text,  translated_text, user_id ) VALUES (?, ?, ?, ?, ?)'
    cursor.execute(sql, (lang_from, lang_to, original_text, translated_text, user_id))
    connection.commit()
    return True

def add_hist(chat_id):
    sql1 = 'SELECT id FROM users WHERE chat_id=?'
    cursor.execute(sql1, (chat_id,))
    row = cursor.fetchone()
    if not row:
        return []
    user_id = row[0]
    sql = 'SELECT * FROM translation WHERE user_id=?'
    cursor.execute(sql, (user_id,))
    hist = cursor.fetchall()
    return hist




connection.commit()
