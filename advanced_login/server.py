from flask import Flask, render_template, request, redirect, session, flash
import re
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt 

app = Flask(__name__)
app.secret_key='Yankees suck'
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

@app.route('/')

#First make sure that the session contains nothing (erase previous user).
def index():
    session.clear()
    return render_template('index.html')





#This POST route is hit when "CLICK TO REGISTER" is clicked on index page
@app.route('/createUser', methods=['POST'])

#This method creates a new user and adds to database. 
#Method validates each field
#Validates the first name field making sure ipput is not blank and contains only letters.
#Validate the last name field making sure input is not blank and contains only letters.
#Validate the email field making sure inpupt is not blank and is a valid email.
#Validate the password field making sure input in not blank and is more than 8 characters   
#Validate the confirm password field making sure input is not blank and matches password field

def createUser():
    if len(request.form['first_name']) < 1:
        flash('First name cannot be blank', 'first_name')
    elif not NAME_REGEX.match(request.form['first_name']):
        flash('First name can only contain alphabets', 'first_name')


    if len(request.form['last_name']) < 1:
        flash('Last name cannot be blank', 'last_name')
    elif not NAME_REGEX.match(request.form['last_name']):
        flash('Last name can only contain alphabets', 'last_name')

    
    if len(request.form['email']) < 1:
        flash('Email cannot be blank', 'email')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email", 'email')


    if len(request.form['password']) < 1:
        flash('Password cannot be blank.', 'password')
    elif len(request.form['password']) < 8:
        flash('Password must be 8 or more characters.', 'password')


    if len(request.form['c_password']) < 1:
        flash('Confirm password!', 'c_password')
    elif request.form['password'] != request.form['c_password']:
        flash ('Passwords do not match', 'c_password')
    

    #If there any validations fail, display them and redirect to index.
    if '_flashes' in session.keys():
        return redirect("/")
    
    #If validation passes, check to see if current user exists in DB
    else:
        #Establish a connector to the DB
        mysql = connectToMySQL('advanced_login')

        #Set up query to check DB for current email
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        data = {'email' : request.form['email']}
        result = mysql.query_db(query, data)
        
        #If the query returns a result, user has already registered.
        if result:
            flash("Email used. Use alternative or log in to proceed.", 'email')
            return redirect('/')
        else:
            #If the query returns no results, enter user details into DB
            try:
                #Hash the password
                pw_hash = bcrypt.generate_password_hash(request.form['password'])
                
                #Connect to the DB
                mysql = connectToMySQL('advanced_login')

                #Create an insert query and all incoming form data is bound to the query and injected into DB.
                query = 'INSERT INTO users (first_name, last_name, email, password,user_level, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s, %(user_level)s, NOW(), NOW())'
                data = {
                    'first_name': request.form['first_name'],
                    'last_name' : request.form['last_name'],
                    'email': request.form['email'],
                    'password_hash' : pw_hash,
                    'user_level' : 1
                    }
                mysql.query_db(query, data)

                #If successful, redirect user to now login
                return redirect('/success')
            except ValueError:
                #If there is a database error, return to page.
                flash('You have some errors to correct', 'c_password')
                return redirect('/')



#This route is hit when the user clicks the 'Log in' button
@app.route('/log_in', methods=['POST'])
def login():
    #Check the validity of the email
    if len(request.form['log_email']) < 1:
        flash('Please enter email!', 'log_email')
    elif not EMAIL_REGEX.match(request.form['log_email']):
        flash("Invalid email!", 'log_email')
        return redirect('/')
    
    #Check the validity of the password
    if len(request.form['log_password']) < 1:
        flash('Please enter password.', 'log_password')
        return redirect('/')

    #Connect to the DB
    mysql = connectToMySQL('advanced_login')

    #Create a query to search the DB for the incoming email
    query = 'SELECT * FROM users WHERE email = %(email)s;'
    data = {'email' : request.form['log_email']}
    result = mysql.query_db(query, data)
    
    ## If the email is in the DB
    if result:
        print(result)

        #Check the validity of the password
        if bcrypt.check_password_hash(result[0]['password'], request.form['log_password']):
            #If password is valid, move to the correct page
            #Put data into session for validation purposes
            session['email'] = result[0]['email']
            session['user_id']=result[0]['id']
            session['first_name']=result[0]['first_name']
            session['user_level'] = result[0]['user_level']
            return redirect('/login_success')
        else:
            #If passwords don't match, redirect
            flash('Incorrect password', 'log_password')
            return redirect('/')

    #If no result, then user not registered
    flash('Email not registered. Please register first', 'log_email')
    return redirect('/')





@app.route('/success')
#If this route is hit, inform the user they have registered and need to log in.
def userRegistered():
    flash("User successfully registered. Please log-in.", 'message')
    return redirect('/')




@app.route('/login_success')
def userLogin():
    #This method does several things
    #checks that the user has successfully logged in and if not,redirects them to the hack page
    if 'email' not in session:
        return redirect('/hack')
    # checks the user's admin level and directs to the appropriate page
    if session['user_level'] == 9:
        return redirect('/admin')
    else:
        return redirect('/user')



@app.route('/admin')
def admin():
    #This method checks that the user is legally registered and then proceeds to populate the 
    #html with data pulled from DB
    if 'user_level' not in session:
        return redirect('/hack')
    elif session['user_level'] != 9:
        return redirect('/hack')
    else:
        #Connect to the DB
        mysql = connectToMySQL('advanced_login')

        #Create a query to grab all the user data from the db
        result = mysql.query_db('SELECT * FROM users')
    
        #pass all the user data to the html page
        return render_template('admin.html', users=result)




@app.route('/user')
def user():
    #This method directs normal users to the appropriate page
    if 'email' not in session:
        return redirect('/hack')
    else:
        return render_template('user.html')



@app.route('/remove/<id>', methods=['POST'])
def remove(id):
    #When the remove button is clicked, the user is removed from the data-base.
    #Connect to the DB
    mysql = connectToMySQL('advanced_login')

    #Create a query to delete the user data from the db
    query = 'DELETE from users WHERE id = %(id)s'
    data = {
        'id' : id
    }
    mysql.query_db(query,data)
    
    #pass all the user data to the html page   
    return redirect('/admin')



@app.route('/remove_admin/<id>', methods=['POST'])
def remove_admin(id):
    #Connect to the DB
    mysql = connectToMySQL('advanced_login')

    #Create a query to delete the user data from the db
    query = 'UPDATE users SET user_level = 1 WHERE id = %(id)s'
    data = {
        'id' : id
    }
    mysql.query_db(query,data)

    return redirect('/admin')

@app.route('/make_admin/<id>', methods=['POST'])
def make_admin(id):
    #Connect to the DB
    mysql = connectToMySQL('advanced_login')

    #Create a query to delete the user data from the db
    query = 'UPDATE users SET user_level = 9 WHERE id = %(id)s'
    data = {
        'id' : id
    }
    mysql.query_db(query,data)

    return redirect('/admin')

@app.route('/hack')
def hack():
    ##Any attempt at hack leads to this page.
    return render_template('hack.html')



@app.route('/log_off')
def log_off():
    #When logging off, all stored variables are deleted and app goes to log in page
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)