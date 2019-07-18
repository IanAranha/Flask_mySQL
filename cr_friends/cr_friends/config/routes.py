from cr_friends import app
from cr_friends.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, request

@app.route('/')
def index():
    mysql = connectToMySQL('friends')
    all_friends = mysql.query_db("SELECT * FROM friends")
    return render_template('index.html', friends=all_friends)

@app.route('/create_friend', methods=['POST'])
def create():
    mysql = connectToMySQL('friends')
    query = 'INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(occupation)s, NOW(), NOW());'
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "occupation" : request.form['occupation']
        }
    mysql.query_db(query, data)
    return redirect('/')