import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')    

@app.route('/account')
def account():
    return render_template('account.html')   

def create_db():
    conn = sqlite3.connect('bankdata.db')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Users")
    cur.execute("DROP TABLE IF EXISTS Accounts")
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute("CREATE TABLE IF NOT EXISTS Users(userId INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, email TEXT, lastname TEXT, firstname TEXT, address TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Accounts(accountId INTEGER PRIMARY KEY AUTOINCREMENT, AccountNo INTEGER UNIQUE, currentBalance REAL, userId INTEGER, FOREIGN KEY(userId) REFERENCES Users(userId))")
    #insert a new user with auto-assigned userId=1
    cur.execute('INSERT INTO Users(username, password, email, lastname, firstname, address) VALUES(?, ?, ?, ?, ?, ?)', ( 'testuser', '012345', 'test@gmail.com', 'testlastname', 'testfirstname', '1000 Palo Verde Road, Irvine'))
    # insert an account for user with userId=1
    cur.execute('INSERT INTO Accounts(AccountNo, currentBalance, userId) VALUES(?, ?, ?)', (2222222222, 5000, 1))

    conn.commit()
    cur.close()

# run the app.
if __name__ == "__main__":
    app.debug = True
    create_db()
    app.run()
    

    
