from flask import Flask, render_template, redirect, request, flash, session
import re
from mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key = "Yankees Suck"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    mysql = connectToMySQL('emails')
    query = ('SELECT * FROM emails WHERE email = %(email)s')
    if len(request.form['email']) < 1:
        flash('Email cannot be blank.', 'error')
        return redirect('/')
    if not EMAIL_REGEX.match(request.form['email']):
        flash('Invalid email.', 'error')
        return redirect('/')
    data = {'email' : request.form['email']}
    result = mysql.query_db(query, data)
    if result:
        flash("Email has already been registered.", 'error')
        return redirect('/')
    else:
        mysql = connectToMySQL('emails')
        query = 'INSERT INTO emails (email, created_at, updated_at) VALUES(%(email)s, NOW(), NOW())'
        data = {
             'email': request.form['email']
             }
        mysql.query_db(query, data)
        session['email'] = request.form['email']
        flash(' is a valid email and has been added to data base')
        return redirect('/success')

@app.route('/success')
def success():
    if 'email' not in session:
        flash('Illegal hack!')
        return redirect('/')
    else:
        mysql = connectToMySQL('emails')
        all_emails = mysql.query_db('SELECT * FROM emails')
        return render_template('success.html', emails=all_emails)

@app.route('/go_back')
def go_back():
    session.pop('email', None)
    return redirect('/')

@app.route('/delete/<id>')
def delete(id):
    mysql = connectToMySQL('emails')
    query = 'DELETE FROM emails WHERE id = %(id)s'
    data = {
        'id': id
    }
    mysql.query_db(query, data)
    flash(' has been deleted from database')
    return redirect('/success')

if __name__ == "__main__":
    app.run(debug=True)
