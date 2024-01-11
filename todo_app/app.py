from flask import Flask
from flask import render_template
from todo_app.data import session_items
from flask import request, redirect, url_for


from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/index', methods=['GET'])
def index():
    return render_template("index.html", itemsList = session_items.get_items())

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == "POST":
        session_items.add_item(request.form.get("title"))
        return redirect(url_for('index'))
    return render_template("add.html", itemsList = session_items.get_items())
