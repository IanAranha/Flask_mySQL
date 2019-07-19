from emails_validation.config.mysqlconnection import connectToMySQL
from flask import request, redirect, flash, session

class Email():
    def validate(self):
        mysql = connectToMySQL('emails')
        query = ('SELECT * FROM emails WHERE email = %(email)s')
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

    def success(self):
        mysql = connectToMySQL('emails')
        result = mysql.query_db('SELECT * FROM emails')
        return result

    def delete(self, id):
        mysql = connectToMySQL('emails')
        query = 'DELETE FROM emails WHERE id = %(id)s'
        data = {
            'id': id
        }
        mysql.query_db(query, data)
        return redirect('/success')
