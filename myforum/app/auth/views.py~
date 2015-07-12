from flask import render_template,redirect,request,url_for,flash,current_app
from flask.ext.login import login_user,login_required,logout_user,current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm,RegisterForm

@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('invalid usernamen or password')
    return render_template('auth/login.html',form=form)
    
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have logged out')
    return redirect(url_for('main.index'))
    
@auth.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('you can login in') 
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)
    
#@auth.before_app_request
#def before_request():
#    if current_user.is_authenticated():
#        current_user.ping()
#        if  request.endpoint[:5]!='auth':
#            return redirect(url_for('main.user'))
