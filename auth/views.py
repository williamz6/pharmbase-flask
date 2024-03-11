from flask import flash, render_template, redirect, url_for, session, request

from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from pharmbase.auth.forms import RegForm, LoginForm
from pharmbase import app, db, bcrypt
from pharmbase.models import User, Role

@auth.route('/register', methods=['GET', 'POST'])
def register():
        
    form =RegForm(request.form)

    
    # if form.validate_on_submit():
    #     hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    #     user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=hashed_password)

    #     db.session.add(user)
    #     db.session.commit()

    #     flash('Your Account has been created', 'success')
    #     return redirect(url_for('auth.login'))

    if form.validate_on_submit():
       
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=form.password.data)

        # add employee to the database
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered! You may now login :)', 'success')
    
       # redirect to the login page
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form, title='Register' )

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verifypassword(form.password.data):
            login_user(user, remember=form.remember.data)
            session['logged_in'] =True
            session['email'] =form.email.data
            flash(f'{form.email.data} Logged in!', 'success')
            return redirect(url_for('home.homepage'))
        else:
            error= "Wrong Login details"
            return render_template('auth/login.html', form=form, error=error, title='Login')

   
    return render_template('auth/login.html', form=form,  title='Login')

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('logged out!', 'success')
    return redirect(url_for('home.homepage'))
@auth.route('/roles')
def list_roles():
    
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('auth/roles/roles.html',
                           roles=roles, title='Roles')
