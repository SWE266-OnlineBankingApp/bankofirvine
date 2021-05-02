import sqlite3
from datetime import date

conn = sqlite3.connect('bankdata.db')
cur = conn.cursor()
# drop tables if exist before to recreate tables
cur.execute("DROP TABLE IF EXISTS Users")
#cur.execute("DROP TABLE IF EXISTS Login")
cur.execute("DROP TABLE IF EXISTS Account")
#cur.execute("DROP TABLE IF EXISTS Savings_accounts")
#cur.execute("DROP TABLE IF EXISTS Transactions")

#cur.execute("CREATE TABLE IF NOT EXISTS Login(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, email TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, email TEXT, name TEXT, AccountNo UNIQUE INTEGER, address TEXT )")
cur.execute("CREATE TABLE IF NOT EXISTS Accounts(id INTEGER PRIMARY KEY AUTOINCREMENT, AccountNo INTEGER UNIQUE REFERENCES User(AccountNo), currentBalance REAL)")
#cur.execute("CREATE TABLE IF NOT EXISTS Savings_accounts(id INTEGER PRIMARY KEY AUTOINCREMENT, savingsAccountNo INTEGER REFERENCES User(savingsAccountNo), currentBalance REAL, routingNo INTEGER)")
#cur.execute("CREATE TABLE IF NOT EXISTS Transactions(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, time TEXT,  amount REAL, senderAccountNo INTEGER, senderRoutingNo INTEGER, senderAccountType TEXT, receiverAccountNo INTEGER, receiverRoutingNo INTEGER, receiverAccountType TEXT, memo TEXT, remainingBalance INTEGER)")


#cur.execute('INSERT INTO Login(username, password, email) VALUES(?, ?, ?)', ('testuser', '012345', 'test@gmail.com'))
cur.execute('INSERT INTO Users(username, password, email, name, AccountNo, address) VALUES(?, ?, ?, ?, ?, ?)', ( 'testuser', '012345' 'test@gmail.com', 'testname', '1111111111', '1000 Palo Verde Road, Irvine'))
cur.execute('INSERT INTO Accounts(AccountNo, currentBalance,) VALUES(?, ?)', (2222222222, 5000))
#cur.execute('INSERT INTO Savings_accounts(savingsAccountNo, currentBalance, routingNo) VALUES (?, ?, ?)', (1111111111, 0, 12345))
            
conn.commit()
cur.close()


