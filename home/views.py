from flask import render_template

from . import home



@home.route('/')
def homepage():    
    return render_template('home/index.html', title='Home')

@home.route('/about')
def about():
    return render_template('home/about.html', title='About')

@home.route('/dashboard')
def dashboard():
    return render_template('home/dashboard.html', title='Dashboard')