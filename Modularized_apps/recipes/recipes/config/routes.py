from recipes import app
from recipes.config.mysqlconnection import connectToMySQL
from recipes.controllers.users import Users

app.secret_key='Yankees suck'

users=Users()

@app.route('/')
def index():
    return users.index()

@app.route('/createUser', methods=['POST'])
def createUser():
    return users.createUser()

@app.route('/registration_success')
def success():
    return users.createUserSuccess()

@app.route('/log_in', methods=['POST'])
def log_in():
    return users.log_in()

@app.route('/dashboard')
def dashboard():
    return users.dashboard()

@app.route('/create')
def create():
    return users.create()

@app.route('/createRecipe', methods=['POST'])
def createRecipe():
    return users.createRecipe()

@app.route('/createRecipeSuccess')
def createRecipeSuccess():
    return users.createRecipeSuccess()

@app.route('/logout')
def logout():
    return users.logout()

@app.route('/review')
def review():
    return users.review()

@app.route('/show/<id>')
def show(id):
    return users.show(id)

@app.route('/delete/<id>')
def delete(id):
    return users.delete(id)


