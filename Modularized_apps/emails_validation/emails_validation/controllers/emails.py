from flask import render_template, request, redirect, flash, session
from emails_validation.config.mysqlconnection import connectToMySQL
import re

from emails_validation.models.email import Email
email = Email()


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Emails:
    def index(self):
        return render_template('index.html')


    def validate(self):
        if len(request.form['email']) < 1:
            flash('Email cannot be blank.', 'error')
        elif not EMAIL_REGEX.match(request.form['email']):
            flash('Invalid email.', 'error')
            return redirect('/')
        return email.validate()
        

    def success(self):
        if 'email' not in session:
            flash('Illegal hack!')
            return redirect('/')
        else:
            result = email.success()
            return render_template('success.html', emails=result)

    
    def go_back(self):
        session.pop('email', None)
        return redirect('/')

    
    def delete(self, id):
        email.delete(id)
        return redirect('/success')
