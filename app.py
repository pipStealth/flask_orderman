from flask import Flask, render_template, request, send_file

app = Flask(__name__)

navMenu = [
    {"title": "Home",       "endpoint": "home"},
    {"title": "Menu",       "endpoint": "menu"},

]

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', CSSpath="../static/css/404.css"), 404

@app.route('/')
def home():
    return render_template('index.html', title="Pizza | Oderman", menu=navMenu, )

@app.route('/menu', methods=["POST", "GET"])
def menu():
    return "Hello!"

if __name__ == '__main__':
    app.debug = True
    app.run()