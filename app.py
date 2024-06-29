from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, g
import os
import sqlite3
import hashlib
from DataBase import DataBase
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from UserData import UserLogin

# =============================================================================
# Configuration
# =============================================================================

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'main.db')))
app.secret_key = 'your_secret_key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "You need sign in to site for read this page!"
login_manager.login_message_category = "error"
the_name = None

# =============================================================================
# DataBase
# =============================================================================

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)

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

def aIsLogged():
    return True if session.get('admin_logged') else False

# =============================================================================
# Errors' routers
# =============================================================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', menu=dbase.getMenu(), item=dbase.getUserByEmail(current_user.getEmail()) if current_user.is_authenticated else None), 404

# =============================================================================
# Routers
# =============================================================================

@app.route('/')
def home():
    return render_template('index.html', title="Pizza | Oderman", menu=dbase.getMenu(), item=dbase.getUserByEmail(current_user.getEmail()) if current_user.is_authenticated else None)

@app.route('/menu', methods=["POST", "GET"])
@login_required
def menu():

    if request.method == "POST":
        pass

    return render_template("menu.html", title="Oderman | Menu", menu=dbase.getMenu(), food=dbase.getFood(), item=dbase.getUserByEmail(current_user.getEmail()))

@app.route("/food/<alias>")
@login_required
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

    return render_template("alogin.html", title="Odermen | Alogin", menu=dbase.getMenu(), item=dbase.getUserByEmail(current_user.getEmail()) if current_user.is_authenticated else None)

@app.route("/admin", methods=["POST", "GET"])
def admin():
    if not aIsLogged():
        return redirect(url_for("alogin"))

    return render_template("admin.html", title="Oderman | Admin", menu=dbase.getMenu(), item=dbase.getUserByEmail(current_user.getEmail()) if current_user.is_authenticated else None)

@app.route("/addFood", methods=["POST", "GET"])
def routeFood():
    if not aIsLogged():
        return redirect(url_for("alogin"))

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]
        category = request.form["category"]
        print(name, category)
        dbase.addFood(title=name, price=price, description=description, type=category)
        flash("Успішно!", "success")

    return render_template("addFood.html", title="Oderman | AddFood", menu=dbase.getMenu(), item=dbase.getUserByEmail(current_user.getEmail()) if current_user.is_authenticated else None)

@app.route("/registration", methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        fullname = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        phone = request.form["phone"]
        account = dbase.addAccount(fullname=fullname, email=email, password=password, phone=phone)
        flash("Успішно!", "success") if account else flash("This email have used already!", "error")

    return render_template("addUser.html", title="Oderman | Registration", menu=dbase.getMenu(), item=dbase.getUserByEmail(current_user.getEmail()) if current_user.is_authenticated else None)

@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['password'], request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("home"))

        flash("The password or login not correct", "error")

    return render_template("login.html", menu=dbase.getMenu(), title="Authorization", item=dbase.getUserByEmail(current_user.getEmail()) if current_user.is_authenticated else None)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Success! You log out from account!", "success")
    return redirect(url_for('login'))


@app.route('/profile/<alias>', methods=["GET"])
@login_required
def profile(alias):
    if not int(current_user.get_id()) == int(alias):
        return redirect(url_for('home'))
    user_id = current_user.get_id()
    orders = dbase.getOrdersByUserId(user_id)
    fullprice = 0
    for i in orders:
        fullprice += float(i['price'])
    return render_template("profile.html", menu=dbase.getMenu(), fullprice=fullprice, item=dbase.getUserByEmail(current_user.getEmail()), orders=orders, title=f"Profile | {current_user.getName()}")

@app.route("/food/<alias>/order", methods=["POST", "GET"])
@login_required
def orderFood(alias):
    if request.method == "POST":

        item = dbase.getFoodByAlias(alias)
        if item:
            dbase.userOrder(current_user.get_id(), item['id'])
            flash("Order placed successfully!", "success")
        else:
            flash("Food item not found", "error")
    return redirect(url_for('home'))

@app.route("/addGift", methods=["POST", "GET"])
def routeGift():
    if not aIsLogged():
        return redirect(url_for("alogin"))

    if request.method == "POST":
        name = request.form["name"]
        amount = request.form["amount"]
        limit = request.form["limit"]
        dbase.addGift(promo=name, amount=amount, count=limit)
        flash("Успішно!", "success")

    return render_template("addGift.html", title="Oderman | AddFood", menu=dbase.getMenu(), item=dbase.getUserByEmail(current_user.getEmail()) if current_user.is_authenticated else None)

@app.route("/gift", methods=["POST", "GET"])
@login_required
def useGift():
    if request.method == "POST":
        name = request.form.get("promo")
        if name:
            gif = dbase.useGift(name, current_user.get_id())
            flash("Success", "success") if gif else flash("This gift has used already!", "error")

    return render_template("useGift.html", title="Oderman | AddFood", menu=dbase.getMenu(), item=dbase.getUserByEmail(current_user.getEmail()) if current_user.is_authenticated else None)

# =============================================================================
# Operations setup
# =============================================================================

if __name__ == '__main__':
    app.debug = True
    app.run()
