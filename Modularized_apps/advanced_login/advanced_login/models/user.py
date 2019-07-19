from advanced_login import app
from advanced_login.config.mysqlconnection import connectToMySQL
from flask import request,flash,redirect, session
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class User:
    def createUser(self):
        mysql = connectToMySQL('advanced_login')
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        data = {'email' : request.form['email']}
        result = mysql.query_db(query, data)
        return result
        
            
    def newUser(self, pw_hash):
        mysql = connectToMySQL('advanced_login')
        query = 'INSERT INTO users (first_name, last_name, email, password,user_level, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s, %(user_level)s, NOW(), NOW())'
        data = {
            'first_name': request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email': request.form['email'],
            'password_hash' : pw_hash,
            'user_level' : 1
            }
        mysql.query_db(query, data)
        return redirect('/success')
    
    def log_in(self):
        mysql = connectToMySQL('advanced_login')
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        data = {'email' : request.form['log_email']}
        result = mysql.query_db(query, data)
        return result

    def admin(self):
        mysql = connectToMySQL('advanced_login')
        result = mysql.query_db('SELECT * FROM users')
        return result

    def remove(self, id):
        mysql = connectToMySQL('advanced_login') 
        query = 'DELETE from users WHERE id = %(id)s'
        data = {
            'id' : id
        }
        mysql.query_db(query,data)
        return redirect('/admin')

    def remove_admin(self, id):
        mysql = connectToMySQL('advanced_login')
        query = 'UPDATE users SET user_level = 1 WHERE id = %(id)s'
        data = {
            'id' : id
        }
        mysql.query_db(query,data)
        return redirect('/admin')

    def make_admin(self, id):
        mysql = connectToMySQL('advanced_login')
        query = 'UPDATE users SET user_level = 9 WHERE id = %(id)s'
        data = {
            'id' : id
        }
        mysql.query_db(query,data)
        return redirect('/admin')



