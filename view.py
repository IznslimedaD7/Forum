from app import app, db
from flask import request, render_template, redirect,url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import Users, Categories, Posts, Comments
from datetime import datetime
from flask_login import current_user, login_required, login_user
from utils import save_image, load_user





@app.route('/')
@app.route('/general')
@login_required
def index():
        return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        avatar = save_image(request.files.get('profile_image'), 'avatars', (250, 250))
        user = Users(login=request.form['login'], nickname=request.form['nickname'],
                     password_hash=generate_password_hash(request.form['password']),
                     profile_image=avatar, email=request.form['email'],
                     date_of_create=datetime.now())
        try:
            db.session.add(user)
            db.session.commit()
            print('sus')
            return render_template('base.html')

        except:
            db.session.rollback()
            print('ERROR AFTER REGISTRATION')
            return redirect('/register')

    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        login = request.form['login']
        password1 = generate_password_hash(request.form['password'])
        remember = True if request.form.get('remember') else False

        user = db.session.query(Users).filter(Users.login == login).first()
        if user or check_password_hash(user.password_hash, password1):
            login_user(user, remember=remember)
            return redirect('/general')
        else:
            return redirect('/login')
    else:
        return render_template('login.html')

@app.route('/<name>')
def account(name):
    user = Users.query.filter_by(login=name).first_or_404()
    return render_template('account.html', name=user)


@app.route('/category/create', methods=['GET', 'POST'])
def createcat():
    if request.method == "POST":
        print(2121)
        title_category = request.form['title']
        description_category = request.form['description']
        creator_of_category = request.form['creator']
        category = Categories(title_category=title_category, description_category=description_category, creator_of_category=creator_of_category)
        try:
            db.session.add(category)
            db.session.commit()
            print('cat create')
            return redirect('/category')
        except:
            db.session.rollback()
            print('cat err')
            return redirect('/category/create')
    else:
        return render_template('create-categori.html')

@app.route('/categories')
def category():
    cat = Categories.query.order_by(Categories.title_category).all()
    return render_template('category.html', cat=cat)

@app.route('/categories/<id>')
def show_category(id):
    posts = Posts.query.filter_by(post_category=id).all()
    cat = Categories.query.filter_by(id=id).first_or_404()
    return render_template('catview.html', posts=posts, cat=cat)

@login_required
@app.route('/categories/<id>/create-post', methods=['GET', 'POST'])
def create_post(id):
    cat = Categories.query.filter_by(id=id).first_or_404()
    if request.method == 'POST':
        img = save_image(request.files.get('image'), 'img', (50, 50))
        body = request.form.get('ckeditor')

        post = Posts(title_post=request.form['title'], short_description_of_post=request.form['description'],
                     post_image=img, post_body=body, post_creator=current_user.id, date_create=datetime.now(),
                     last_redactor=current_user.id, date_of_last_redact=datetime.now(), post_category=cat.id)
        try:
            print('susef', post)
            db.session.add(post)
            db.session.commit()
            return redirect('/categories/'+ id)
        except:
            print('error')
            db.session.rollback()
            return render_template('create_post.html', cat=cat)
    else:
        return render_template('create_post.html', cat=cat)

@app.route('/categories/<id>/view/<name>', methods=['GET', 'POST'])
def postview(id, name):
    post = Posts.query.filter_by(post_category=id, title_post=name).first_or_404()
    cat = Categories.query.filter_by(id=id).first_or_404()
    comm = Comments.query.filter_by(comment_post=cat.id).all()
    if request.method == 'POST':
        comment = Comments(date_post=datetime.now(), author=current_user.id,
                           comment_body=request.form['body'], comment_post=cat.id)
        try:
            print("dsds")
            db.session.add(comment)
            db.session.commit()
            return redirect(f'/categories/{id}/view/{name}')
        except:
            print('popod')
            db.session.rollback()
            return redirect(f'/categories/{id}/view/{name}')
    else:
        return render_template('postview.html', cat=cat, post=post, comm=comm)