from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    title = "Hello";
    msg = "hi";
    body = [1, 2, 3, 4, 5, 6, 7, 8];
    return render_template("index.html", title = title, msg = msg, body = body);

