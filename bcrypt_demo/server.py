from flask import Flask, render_template, redirect, request, session, flash
import re
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt 

app = Flask(__name__)
app.secret_key='Yankees suck'
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/createUser', methods=['POST'])
def create():
    if len(request.form['first_name']) < 1:
        flash('First name cannot be blank')
    elif not NAME_REGEX.match(request.form['first_name']):
        flash('First name can only contain alphabets')

    elif len(request.form['last_name']) < 1:
        flash('Last name cannot be blank')
    elif not NAME_REGEX.match(request.form['last_name']):
        flash('Last name can only contain alphabets')

    elif len(request.form['email']) < 1:
        flash('Email cannot be blank')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email")

    elif len(request.form['password']) < 1:
        flash('Password cannot be blank.')
    elif len(request.form['password']) < 8:
        flash('Password must be 8 or more characters.')
    elif len(request.form['c_password']) < 1:
        flash('Confirm password!')
    elif request.form['password'] != request.form['c_password']:
        flash ('Passwords do not match')
        return redirect('/')

    mysql = connectToMySQL('loginreg')
    query = 'SELECT * FROM users WHERE email = %(email)s;'
    data = {'email' : request.form['email']}
    result = mysql.query_db(query, data)
    if result:
        flash("Email has already been registered. Use another email or log in to proceed.")
        return redirect('/')
    else:
        try: 
            pw_hash = bcrypt.generate_password_hash(request.form['password'])
            mysql = connectToMySQL('loginreg')
            query = 'INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s)'
            data = {
                'first_name': request.form['first_name'],
                'last_name' : request.form['last_name'],
                'email': request.form['email'],
                'password_hash' : pw_hash
            }
            mysql.query_db(query, data)
            return redirect('/success')
        except ValueError:
            flash('You have some errors to correct')
            return redirect('/')

            
@app.route('/log_in', methods=['POST'])
def login():
    mysql = connectToMySQL('loginreg')
    query = 'SELECT * FROM users WHERE email = %(email)s;'
    data = {'email' : request.form['email']}
    result = mysql.query_db(query, data)
    if result:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            session['email'] = result[0]['email']
            return redirect('/login_success')
        else:
            flash('Incorrect password')
            return redirect('/')
    flash('Email not registered. Please register first')
    return redirect('/')

@app.route('/success')
def success():
    flash('USER SUCCESSFULLY REGISTERED. PLEASE LOG-IN TO PROCEED')
    return redirect('/')

@app.route('/login_success')
def log_in():
    return render_template('success.html')




if __name__ == '__main__':
    app.run(debug=True)