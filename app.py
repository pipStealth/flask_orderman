from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, g
import os
import sqlite3
from DataBase import DataBase

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'main.db')))
app.secret_key = 'your_secret_key'  # Ensure you have a secret key for sessions

# Database setup
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

dbase = None

@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = DataBase(db)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

def logout():
    return session.pop('admin_logged', None)

def aIsLogged():
    return True if session.get('admin_logged') else False

# Error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', menu=dbase.getMenu()), 404

# Routes
@app.route('/')
def home():
    return render_template('index.html', title="Pizza | Oderman", menu=dbase.getMenu())

@app.route('/menu', methods=["POST", "GET"])
def menu():
    if request.method == "POST":
        pass

    return render_template("menu.html", title="Oderman | Menu", menu=dbase.getMenu(), food=dbase.getFood())

@app.route("/food/<alias>")
def showFood(alias):
    item = dbase.getFoodByAlias(alias)
    if not item:
        abort(404)

    return render_template('food.html', menu=dbase.getMenu(), item=item, name="Pizza")

@app.route("/alogin", methods=["POST", "GET"])
def alogin():
    if aIsLogged():
        return redirect(url_for('admin'))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "123123":
            session['admin_logged'] = True
            return redirect(url_for("admin"))
        else:
            flash("Incorrect username or password", "error")

    return render_template("alogin.html", title="Odermen | Alogin", menu=dbase.getMenu())

@app.route("/admin", methods=["POST", "GET"])
def admin():
    if not aIsLogged():
        return redirect(url_for("alogin"))

    return render_template("admin.html", title="Oderman | Admin", menu=dbase.getMenu())

@app.route("/addFood", methods=["POST", "GET"])
def routeFood():
    if not aIsLogged():
        return redirect(url_for("alogin"))
    
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]

        dbase.addFood(name=name, price=price, description=description)
        flash("Успішно!", "success")

    return render_template("addFood.html", title="Oderman | AddFood", menu=dbase.getMenu()) 

if __name__ == '__main__':
    app.debug = True
    app.run()
