from advanced_login import app
from flask import render_template, request, redirect, session, flash
from advanced_login.config.mysqlconnection import connectToMySQL
import re
from advanced_login.models.user import User

from flask_bcrypt import Bcrypt

NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)
user=User()

class Users:
    def index(self):
        session.pop('email', None)
        return render_template('index.html')

    def createUser(self):
        if len(request.form['first_name']) < 1:
            flash('First name cannot be blank', 'first_name')
        elif not NAME_REGEX.match(request.form['first_name']):
            flash('First name can only contain alphabets', 'first_name')
        if len(request.form['last_name']) < 1:
            flash('Last name cannot be blank', 'last_name')
        elif not NAME_REGEX.match(request.form['last_name']):
            flash('Last name can only contain alphabets', 'last_name')
        if len(request.form['email']) < 1:
            flash('Email cannot be blank', 'email')
        elif not EMAIL_REGEX.match(request.form['email']):
            flash("Invalid email", 'email')
        if len(request.form['password']) < 1:
            flash('Password cannot be blank.', 'password')
        elif len(request.form['password']) < 8:
            flash('Password must be 8 or more characters.', 'password')
        if len(request.form['c_password']) < 1:
            flash('Confirm password!', 'c_password')
        elif request.form['password'] != request.form['c_password']:
            flash ('Passwords do not match', 'c_password')
        
        if '_flashes' in session.keys():
            return redirect("/")
        else:
            result=user.createUser()
            if result:
                flash("Email used. Use alternative or log in to proceed.", 'email')
                return redirect('/')
            else:
                pw_hash = bcrypt.generate_password_hash(request.form['password'])
                return user.newUser(pw_hash)
            
    def userRegistered(self):
        flash("User successfully registered. Please log-in.", 'message')
        return redirect('/')
 
    def log_in(self):
        if len(request.form['log_email']) < 1:
            flash('Please enter email!', 'log_email')
        elif not EMAIL_REGEX.match(request.form['log_email']):
            flash("Invalid email!", 'log_email')
        if len(request.form['log_password']) < 1:
            flash('Please enter password.', 'log_password')
            return redirect('/')
        result=user.log_in()
        if result:
            if bcrypt.check_password_hash(result[0]['password'], request.form['log_password']):
                session['email'] = result[0]['email']
                session['user_id']=result[0]['id']
                session['first_name']=result[0]['first_name']
                session['user_level'] = result[0]['user_level']
                return redirect('/login_success')
            else:
                flash('Incorrect password', 'log_password')
                return redirect('/')
        flash('Email not registered. Please register first', 'log_email')
        return redirect('/')

    def login_success(self):
        if 'email' not in session:
            return redirect('/hack')
        if session['user_level'] == 9:
            return redirect('/admin')
        else:
            return redirect('/user')

    def admin(self):
        if 'user_level' not in session:
            return redirect('/hack')
        elif session['user_level'] != 9:
            return redirect('/hack')
        else:
            result=user.admin()
            return render_template('admin.html', users=result)

    def user(self):
        if 'email' not in session:
            return redirect('/hack')
        else:
            return render_template('user.html')

    def remove(self, id):
        return user.remove(id)

    def remove_admin(self, id):
        return user.remove_admin(id)

    def make_admin(self, id):
        return user.make_admin(id)

    def hack(self):
        return render_template('hack.html')

    def log_off(self):
        session.clear()
        return redirect('/')

