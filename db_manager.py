import sqlite3
from admin import check_privilege

def create(message):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id   
    balance = check_privilege(id)
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        name tinytext,
        surname tinytext,
        chatid integer,
        balance integer,
        lent_cash integer,
        winrate float
    )""")
    cur.execute("INSERT INTO users(name, surname, chatid, balance, lent_cash, winrate) SELECT 0, 0, ?, ?, 0, 0 WHERE NOT EXISTS (SELECT chatid FROM users WHERE chatid = ?)" , (id, balance, id))
    cur.execute("SELECT * FROM users")
    print(cur.fetchall())
    data.commit()
    data.close()

def get_info(message):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id
    info = list(cur.execute("SELECT * FROM users where chatid = ?", (id,)))[0]
    print(info)
    data.commit()
    data.close()
    return info

def addnametodb(message, name):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id
    cur.execute("UPDATE users SET name = ? WHERE chatid = ?", (name, id))  
    data.commit()
    data.close()

def addsurnametodb(message, surname):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id
    cur.execute("UPDATE users SET surname = ? WHERE chatid = ?", (surname, id))  
    data.commit()
    data.close()
# def getleaderboard():
#     data = sqlite3.connect('baseddata.db')
#     cur = data.cursor()
#     cur.execute("SELECT surname, name FROM users ORDER BY balance DESC")