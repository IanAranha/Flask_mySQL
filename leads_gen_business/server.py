from flask import Flask, render_template, require, redirect
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route('/')
def index():
    mysql = connectToMySQL('lead_get_business')
    all_clients = mysql.query_db('SELECT * FROM clients')
    return render_template('index.html', clients = all_clients)


if __name__ == '__main__':
    app.run(debug=True)
