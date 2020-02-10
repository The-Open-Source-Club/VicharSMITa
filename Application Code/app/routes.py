from flask import render_template
from flask import flash, redirect, url_for
from flask import request
from flask import abort
from flask_login import current_user, login_user, logout_user
from markdown2 import Markdown

from app import app
from app.forms import LoginForm, RegisterForm, BrowseForm, CreateArticleForm,\
                      ArticleForm, ProfileForm
from app.datamodel import User, Article
from app import db

def rolestr(k):
    if (k == 0):
        return "Administrator";
    elif (k == 1):
        return "Reporter";
    elif (k == 2):
        return "Normal User";

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
        user = User(username=form.username.data, email=form.email.data, role=2)
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
    p = "";
    print(current_user.articles);
    for i in current_user.articles.split():
        "<li><a href=\"/articles/" + i + "\">" + Article.query.filter_by(id=int(i)).first().title + "</a></li>"
    return render_template('profile.html', title='Your Profile', form=form, rolestr = rolestr(current_user.role), article = p)

@app.route('/admin')
def admin():
    if not (current_user.is_authenticated):
        return redirect(url_for('login'))
    elif(not current_user.role == 0):
        return render_template('denied.html')
        
    form = AdminForm()
    return render_template('admin.html', title='Admin Panel', form=form)

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
    if(article_id == None):
        return redirect(url_for('index'))
    else:
        art = Article.query.filter_by(id=article_id).first()
        if(art == None):
            abort(404)
    form = ArticleForm()
    if form.validate_on_submit():
        if not (current_user.is_authenticated):
            return redirect(url_for('login'))
        if form.like.data:
            if(str(current_user.id) not in (art.likedusers.split() if art.likedusers else [])):
                art.likes += 1
                art.likedusers = (art.likedusers if art.likedusers else "") + str(current_user.id) + " "; 
                db.session.commit()
            else:
                return render_template('article.html', article = art, form = form, message = "You have already liked this article!")
        elif form.readlater.data:
            if(str(art.id) not in (current_user.articles.split() if current_user.articles else [])):
                if current_user.articles:
                    current_user.articles += " " + str(art.id)
                else:
                    current_user.articles = str(art.id)
                db.session.commit()
            else:
                return render_template('article.html', article = art, form = form, message = "This article has already been marked!")
    return render_template('article.html', article = art, form = form)

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
