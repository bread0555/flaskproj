from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route("/", methods=("GET","POST"))
def login():
    if request.method == "POST":
        name = request.form.get('name', '').strip()
        password = request.form.get('password', '').strip()
        if not name or not password:
            return "Name and password cannot be empty"
        sql = "SELECT id FROM users WHERE name='"+request.form.get('name')+"' AND password='"+request.form.get('password')+"';"
        result = select(sql)
        if len(result) > 0:
            return redirect("/userid=" + str(result[0][0]), code = 307)
        else:
            return "Invalid credentials", 401
    else:
        return login_form()


def login_form():
    return render_template("head.html") + render_template("header.html") + render_template("login.html") + render_template("footer.html")


@app.route("/select")
def select():
    connection = connect()
    records = connection.execute("select * from users").fetchall()
    connection.close()
    output = ""
    for user in records:
        output = output + render_template('user', user = user)
    return output


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

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return signup_form()
    else:
        name = request.form['name']
        password = request.form['password']
        description = request.form['description']
        if name and password and description:
            connection = connect()
            connection.execute("INSERT INTO users (name, password, description) values ('"+name+"', '"+password+"', '"+description+"');")
            connection.close()
        else:
            return "Unable to signup, complete all fields" + signup_form
    
    if request.method == 'POST':
        print("Welcome")


def signup_form():
    html = "<form action = '/login' method = 'POST' >"
    html = html + "<input name='name' id='name' />"
    html = html + "<input password ='name' id='password' />"
    html = html + "<input description ='name' id='description' />"
    html = html + "<input type='submit'>Submit</button>"
    html = html + "</form>"
    return render_template("head.html") + html + render_template("footer.html")



@app.route("/<url>")
def anotherURL(url):
    #Give a 'friendly' page missing error.
    html = "<br><p>HTTP error 404: URL /" + url + " does not exist</p>"
    return render_template("head.html") + render_template("header.html") + html + render_template("footer.html")

def select(sql):
    #execute a given SQL query anbd return the results
    print(sql)
    connection = connect()
    cursor = connection.cursor()
    result = cursor.execute(sql).fetchall()
    connection.close()
    return result

def insert(sql):
    print(sql)
    connection = connect()
    connection.execute(sql)
    connection.commit()

def connect():
    #connect to the database
    import sqlite3
    connection = sqlite3.connect('database.sqlite')
    return connection

app.run(port = 5555)