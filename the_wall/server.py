from flask import Flask, render_template, redirect, request, session, flash
import re
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt 


app = Flask(__name__)
app.secret_key='Yankees suck'
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'email' in session:
        session.pop('email', None)
        return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/createUser', methods=['POST'])
def create():
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
    
    if '_flashes' in session.keys():
            return redirect("/")
    else:
        mysql = connectToMySQL('the_wall')
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        data = {'email' : request.form['email']}
        result = mysql.query_db(query, data)
        if result:
            flash("Email used. Use alternative or log in to proceed.", 'email')
            return redirect('/')
        else:
            try: 
                pw_hash = bcrypt.generate_password_hash(request.form['password'])
                mysql = connectToMySQL('the_wall')
                query = 'INSERT INTO users (first_name, last_name, email, password,created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s, NOW(), NOW())'
                data = {
                    'first_name': request.form['first_name'],
                    'last_name' : request.form['last_name'],
                    'email': request.form['email'],
                    'password_hash' : pw_hash
                }
                mysql.query_db(query, data)
                return redirect('/success')
            except ValueError:
                flash('You have some errors to correct', 'c_password')
                return redirect('/')


@app.route('/log_in', methods=['POST'])
def login():
    if len(request.form['email']) < 1:
        flash('Please enter email!', 'log_email')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email!", 'log_email')
        return redirect('/')
    if len(request.form['password']) < 1:
        flash('Please enter password.', 'log_password')
        return redirect('/')

    mysql = connectToMySQL('the_wall')
    query = 'SELECT * FROM users WHERE email = %(email)s;'
    data = {'email' : request.form['email']}
    result = mysql.query_db(query, data)
    if result:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            session['email'] = result[0]['email']
            session['user_id']=result[0]['id']
            session['first_name']=result[0]['first_name']
            return redirect('/login_success')
        else:
            flash('Incorrect password', 'log_password')
            return redirect('/')
    flash('Email not registered. Please register first', 'log_email')
    return redirect('/')

@app.route('/success')
def success():
    if 'email' not in session:
        ip_add = request.remote_addr
        return render_template('hack.html', ip=ip_add)
    else:
        flash('Registration successful. Log-in to proceed', 'log_email')
        return redirect('/')


@app.route('/login_success')
def log_in():
    if 'email' not in session:
        ip_add = request.remote_addr
        return render_template('hack.html', ip=ip_add)
    else:
        mysql = connectToMySQL('the_wall')
        queryA = "SELECT * FROM messages JOIN users ON messages.written_by = users.id WHERE messages.written_for = %(user)s ORDER BY messages.created_at DESC"
        dataA = {
             'user' : session['user_id']
         }
        all_messages = mysql.query_db(queryA, dataA)

        mysql = connectToMySQL('the_wall')
        queryB = "SELECT * FROM users WHERE users.email != %(email)s;"
        dataB = {
            'email' : session['email']
        }
        all_other_users = mysql.query_db(queryB, dataB)

        mysql = connectToMySQL('the_wall')
        queryC = "SELECT COUNT(*) FROM messages WHERE written_for = %(user)s"
        dataC = {
             'user' : session['user_id']
         }
        messageCount = mysql.query_db(queryC, dataC)
        counter = messageCount[0]['COUNT(*)']

        mysql = connectToMySQL('the_wall')
        queryD = "SELECT COUNT(*) FROM messages WHERE messages.written_by = %(user)s"
        dataD = {
             'user' : session['user_id']
         }
        messageCount = mysql.query_db(queryD, dataD)
        counter2 = messageCount[0]['COUNT(*)']

    
        return render_template('success.html',myMessages=all_messages, all_other_users=all_other_users, messageCount=counter,sent_messages=counter2)



@app.route('/delete/<id>', methods=['GET','POST'])
def delete(id):
    if 'email' not in session:
        ip_add = request.remote_addr
        return render_template('hack.html', ip=ip_add)
    else:
        mysql = connectToMySQL('the_wall')
        query='DELETE FROM messages WHERE messages.message_id = %(message_id)s'
        data = {
            'message_id' : id
        }
        mysql.query_db(query, data)
        return redirect('/login_success')
    

@app.route('/log_out' , methods=['POST'])
def log_out():
    session.pop('email', None)
    return redirect('/')


@app.route('/add_message', methods=['POST'])
def add_message():
    if len(request.form['message']) < 1:
        flash('You must include a message', 'message')
    mysql = connectToMySQL('the_wall')
    query = 'INSERT INTO messages (message_text, written_for, created_at, updated_at, written_by) VALUES (%(message)s, %(written_for)s, NOW(),NOW(), %(written_by)s)'
    data = {
        'message' : request.form['message'],
        'written_for': request.form['message_recipant'],
        'written_by': session['user_id']
        }
    mysql.query_db(query, data)
   

    return redirect('/login_success')
if __name__ == '__main__':
    app.run(debug=True)