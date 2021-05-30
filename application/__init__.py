from flask import Flask
#from flask_talisman import Talisman
from datetime import timedelta

app = Flask(__name__, template_folder='./templates')
#Talisman(app)
from application import views
from application.functions.data_access import create_db
from application.functions.util import gen_key
app.config['SECRET_KEY'] = gen_key()
app.config['PERMANENT_SESSION_LIFETIME']= timedelta(minutes=5)
#app.config['SESSION_COOKIE_SECURE'] = True
#app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
create_db()