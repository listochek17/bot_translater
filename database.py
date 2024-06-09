import sqlite3

connection = sqlite3.connect('bot.db', check_same_thread=False)

cursor = connection.cursor()


# bot_table_sql = """
# DROP TABLE IF EXISTS users;
# CREATE TABLE IF NOT EXISTS users(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     first_name TEXT,
#     chat_id BIGINT
# );
#
# """
#
# bot_table2_sql = """
# DROP TABLE IF EXISTS translation;
# CREATE TABLE IF NOT EXISTS translation(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     lang_from TEXT,
#     lang_to TEXT,
#     original_text TEXT,
#     translated_text TEXT,
#     user_id  INT REFERENCES users(id)
# );
#
# """
# cursor.executescript(bot_table2_sql)
def is_user_exists(chat_id):
    sql = 'SELECT id FROM users WHERE chat_id=?'
    cursor.execute(sql, (chat_id,))
    user_id = cursor.fetchone()
    if not user_id:
        return False
    return True



def add_user(first_name, chat_id):
    sql = 'INSERT INTO users(first_name, chat_id) VALUES (?, ?)'
    if not is_user_exists(chat_id):
        cursor.execute(sql, (first_name, chat_id))
        connection.commit()


def add_trans(lang_from, lang_to, original_text, translated_text, chat_id):
    sql1 = 'SELECT id FROM users WHERE chat_id=?'
    cursor.execute(sql1, (chat_id,))
    user_id = cursor.fetchone()[0]
    sql = 'INSERT INTO translation(lang_from, lang_to, original_text,  translated_text, user_id ) VALUES (?, ?, ?, ?, ?)'
    cursor.execute(sql, (lang_from, lang_to, original_text, translated_text, user_id))
    connection.commit()

def add_hist(chat_id):
    sql1 = 'SELECT id FROM users WHERE chat_id=?'
    cursor.execute(sql1, (chat_id,))
    user_id = cursor.fetchone()[0]
    sql = 'SELECT * FROM translation WHERE user_id=?'
    cursor.execute(sql, (user_id,))
    hist = cursor.fetchall()
    return hist




connection.commit()
