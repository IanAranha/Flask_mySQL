from the_wall import app
from flask import request, redirect, session

from the_wall.config.mysqlconnection import connectToMySQL


class User:
    def checkUser(self):
        mysql = connectToMySQL('theWall')
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        data = {'email' : request.form['email']}
        result = mysql.query_db(query, data)
        return result   

    def newUser(self, pw_hash):
        mysql = connectToMySQL('theWall')
        query = 'INSERT INTO users (first_name,last_name, email, password, birthday, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s,%(email)s, %(password)s, %(birthday)s, NOW(), NOW())'
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password' : pw_hash,
            'birthday': request.form['birthday']
            }
        mysql.query_db(query, data)
        return redirect('/registration_success')

    def log_in(self):
        mysql = connectToMySQL('theWall')
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        data = {'email' : request.form['log_email']}
        result = mysql.query_db(query, data)
        return result

    def post_message(self):
        mysql = connectToMySQL('theWall')
        query = 'INSERT INTO messages (message, created_at, updated_at, user_id) VALUES (%(message)s,NOW(),NOW(),%(user_id)s)'
        data = {
            'message' : request.form['message'],
            'user_id': session['user_id']
            }
        mysql.query_db(query, data)
        return redirect('/message_success')

    def all_messages(self):
        mysql = connectToMySQL('theWall')
        query = 'SELECT * FROM messages JOIN users on messages.user_id = users.id ORDER BY messages.created_at DESC'
        result = mysql.query_db(query)
        return result
    
    def post_comment(self, id):
        mysql = connectToMySQL('theWall')
        query = 'INSERT INTO comments (user_id,message_id, comment, created_at, updated_at) VALUES (%(user_id)s,%(message_id)s,%(comment)s,NOW(),NOW())'
        data = {
            'user_id': session['user_id'],
            'message_id': id,
            'comment': request.form['comment']
            }
        mysql.query_db(query, data)
        return redirect('/comment_success')

    def post_comment_update(self):
        mysql = connectToMySQL('theWall')
        query = 'SELECT * FROM comments JOIN messages on comments.message_id = messages.id JOIN users ON users.id = comments.user_id ORDER BY comments.created_at DESC'
        result = mysql.query_db(query)
        return result



