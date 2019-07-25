from books import app
from flask import redirect, render_template, request, session, flash

from datetime import datetime, date

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from books.models.user import User
user=User()

app.secret_key='Yankees Suck'

class Users:
    def index(self):
        return render_template('index.html')

    def createUser(self):
        if len(request.form['first_name']) < 1:
            flash('First name cannot be blank', 'first_name')
        if len(request.form['last_name']) < 1:
            flash('Last name cannot be blank', 'last_name')
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

    def registration_success(self):
        flash("User registered. Log-in to continue")
        return redirect('/')

    def log_in(self):
        if len(request.form['log_email']) < 1:
            flash('Please enter email!', 'log_email')
        if len(request.form['log_password']) < 1:
            flash('Please enter password.', 'log_password')
            return redirect('/')
        result=user.log_in()
        if result:
            if bcrypt.check_password_hash(result[0]['password'], request.form['log_password']):
                session['email']=result[0]['email']
                session['first_name']=result[0]['first_name']
                session['user_id']=result[0]['id']
                return redirect('/books')
            else:
                flash('Incorrect password', 'log_password')
                return redirect('/')
        flash('User not registered. Please register first', 'log_email')
        return redirect('/')

    def books(self):
        if 'email' not in session:
            return redirect ('/hack')
        else:
            result=user.showBooks()
            total_books = result[0]['COUNT(*)']
            if total_books == 0:
                return render_template('books.html')
            elif total_books > 0 and total_books < 3:
                result1=user.showThree()
                return render_template('books.html', results=result1)
            else:
                result1=user.showThree()
                result2=user.showRest()
                return render_template('books.html',results=result1, rest=result2)
    
    def add_book(self):
        if 'email' not in session:
            return redirect('/hack')
        else:
            result=user.authors_list()
            return render_template('add_book.html', options=result)

    def addbook(self):
        if request.form['new_author'] == "":
            user.addauthor1()
        else:
            user.addauthor2()
            
        result=user.checkBook()
        if result:
            flash('Book already reviewed')
            return redirect ('/books')
        else:
            result=user.addbook()
            route=('/showOne/'+str(result))
            return redirect(route)

    def showOne(self, id):
        results = user.showOne(id)
        reviews = user.showReviews(id)
        return render_template('show.html', results=results, reviews=reviews)

    def logout(self):
        session.clear()
        return redirect('/')

    def addReview(self):
        result=user.addReview()
        route=('/showOne/'+str(result))
        return redirect(route)
        
    def showUser(self, id):
        result=user.showUser(id)
        count=user.countReviews(id)
        counts=count[0]['count(users.id)']
        reviews=user.allReviews(id)
        return render_template('showUser.html', results=result, counts=counts, reviews=reviews)