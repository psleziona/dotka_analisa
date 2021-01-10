from app import app, db
from app.forms import LoginForm, RegisterForm
from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import User

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if not current_user.is_authenticated:
        if form.validate_on_submit():
            user = form.username.data
            password = form.password.data
            u = User.query.filter_by(username=user).first()
            if u.check_password(password):
                flash('Success')
                login_user(u)
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password')
                return redirect(url_for('login'))
    else:
        flash('You are already logged in!')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)
        

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        flash('You already have acc')
        return redirect(url_for('index'))
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        u = User(username=username, email=email)
        u.generate_password(password)
        db.session.add(u)
        db.session.commit()
        flash('Success, you can login now')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/users/<user>')
def user_page(user):
    isAdmin = False
    u = User.query.filter_by(username=user).first()
    if u is None:
        return '<h1>No such user, 404 soon</h1>'
    if current_user.username == 'admin' and u.username == 'admin':
        isAdmin = True
    return render_template('user_page.html', user=u, admin=isAdmin)

    
