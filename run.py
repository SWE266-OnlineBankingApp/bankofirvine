from application import app

# run the app.
if __name__ == "__main__":
    app.debug = False
    app.run(ssl_context=('cert.pem', 'key.pem'))
    
