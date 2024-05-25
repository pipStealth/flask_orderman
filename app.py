from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title="Pizza | Oderman")

@app.route('/menu', methods=["POST", "GET"])
def menu():
    return "Hello!"

app.run(host='0.0.0.0',port='80')