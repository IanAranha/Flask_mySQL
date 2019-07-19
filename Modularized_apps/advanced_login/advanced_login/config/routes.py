from advanced_login import app
from advanced_login.config.mysqlconnection import connectToMySQL
from advanced_login.controllers.users import Users

app.secret_key='Yankees suck'

users=Users()

@app.route('/')
def index():
    return users.index()

@app.route('/createUser', methods=['POST'])
def createUser():
    return users.createUser()

@app.route('/success')
def userRegistered():
    return users.userRegistered()

@app.route('/log_in', methods=['POST'])
def login():
    return users.log_in()

@app.route('/login_success')
def userLogin():
    return users.login_success()

@app.route('/admin')
def admin():
    return users.admin()
   
@app.route('/user')
def user():
    return users.user()
    
@app.route('/remove/<id>', methods=['POST'])
def remove(id):
    return users.remove(id)

@app.route('/remove_admin/<id>', methods=['POST'])
def remove_admin(id):
    return users.remove_admin(id)

@app.route('/make_admin/<id>', methods=['POST'])
def make_admin(id):
    return users.make_admin(id)
    
@app.route('/hack')
def hack():
    return users.hack()

@app.route('/log_off')
def log_off():
    return users.log_off()