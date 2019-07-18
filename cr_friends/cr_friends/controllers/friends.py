from cr_friends.config.mysqlconnection import connectToMySQL
from flask import render_template, request, redirect

class Friends:
    def index(self):
        mysql = connectToMySQL('friends')
        query = "SELECT * FROM friends"
        result=mysql.query_db(query)
        return render_template('index.html', friends=result)

    def create(self):
        mysql = connectToMySQL('friends')
        query = 'INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(occupation)s, NOW(), NOW());'
        data = {
            "first_name" : request.form['first_name'],
            "last_name" : request.form['last_name'],
            "occupation" : request.form['occupation']
        }
        mysql.query_db(query, data)
        return redirect('/')