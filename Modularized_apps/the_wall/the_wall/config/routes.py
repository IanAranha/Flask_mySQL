from the_wall import app

from the_wall.controllers.users import Users

users=Users()

@app.route('/')
def index():
    return users.index()

@app.route('/createUser', methods=['POST'])
def createUser():
    return users.createUser()

@app.route('/registration_success')
def registration_success():
    return users.registration_success()

@app.route('/log_in', methods=['POST'])
def log_in():
    return users.log_in()

@app.route('/dashboard')
def dashboard():
    return users.dashboard()

@app.route('/post_message', methods=['POST'])
def post_message():
    return users.post_message()

@app.route('/message_success')
def message_success():
    return users.message_success()

@app.route('/logout')
def logout():
    return users.logout()

@app.route('/post_comment/<id>', methods=['POST'])
def post_comment(id):
    print(id)
    return users.post_comment(id)

@app.route('/comment_success')
def comment_success():
    return users.comment_success()