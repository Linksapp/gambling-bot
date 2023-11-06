import sqlite3
from admin import check_privilege

def create(message):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id   
    # id = message
    balance, isadmin = check_privilege(id)
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        name tinytext,
        surname tinytext,
        chatid integer,
        balance float,
        lent_cash integer,
        isadmin bit
    )""")
    cur.execute("INSERT INTO users(name, surname, chatid, balance, isadmin) SELECT 0, 0, ?, ?, ? WHERE NOT EXISTS (SELECT chatid FROM users WHERE chatid = ?)" , (id, balance, isadmin, id))
    cur.execute("SELECT * FROM users")
    data.commit()
    data.close()

def get_info(message):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id
    info = list(cur.execute("SELECT * FROM users where chatid = ?", (id,)))[0]
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

def get_names(message):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id
    cur.execute("SELECT name, surname FROM users WHERE chatid != ?", (id,))
    ls = cur.fetchall()
    print(ls)
    data.commit()
    data.close()
    return ls

def check_wealth(message):
    try:
        cash = int(message.text)
        if cash <= 0: raise ValueError
        data = sqlite3.connect('baseddata.db')
        cur = data.cursor()
        id = message.chat.id
        cur.execute("SELECT balance FROM users WHERE chatid = ?", (id,))
        balance = cur.fetchone()[0]
        if balance - cash * 1.03 >= 0:
            data.commit()
            data.close()
            return 1
        else:
            data.commit()
            data.close()
            return -1
    except ValueError:
        return 0

def withdraw_money(message, id):
    cash = int(message.text) 
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    cur.execute("SELECT balance FROM users WHERE chatid = ?", (message.chat.id,))
    balance = cur.fetchone()[0]
    cur.execute("UPDATE users SET balance = ? WHERE chatid = ?", (balance - cash * 1.03, message.chat.id,))

    cur.execute("SELECT balance FROM users WHERE chatid = ?", (id,))
    balance = cur.fetchone()[0]
    cur.execute("UPDATE users SET balance = ? WHERE chatid = ?", (balance + cash, id,))
    data.commit()
    data.close()


def get_chat_id(message):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    name, surname = message[0], message[1]
    cur.execute("SELECT chatid FROM users where name = ? AND surname = ?", (name, surname,))
    id = cur.fetchone()[0]
    data.commit()
    data.close()
    return id

def getleaderboard():
    maxpositions = 8
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    cur.execute("SELECT surname, name FROM users WHERE isadmin = 0 ORDER BY balance DESC")
    ls = cur.fetchmany(maxpositions)
    leaderboard = ''
    try:
        leaderboard += '1. 🥇 ' + str(ls[0][1]) + '\n'
        leaderboard += '2. 🥈 ' + str(ls[1][1]) + '\n'
        leaderboard += '3. 🥉 ' + str(ls[2][1])+ '\n'
        count = 3
        for i in range(3, maxpositions):
            count+=1
            leaderboard += str(count) +'. ' + str(ls[i][1]) + '\n'
    except IndexError:
        pass
    data.commit()
    data.close()
    return leaderboard
    
if __name__ == '__main__':
    print(getleaderboard())