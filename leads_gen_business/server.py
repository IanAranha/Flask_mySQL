from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route('/')
def index():
    mysql = connectToMySQL('lead_gen_business')
    all_clients = mysql.query_db(
        "SELECT CONCAT(clients.first_name,' ', clients.last_name) AS 'Name', COUNT(leads.leads_id) AS 'Leads' FROM clients JOIN sites ON sites.client_id = clients.client_id JOIN leads ON leads.site_id = sites.site_id GROUP BY CONCAT(clients.first_name,' ', clients.last_name)")
    return render_template('index.html', clients=all_clients)


if __name__ == '__main__':
    app.run(debug=True)
