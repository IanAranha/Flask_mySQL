from books import app
from flask import request, redirect, session

from books.config.mysqlconnection import connectToMySQL


class User:
    def checkUser(self):
        mysql = connectToMySQL('books')
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        data = {'email' : request.form['email']}
        result = mysql.query_db(query, data)
        return result

    def newUser(self, pw_hash):
        mysql = connectToMySQL('books')
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
        mysql = connectToMySQL('books')
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        data = {'email' : request.form['log_email']}
        result = mysql.query_db(query, data)
        return result
    
    def addauthor1(self):
        mysql = connectToMySQL('books')
        query = 'SELECT * FROM authors WHERE authors.author=%(author)s'
        data = {
            'author': request.form['author'],
        }
        result=mysql.query_db(query,data)
        session['result'] = result[0]['id']
        return result

    def addauthor2(self):
        mysql = connectToMySQL('books')
        query = 'INSERT INTO authors (author, created_at, updated_at) VALUES (%(author)s,NOW(),NOW())'
        data = {
            'author': request.form['new_author'],
            }
        result=mysql.query_db(query,data)
        session['result'] = result
        return result
    
    def checkBook(self):
        mysql = connectToMySQL('books')
        query = 'SELECT * FROM books WHERE title = %(title)s;'
        data = {'title' : request.form['title']}
        result = mysql.query_db(query, data)
        print(result)
        return result

    def addbook(self):
        mysql = connectToMySQL('books')
        query = 'INSERT INTO books (title, rating, created_at, updated_at, author_id, user_id) VALUES (%(title)s,%(rating)s,NOW(),NOW(),%(author_id)s, %(user_id)s)'
        data = {
            'title': request.form['title'],
            'rating': request.form['rating'],
            'author_id': session['result'],
            'user_id': session['user_id'],
            }
        book_id = mysql.query_db(query,data)

        mysql = connectToMySQL('books')
        query = 'INSERT INTO reviews (review, created_at, updated_at,book_id, user_id) VALUES (%(review)s,NOW(),NOW(),%(book_id)s, %(user_id)s)'
        data = {
            'review': request.form['review'],
            'book_id': book_id,
            'user_id': session['user_id'],
            }
        result = mysql.query_db(query,data)
        return result

    def showBooks(self):
        mysql = connectToMySQL('books')
        query = 'SELECT COUNT(*) from books'
        result = mysql.query_db(query)
        return result

    def showThree(self):
        mysql = connectToMySQL('books')
        query = 'SELECT * from books JOIN authors ON books.author_id = authors.id JOIN reviews ON reviews.book_id = books.id JOIN users ON reviews.user_id = users.id ORDER BY books.created_at DESC LIMIT 3'
        result = mysql.query_db(query)
        return result

    def showRest(self):
        mysql = connectToMySQL('books')
        query = 'SELECT COUNT(*) from books'
        count = mysql.query_db(query)
        if count[0]['COUNT(*)'] <= 3:
            return count
        else:
            show = count[0]['COUNT(*)']-3
            mysql = connectToMySQL('books')
            query = 'SELECT * from books ORDER BY books.created_at ASC LIMIT %(count)s'
            data={
                'count':show
            }
            rest = mysql.query_db(query, data)
            return rest

    def showOne(self, id):
        mysql = connectToMySQL('books')
        query = 'SELECT * from books JOIN authors ON books.author_id = authors.id WHERE books.id = %(id)s'
        data = {
            'id' : id
        }
        result = mysql.query_db(query, data)
        return result

    def showReviews(self, id):
        mysql = connectToMySQL('books')
        query = 'SELECT * FROM books JOIN reviews ON books.id = reviews.book_id JOIN users ON reviews.user_id=users.id WHERE books.id=%(id)s'
        data = {
            'id' : id
        }
        result = mysql.query_db(query, data)
        return result

    def authors_list(self):
        mysql = connectToMySQL('books')
        query = 'SELECT * from authors'
        result = mysql.query_db(query)
        return result

    def addReview(self):
        mysql = connectToMySQL('books')
        query = 'INSERT INTO reviews (review, created_at, updated_at,book_id, user_id) VALUES (%(review)s,NOW(),NOW(),%(book_id)s, %(user_id)s)'
        data={
            'review':request.form['review'],
            'book_id':request.form['book_id'],
            'user_id':session['user_id']
        }
        mysql.query_db(query,data)
        return request.form['book_id']


    def showUser(self, id):
        mysql = connectToMySQL('books')
        query = 'SELECT * FROM users WHERE users.id=%(id)s'
        data={
            'id':id
        }
        result = mysql.query_db(query,data)
        return result

    def countReviews(self, id):
        mysql = connectToMySQL('books')
        query = 'SELECT  first_name, count(users.id) FROM users JOIN reviews ON reviews.user_id=users.id JOIN books ON reviews.book_id=books.id WHERE users.id=%(id)s'
        data={
            'id':id
        }
        result = mysql.query_db(query, data)
        return result

    def allReviews(self, id):
        mysql = connectToMySQL('books')
        query = 'SELECT title  FROM users JOIN reviews on reviews.user_id=users.id JOIN books on reviews.book_id=books.id WHERE users.id=%(id)s'
        data={
            'id':id
        }
        result = mysql.query_db(query, data)
        return result
        