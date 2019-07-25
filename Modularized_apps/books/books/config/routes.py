from books import app

from books.controllers.users import Users

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

@app.route('/books')
def books():
    return users.books()

@app.route('/logout')
def logout():
    return users.logout()

@app.route('/add_book')
def add_book():
    return users.add_book()

@app.route('/addbook', methods=['POST'])
def addbook():
    return users.addbook()

@app.route('/showOne/<id>')
def showOne(id):
    return users.showOne(id)

@app.route('/addreview', methods=['POST'])
def addReview():
    return users.addReview()

@app.route('/users/<id>')
def showUsers(id):
    return users.showUser(id)