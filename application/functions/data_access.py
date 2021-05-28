import sqlite3
from application import app
from datetime import date
from application.functions.util import create_salt, hash_password, create_random_userid


def create_db():
    app.logger.debug("Initiate DB creation")
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Users")
    cur.execute("DROP TABLE IF EXISTS Accounts")
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute("CREATE TABLE IF NOT EXISTS Users(userId TEXT PRIMARY KEY, username TEXT UNIQUE, password TEXT, salt TEXT, name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Accounts(accountId INTEGER PRIMARY KEY AUTOINCREMENT, currentBalance REAL, userId TEXT, FOREIGN KEY(userId) REFERENCES Users(userId))")

    conn.commit()
    cur.close()
    app.logger.debug("DB Created")

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

def create_account(initial_balance, userid):
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO Accounts(currentBalance, userId) VALUES(?, ?)", (initial_balance, userid))
    conn.commit()
    cur.close()

def get_user_authentication_info(username):
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()
    result = cur.execute("select userId, password, salt from Users where username= ?", (username,)).fetchone()
    conn.close()
    return result

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
    conn.commit()
    cur.close()
    return name

def get_currentBalance_from_userid(userid):
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()
    balance = cur.execute("select currentBalance from Accounts where userId= ? ",[userid]).fetchone()
    return balance

def deposit_and_update(new_deposit, userid):
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()
    cur.execute("update Accounts set currentBalance = currentBalance + ? where userId= ? ", [float(new_deposit), userid])
    conn.commit()
    conn.close()

def withdraw_and_update(new_withdraw, userid):
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()
    cur.execute("update Accounts set currentBalance = currentBalance - ? where userId= ? ", [float(new_withdraw), userid])
    conn.commit()
    conn.close()