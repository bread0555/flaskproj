from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route("/", methods=("GET","POST")) # need to create sign up button
def login():
    if request.method == "POST":
        name = request.form.get('name', '').strip()
        password = request.form.get('password', '').strip()
        if not name or not password:
            return render_template("head.html") + """<span style = "font-size: 30px; font-weight: bold;">Login</span><br><span style = "color: #fa4b4b; font-size: 15px;">Fields cannot be empty</span>""" + render_template("auth_form.html", auth_form = "") + """<a href="/signup" style="text-decoration: none;">Signup</a>"""
        sql = "SELECT id FROM users WHERE name='" + request.form.get('name') + "' AND password='" + request.form.get('password') + "'"
        result = select(sql)
        if len(result) > 0:
            return redirect("/posts/userid=" + str(result[0][0]), code = 307)
        else:
            return render_template("head.html") + """<span style = "font-size: 30px; font-weight: bold;">Login</span><br><span style = "color: #fa4b4b; font-size: 15px;">Invalid credentials</span>""" + render_template("auth_form.html", auth_form = "") + """<a href="/signup" style="text-decoration: none;">Signup</a>""", 401
    else:
        return render_template("head.html") + """<span style = "font-size: 30px; font-weight: bold;">Login</span>""" + render_template("auth_form.html", auth_form = "") + """<a href="/signup" style="text-decoration: none;">Signup</a>"""


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get('name', '').strip()
        password = request.form.get('password', '').strip()
        sql = "SELECT id FROM users WHERE name='" + request.form.get('name') + "' AND password='" + request.form.get('password') + "'"
        result = select(sql)
        if result == 0:
            if not name or not password:
                return render_template("head.html") + """<span style = "font-size: 30px; font-weight: bold;">Signup</span><br><span style = "color: #fa4b4b; font-size: 15px;">Fields cannot be empty</span>""" + render_template("auth_form.html", auth_form = "signup") + """<a href="/" style="text-decoration: none;">Login</a>"""
            sql = f"INSERT INTO users (name, password) values ('{name}', '{password}')"
            insert(sql)
            return redirect("/posts/userid=" + str(result[0][0]), code = 307)
        else:
            return render_template("head.html") + """<span style = "font-size: 30px; font-weight: bold;">Signup</span><br><span style = "color: #fa4b4b; font-size: 15px;">User already exists</span>""" + render_template("auth_form.html", auth_form = "signup") + """<a href="/" style="text-decoration: none;">Login</a>"""
    else:
        return render_template("head.html") + """<span style = "font-size: 30px; font-weight: bold;">Signup</span>""" + render_template("auth_form.html", auth_form = "signup") + """<a href="/" style="text-decoration: none;">Login</a>"""


@app.route("/posts/userid=<userid>", methods=("GET","POST"))
def all_posts(userid):
    sql = "SELECT posts.id, users.id, users.name, posts.title, posts.content FROM posts, users WHERE posts.authorid = users.id"
    posts = select(sql)
    html = render_template("head.html", userid = userid) + render_template("header.html", userid = userid) + """<span style = "font-size: 30px; font-weight: bold;">Posts</span>"""
    if len(posts) > 0:
        for post in posts:
            html = html + render_template("post_banner.html", authorid = post[1], postid = post[0], author = post[2], title = post[3], content = post[4], userid = userid)
    else:
        html = render_template("head.html", userid = userid) + render_template("header.html", userid = userid) + """<span style = "color: #fa4b4b; font-size: 15px;">There are no posts. Make the first one!</span>"""
    return html + render_template("footer.html", userid = userid)


@app.route("/posts/userid=<userid>/new", methods=["GET", "POST"])
def new_post(userid):
    if request.method == "POST":
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title or not content:
            return render_template("head.html", userid = userid) + render_template("header.html", userid = userid) + """<span style = "font-size: 30px; font-weight: bold;">New post</span><br><span style = "color: #fa4b4b; font-size: 15px;">Fields cannot be empty</span>""" + render_template("new_post.html", userid = userid) + render_template("footer.html", userid = userid)
        else:
            sql = "SELECT id FROM posts WHERE title = '" + request.form.get('title') + "' AND content = '" + request.form.get('content') + "' AND authorid = {}".format(userid)
            result = select(sql)
            if len(result) < 0:
                sql = f"INSERT INTO posts (authorid, title, content) values ('{userid}', '{title}', '{content}')"
                insert(sql)
                return redirect(f"/posts/userid=" + str(result[0][0]), code = 307)
            else:
                return render_template("head.html", userid = userid) + render_template("header.html", userid = userid) + """<span style = "font-size: 30px; font-weight: bold;">New post</span><br><span style = "color: #fa4b4b; font-size: 15px;">Post exists already. Create a new one/span>""" + render_template("new_post.html", userid = userid) + render_template("footer.html", userid = userid)
    else:
        return render_template("head.html", userid = userid) + render_template("header.html", userid = userid) + """<span style = "font-size: 30px; font-weight: bold;">New post</span>""" + render_template("new_post.html", userid = userid) + render_template("footer.html", userid = userid)


