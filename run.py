from application import app
from application.functions.data_access import create_db

# run the app.
if __name__ == "__main__":
    app.debug = True
    create_db()
    app.run()
    

    
