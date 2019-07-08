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
        session["email"] = request.form['email']
        mysql = connectToMySQL('loginreg')
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        data = {'email' : request.form['email']}
        result = mysql.query_db(query, data)
        if result:
            flash("Email used. Use alternative or log in to proceed.", 'email')
            return redirect('/')
        else:
            try: 
                pw_hash = bcrypt.generate_password_hash(request.form['password'])
                mysql = connectToMySQL('loginreg')
                query = 'INSERT INTO users (first_name, last_name, email, password,created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s, NOW(), NOW())'
                data = {
                    'first_name': request.form['first_name'],
                    'last_name' : request.form['last_name'],
                    'email': request.form['email'],
                    'password_hash' : pw_hash
                }
                mysql.query_db(query, data)
                return redirect('/success')
            except ValueError:
                flash('You have some errors to correct', 'c_password')
                return redirect('/')


@app.route('/log_in', methods=['POST'])
def login():
    if len(request.form['email']) < 1:
        flash('Please enter email!', 'log_email')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email!", 'log_email')
        return redirect('/')
    if len(request.form['password']) < 1:
        flash('Please enter password.', 'log_password')
        return redirect('/')

    mysql = connectToMySQL('loginreg')
    query = 'SELECT * FROM users WHERE email = %(email)s;'
    data = {'email' : request.form['email']}
    result = mysql.query_db(query, data)
    if result:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            session['email'] = result[0]['email']
            return redirect('/login_success')
        else:
            flash('Incorrect password', 'log_password')
            return redirect('/')
    flash('Email not registered. Please register first', 'log_email')
    return redirect('/')

@app.route('/success')
def success():
    flash('Registration successful. Log-in to proceed', 'log_email')
    return redirect('/')


@app.route('/login_success')
def log_in():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)