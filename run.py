#import sqlite3
#from flask import Flask, render_template, request, redirect, url_for, session

from application import app
from application.functions.data_access import create_db

#app = Flask(__name__, template_folder='./application/templates')
#app.config['SECRET_KEY'] = 'bQ9J84inbtoUcjLZFbQTVg'


# run the app.
if __name__ == "__main__":
    app.debug = True
    create_db()
    app.run()
    

    
