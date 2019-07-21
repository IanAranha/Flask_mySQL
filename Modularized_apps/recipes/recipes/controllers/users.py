from recipes import app
from flask import render_template, redirect, request, session, flash

from datetime import datetime, date

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from recipes.models.user import User
user=User()

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class Users:
    def index(self):
        session.pop('user_id', None)
        return render_template('index.html')

    def createUser(self):
        if len(request.form['username']) < 1:
            flash('First name cannot be blank', 'username')
        if len(request.form['email']) < 1:
            flash('Email cannot be blank', 'email')
        if not EMAIL_REGEX.match(request.form['email']):
            flash("Invalid email", 'email')
        if len(request.form['password']) < 1:
            flash('Password cannot be blank.', 'password')
        if len(request.form['password']) < 8:
            flash('Password must be 8 or more characters.', 'password')
        if len(request.form['c_password']) < 1:
            flash('Confirm password!', 'c_password')
        if request.form['password'] != request.form['c_password']:
            flash ('Passwords do not match', 'c_password')
        today = date.today()
        birth = datetime.strptime(request.form['birthday'], '%Y-%m-%d')
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        if age < 18:
            flash('Sorry, you must be at least 18 years old to use this site.', 'birthday')

        if '_flashes' in session.keys():
            return redirect("/")
        else:
            result=user.checkUser()
            if result:
                flash("Email used. Use alternative or log in to proceed.", 'email')
                return redirect('/')
            else:
                pw_hash = bcrypt.generate_password_hash(request.form['password'])
                return user.newUser(pw_hash)


    def createUserSuccess(self):
        flash('User successfully registered. Please log-in to continue.')
        return redirect('/')

    def log_in(self):
        if len(request.form['log_username']) < 1:
            flash('Please enter username!', 'log_username')
        if len(request.form['log_password']) < 1:
            flash('Please enter password.', 'log_password')
            return redirect('/')
        result=user.log_in()
        if result:
            if bcrypt.check_password_hash(result[0]['password'], request.form['log_password']):
                session['user_id']=result[0]['id']
                session['email']=result[0]['email']
                session['username']=result[0]['username']
                return redirect('/dashboard')
            else:
                flash('Incorrect password', 'log_password')
                return redirect('/')
        flash('User not registered. Please register first', 'log_username')
        return redirect('/')

    def dashboard(self):
        if 'email' not in session:
            return render_template('hack.html')
        else:
            return render_template('dashboard.html')

    def create(self):
        if 'email' not in session:
            return render_template('hack.html')
        else:
            return render_template('create.html')

    def createRecipe(self):
        if 'email' not in session:
            return render_template('hack.html')
        if len(request.form['name']) < 1:
            flash('This field cannot be blank', 'name')
        if len(request.form['name']) < 3:
            flash("This field must contain more than 3 characters", 'name')
        if len(request.form['description']) < 1:
            flash('This field cannot be blank', 'description')
        if len(request.form['description']) < 3:
            flash("This field must contain more than 3 characters", 'description')
        if len(request.form['instructions']) < 1:
            flash("This field cannot be blank", 'instructions')
        if len(request.form['instructions']) < 3:
            flash("This field must contain more than 3 characters", 'instructions')
        if '_flashes' in session.keys():
            return redirect("/create")
        else:
            return user.createRecipe()

    def createRecipeSuccess(self):
        flash("Recipe has been created", 'message')
        return redirect('/create')

    def logout(self):
        session.clear()
        return redirect('/')

    def review(self):
        if 'email' not in session:
            return render_template('hack.html')
        else:
            recipes=user.review()
            return render_template('review.html', results=recipes)

    def show(self, id):
        if 'email' not in session:
            return render_template('hack.html')
        else:
            recipe=user.show(id)
            return render_template('view.html', result=recipe)

    def delete(self, id):
        if 'email' not in session:
            return render_template('hack.html')
        else:
            user.delete(id)
            return redirect('/review')