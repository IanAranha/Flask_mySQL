from recipes import app
from recipes.config.mysqlconnection import connectToMySQL
from flask import redirect, request, session

class User:
    def checkUser(self):
        mysql = connectToMySQL('recipes')
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        data = {'email' : request.form['email']}
        result = mysql.query_db(query, data)
        return result

    def newUser(self, pw_hash):
        mysql = connectToMySQL('recipes')
        query = 'INSERT INTO users (username, email, dojo_location, password, birthday, created_at, updated_at) VALUES (%(username)s, %(email)s, %(dojo_location)s, %(password_hash)s, %(birthday)s, NOW(), NOW())'
        data = {
            'username': request.form['username'],
            'email': request.form['email'],
            'dojo_location': request.form['dojo_location'],
            'password_hash' : pw_hash,
            'birthday': request.form['birthday']
            }
        mysql.query_db(query, data)
        return redirect('/registration_success')

    def log_in(self):
        mysql = connectToMySQL('recipes')
        query = 'SELECT * FROM users WHERE username = %(username)s;'
        data = {'username' : request.form['log_username']}
        result = mysql.query_db(query, data)
        return result

    def createRecipe(self):
        mysql = connectToMySQL('recipes')
        query = 'INSERT INTO recipes (name, description, instructions, time, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(time)s, NOW(), NOW(),%(user_id)s)'
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'time' : request.form['time'],
            'user_id': session['user_id']
            }
        mysql.query_db(query, data)
        return redirect('/createRecipeSuccess')
    
    def review(self):
        mysql=connectToMySQL('recipes')
        query='SELECT * FROM recipes WHERE recipes.user_id = %(id)s'
        data={'id':session['user_id']} 
        review=mysql.query_db(query, data)
        return review

    def show(self, id):
        mysql=connectToMySQL('recipes')
        query='SELECT * FROM recipes WHERE id = %(id)s'
        data={
            'id':id
        } 
        review=mysql.query_db(query, data)
        return review

    def delete(self, id):
        mysql=connectToMySQL('recipes')
        query='DELETE FROM recipes WHERE id = %(id)s'
        data={
            'id':id
        } 
        review=mysql.query_db(query, data)
        return review
