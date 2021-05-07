from flask import Flask

app = Flask(__name__, template_folder='./templates')
app.config['SECRET_KEY'] = 'bQ9J84inbtoUcjLZFbQTVg'

from application import views