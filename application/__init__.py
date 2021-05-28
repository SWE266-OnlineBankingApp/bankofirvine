from flask import Flask

app = Flask(__name__, template_folder='./templates')

from application import views
from application.functions.data_access import create_db
from application.functions.util import gen_key
app.config['SECRET_KEY'] = gen_key()
create_db()