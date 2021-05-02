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
    cur.execute("CREATE TABLE IF NOT EXISTS Users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, email TEXT, name TEXT, AccountNo INTEGER UNIQUE, address TEXT )")
    cur.execute("CREATE TABLE IF NOT EXISTS Accounts(id INTEGER PRIMARY KEY AUTOINCREMENT, AccountNo INTEGER UNIQUE REFERENCES User(AccountNo), currentBalance REAL)")
    cur.execute('INSERT INTO Users(username, password, email, name, AccountNo, address) VALUES(?, ?, ?, ?, ?, ?)', ( 'testuser', '012345', 'test@gmail.com', 'testname', 1111111111, '1000 Palo Verde Road, Irvine'))
    cur.execute('INSERT INTO Accounts(AccountNo, currentBalance) VALUES(?, ?)', (2222222222, 5000))
    conn.commit()
    cur.close()

# run the app.
if __name__ == "__main__":
    app.debug = True
    create_db()
    app.run()
    

    
