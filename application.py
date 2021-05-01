from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


# run the app.
if __name__ == "__main__":
    app.debug = True
    app.run()