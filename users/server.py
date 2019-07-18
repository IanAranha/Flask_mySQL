from flask import Flask, render_template, request, redirect, session, flash
import re
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt 

app = Flask(__name__)
app.secret_key='Yankees suck'
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

@app.route('/users')
def index():
    mysql = connectToMySQL('friends3')
    result = mysql.query_db('SELECT * FROM users')
    return render_template('index.html', users=result)



@app.route('/users/new')
def newUser():
    return render_template('add.html')



@app.route('/users/create', methods=['POST'])
def createUser():
    mysql = connectToMySQL('friends3')
    query=('INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW())')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    mysql.query_db(query, data)
    return redirect('/users')




@app.route('/users/<id>')
def showUser(id):
    mysql = connectToMySQL('friends3')
    query=('SELECT * FROM users WHERE id = %(id)s')
    data = {
        'id' : id
    }
    result = mysql.query_db(query, data)
    return render_template('show.html', user_info = result)




@app.route('/users/<id>/edit')
def editUser(id):
    mysql = connectToMySQL('friends3')
    query=('SELECT * FROM users WHERE id = %(id)s')
    data = {
        'id' : id
    }
    result = mysql.query_db(query, data)
    return render_template('edit.html', data=result)




@app.route('/users/<id>/edit' , methods=['POST'])
def updateUser(id):
    mysql = connectToMySQL('friends3')
    query=('UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s , email = %(email)s, updated_at = NOW() WHERE id = %(id)s' )
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'id' : id
    }
    mysql.query_db(query, data)
    return redirect('/users')




@app.route('/users/<id>/delete')
def deleteUser(id):
    mysql = connectToMySQL('friends3')
    query=('DELETE FROM users WHERE id = %(id)s' )
    data = {
        'id' : id
    }
    mysql.query_db(query, data)
    return redirect('/users')


if __name__ == '__main__':
    app.run(debug=True)