@app.route("/posts/userid=<userid>/postid=<postid>")
def post(userid, postid):
    sql = f"SELECT posts.id, users.id, users.name, posts.title, posts.content FROM posts, users WHERE posts.authorid = users.id AND {postid} = posts.id"
    post = select(sql)
    if len(post) > 0:
        html = render_template("head.html", userid = userid) + render_template("header.html", userid = userid) + render_template("post_layout.html", authorid = post[0][0], postid = post[0][1], author = post[0][2], title = post[0][3], content = post[0][4], userid = userid)  + render_template("footer.html", userid = userid)
    else:
        html = render_template("head.html", userid = userid) + render_template("header.html", userid = userid) + """<span style = "color: #fa4b4b; font-size: 15px;">This post does not exist</span>""" + render_template("footer.html", userid = userid)
    return html


@app.route("/posts/userid=<userid>/authors", methods=["GET", "POST"])
def authors(userid):
    sql = "SELECT users.id, users.name FROM users"
    users = select(sql)
    sql = "SELECT posts.id, posts.title, posts.authorid FROM posts"
    posts = select(sql)
    html = render_template("head.html", userid = userid) + render_template("header.html", userid = userid) + """<span style = "font-size: 30px; font-weight: bold;">Authors</span>"""
    if len(users) > 0:
        for user in users:
            post_count = 0
            post_titles = ""
            for post in posts:
                if post[2] == user[0]:
                    post_count += 1
                    post_titles += post[1] + ", "
            html = html + render_template("author_banner.html", userid = user[0], name = user[1], post_titles = post_titles, post_count = post_count)
    return html + render_template("footer.html", userid = userid)


@app.route("/posts/userid=<userid>/authorid=<authorid>", methods=["GET", "POST"])
def author_posts(userid, authorid):
    sql = f"SELECT posts.id, users.id, users.name, posts.title, posts.content FROM posts, users WHERE posts.authorid = {authorid} AND users.id = posts.authorid"
    posts = select(sql)
    sql = f"SELECT users.id, users.name FROM users WHERE users.id = {authorid}"
    user = select(sql)
    html = render_template("head.html", userid = userid) + render_template("header.html", userid = userid) + f"""<span style = "font-size: 30px; font-weight: bold;">Posts by: {user[0][1]}</span>"""
    if len(posts) > 0:
        for post in posts:
            html = html + render_template("post_banner.html", authorid = post[1], postid = post[0], author = post[2], title = post[3], content = post[4], userid = userid)
        return html + render_template("footer.html", userid = userid)
    else:
        html = html + """<span style = "color: #fa4b4b; font-size: 15px;">This author has made no posts</span>""" + render_template("footer.html", userid = userid)
    return html


@app.route("/posts/userid=<userid>/search", methods=["GET", "POST"])
def search(userid):
    if request.method == "POST":
        search = request.form.get('search', '').strip()
        if not search:
            return render_template("head.html", userid=userid) + render_template("header.html", userid=userid) + """<span style="font-size: 30px; font-weight: bold;">Search</span><br><span style="color: #fa4b4b; font-size: 15px;">Field cannot be empty</span>""" + render_template("search.html", userid=userid) + render_template("footer.html", userid=userid)
        return redirect(f"/posts/userid={userid}/search={search}", code=302)
    return render_template("head.html", userid=userid) + render_template("header.html", userid=userid) + """<span style="font-size: 30px; font-weight: bold;">Search</span>""" + render_template("search.html", userid=userid) + render_template("footer.html", userid=userid)


@app.route("/posts/userid=<userid>/search=<keyword>")
def search_posts(userid, keyword):
    sql = f"SELECT posts.id, users.id, users.name, posts.title, posts.content FROM posts, users"
    posts = select(sql)
    if len(posts) > 0:
        html = ""
        for post in posts:
            if keyword in post[2] or keyword in post[3] or keyword in post[4]:
                html = html + render_template("post_banner.html", authorid = post[1], postid = post[0], author = post[2], title = post[3], content = post[4], userid = userid)
        if html:
            return render_template("head.html", userid = userid) + render_template("header.html", userid = userid) + f"""<span style = "font-size: 30px; font-weight: bold;">Search for: '{keyword}'</span>""" + html + render_template("footer.html", userid = userid)
        else:
            return render_template("head.html", userid = userid) + render_template("header.html", userid = userid) + f"""<span style = "font-size: 30px; font-weight: bold;">Search for: '{keyword}'</span><br><span style = "color: #fa4b4b; font-size: 15px;">Your query couldn't be found</span>""" + render_template("footer.html", userid = userid)
    else:
        return render_template("head.html", userid = userid) + render_template("header.html", userid = userid) + f"""<span style = "font-size: 30px; font-weight: bold;">Search for: '{keyword}'</span><br><span style = "color: #fa4b4b; font-size: 15px;">There are no posts. Make the first one!</span>""" + render_template("footer.html", userid = userid)


@app.route("/<url>")
def anotherURL(url):
    #Give a 'friendly' page missing error.
    html = "<br><p>HTTP error 404: URL /" + url + " does not exist</p>"
    return render_template("head.html") + html + render_template("footer.html")

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