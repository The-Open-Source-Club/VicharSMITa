from flask import render_template
from flask import flash, redirect, url_for
from flask import request
from flask import abort
from flask_login import current_user, login_user, logout_user
from markdown2 import Markdown

from app import app
from app.forms import LoginForm, RegisterForm, BrowseForm, CreateArticleForm,\
                      ArticleLikeForm, ArticleReadLaterForm, ProfileForm
from app.datamodel import User, Article
from app import db

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
@app.route('/index')
def index():
    title = "Hello"
    news = list(Article.query.order_by(Article.date.desc()).limit(10).all())
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
    if not (current_user.is_authenticated):
        return redirect(url_for('login'))
    form = ProfileForm()
    return render_template('profile.html', title='Sign In', form=form, usertype = 5)

@app.route('/browse', methods=['GET', 'POST'])
def browse():
    form = BrowseForm()
    news = Article.query;
    if(request.args.get('sortby') == None):
        sb = 1;
    else:
        sb = int(request.args.get('sortby'));
    
    if(request.args.get('q') != None):
        if(sb == 1):
            news = news.filter(Article.title.like('%' + request.args.get('q') + '%'));
            news = news.order_by(Article.date.desc()).all();
        elif(sb == 2):
            news = news.filter(Article.title.like('%' + request.args.get('q') + '%'));
            news = news.order_by(Article.date).all();
        return render_template('browse.html', title='Browse', form=form, news=news);
    else:
        news = news.order_by(Article.date.desc()).all();
        return render_template('browse.html', title='Browse', form=form, news=news);

@app.route('/article/<article_id>', methods=['GET', 'POST'])
def article(article_id):
    if(article_id == ""):
        return redirect(url_for('index'))
    else:
        art = Article.query.filter_by(id=article_id).first()
        if(art == None):
            abort(404)
    formlike = ArticleLikeForm()
    formlater = ArticleReadLaterForm()
    if formlike.validate_on_submit():
        print(current_user.id + "##########################################")
    return render_template('article.html', article = art, formlike = formlike, formlater = formlater)

@app.route('/createarticle', methods=['GET', 'POST'])
def createarticle():
    #if not (current_user.is_authenticated):
      #  return redirect(url_for('login'))
    form = CreateArticleForm();
    if form.validate_on_submit():
        md = Markdown()
        art = Article(title = form.title.data, content = md.convert(form.content.data), 
        tags = form.tags.data, imageurl = form.imageurl.data);
        print(form.imageurl.data)
        db.session.add(art)
        db.session.commit()
        flash('Article Published!')
        return redirect(url_for('index'))
    return render_template('createarticle.html', title = "Create Article", form = form);
