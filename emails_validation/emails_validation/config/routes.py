from emails_validation import app
from emails_validation.controllers.emails import Emails


emails = Emails()


app.secret_key = "Yankees Suck"


@app.route('/')
def index():
    return emails.index()
    

@app.route('/validate', methods=['POST'])
def validate():
    return emails.validate()


@app.route('/success')
def success():
    return emails.success()


@app.route('/go_back')
def go_back():
    return emails.go_back()


@app.route('/delete/<id>')
def delete(id):
    return emails.delete(id)