import sqlite3
from application import app
from datetime import date
from application.functions.util import create_salt, hash_password, create_random_userid

def create_user(userid, username, password_hash, salt, name):
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Users(userId, username, password, salt, name) VALUES(?, ?, ?, ?, ?)", (userid, username, password_hash, salt, name))
    except sqlite3.IntegrityError as e:
        raise sqlite3.IntegrityError
    finally:
        conn.commit()
        cur.close()

def get_userid_from_username(username):
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()
    userid = cur.execute("SELECT userid from Users where username = ?", (username,)).fetchone()[0]
    conn.commit()
    cur.close()
    return userid

def get_name_from_userid(userid):
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()
    name = cur.execute("SELECT name from Users WHERE userId = ?", (userid,)).fetchone()
    cur.close()
    conn.commit()
    return name

def create_account(initial_balance, userid):
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO Accounts(currentBalance, userId) VALUES(?, ?)", (initial_balance, userid))
    conn.commit()
    cur.close()


def create_db():
    app.logger.debug("Initiate DB creation")
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Users")
    cur.execute("DROP TABLE IF EXISTS Accounts")
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute("CREATE TABLE IF NOT EXISTS Users(userId TEXT PRIMARY KEY, username TEXT UNIQUE, password TEXT, salt TEXT, name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Accounts(accountId INTEGER PRIMARY KEY AUTOINCREMENT, currentBalance REAL, userId TEXT, FOREIGN KEY(userId) REFERENCES Users(userId))")
    #insert an initial new user 
    userid = create_random_userid()
    password1 = '012345'
    salt1 = create_salt()
    password_hash = hash_password(password1,salt1)
    cur.execute('INSERT INTO Users(userId, username, password, salt, name) VALUES(?, ?, ?, ?, ?)', (userid, 'testuser', password_hash, salt1, 'testname'))
    # insert an account for intial user
    cur.execute('INSERT INTO Accounts(currentBalance, userId) VALUES(?, ?)', (5000, userid))

    conn.commit()
    cur.close()
    app.logger.debug("DB Created")


