from app import app, db, avatars
from flask import request, render_template, redirect, send_from_directory, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import Users
from datetime import datetime
from flask_login import current_user


@app.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(app.config['AVATARS_SAVE_PATH'], filename)


@app.route('/')
@app.route('/general')
def index():
        return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = Users(login=request.form['login'], nickname=request.form['nickname'],
                     password_hash=generate_password_hash(request.form['password']),
                     profile_image=request.form['profile_image'], email=request.form['email'],
                     date_of_create=datetime.now())
        f = request.form['profile_image']
        raw_filename = avatars.save_avatar(f)
        session['raw_filename'] = raw_filename
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

