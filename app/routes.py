from flask import render_template, redirect, url_for, flash, session, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User

@app.route('/')
def home():
    return render_template('home.html', username=session.get('username'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if session.get('username'):
        flash('You are already registered!', 'warning')
        return redirect(url_for('home'))
    else:
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("You've been registered successfully!", 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('username'):
        flash('You are already logged in!', 'warning')
        return redirect(url_for('home'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                session['id'] = user.id
                session['username'] = user.username
                session['email'] = user.email
                return redirect(url_for('home'))
            else:
                flash("Couldn't find the user. Please check your email and password.", 'error')
        return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    if session.get('username'):
        session.clear()
        return redirect(url_for('home'))
    else:
        flash("You haven't logged in yet!", 'error')
        return redirect(url_for('login'))

@app.route('/protected')
def protected():
    if session.get('username'): 
        return render_template('protected.html', id=session.get('id'), 
                               username=session.get('username'), 
                               email=session.get('email'))
    else:
        flash("In order to access the protected page, you need to log in!", 'error')
        return(redirect(url_for('login')))