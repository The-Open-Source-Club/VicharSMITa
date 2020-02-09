from flask import render_template
from flask import flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app import app
from app.forms import LoginForm
from app.datamodel import User

@app.route('/')
@app.route('/index')
def index():
    title = "Hello";
    msg = "hi";
    body = [1, 2, 3, 4, 5, 6, 7, 8];
    return render_template("index.html", title = title, msg = msg, body = body);

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    return None;

@app.route('/browse', methods=['GET', 'POST'])
def search():
    return None;

@app.route('/article', methods=['GET', 'POST'])
def article():
    return None;
