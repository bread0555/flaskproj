from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def home():
    return "Willkommen"

@app.route("/select")
def select():
    connection = connect()
    records = connection.execute("select * from users").fetchall()
    connection.close()
    output = ""
    for user in records:
        output = output + render_template('user', user = user)
    return output

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return login_form()
    else:
        # user has POSTed their name and password
        name = request.form['name']
        password = request.form['password']
        connection = connect()
        records = connection.execute("SELECT count(*) from users WHERE name = '"+name+"' and password ='"+password+"';")
        connection.close()
        if str(records[0][0]) == 1:
            # successful login
            return "Successful login"
        else:
            # failed login
            return "Incorrect login details - try again" + login_form()

def login_form():
    html = "<form action = '/login' method = 'POST' >"
    html = html + "<input name='name' id='name' />"
    html = html + "<input password ='name' id='password' />"
    html = html + "<input type='submit'>Login</button>"
    html = html + "</form>"
    return html



@app.route("/select/<condition>")
def select_with_condition(condition):
    connection = connect()
    records = connection.execute("select * from users where " + condition).fetchall()
    connection.close()
    output = ""
    for user in records:
        output = output + render_template('user', user = user)
    return output

@app.route("/add/<user>")
def add_user(user):
    name = user.split(", ")[0]
    password = user.split(", ")[1]
    description = user.split(", ")[2]
    connection = connect()
    connection.execute("insert into users (name, password, description) values ")


def connect():
    import sqlite3
    connection = sqlite3.connect('database.sqlite')
    return connection.cursor()



app.run(port = 5555)