from flask import render_template
from flask import flash, redirect, url_for
from flask import request
from flask_login import current_user, login_user, logout_user
from app import app
from app.forms import LoginForm, RegisterForm
from app.datamodel import User, Article
from app import db

@app.route('/')
@app.route('/index')
def index():
    title = "Hello"
    news = list(Article.query.order_by(Article.date.desc()))
    return render_template("index.html", title = title, news = news);

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register an Account', form=form)

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

@app.route('/article/<article_id>', methods=['GET', 'POST'])
def article(article_id):
    if(article_id == None):
        return redirect(url_for('index'))
    
    return render_template('article.html', art_title = art_title, art_date = art_date, art_content = art_content);

@app.route('/createarticle', methods=['GET', 'POST'])
def createarticle():
    return render_template('article.html');
