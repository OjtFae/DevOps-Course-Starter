from flask import Flask
from flask import render_template
from todo_app.data import trello_items
from flask import request, redirect, url_for
from todo_app.flask_config import Config
import os
import requests

app = Flask(__name__)
app.config.from_object(Config())
app.run()
    
# deliberate redirect (308) to '/index' to return the actual home page (helps out with lost people - no cost to implementation)
@app.route('/')
def hello():
    return redirect(url_for('index'), 308) # using 308 allows browsers to cache the redirect

@app.route('/index', methods=['GET'])
def index():
    return render_template("index.html", itemsList = trello_items.get_items(app.config))

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == "POST":
        trello_items.add_item(app.config, request.form.get("title"))
        return redirect(url_for('index'), 303) # 303 see https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/303
    return render_template("add.html", itemsList = trello_items.get_items(app.config))

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == "POST":
        for itemId in list(request.form):
            trello_items.update_item(app.config, itemId, request.form.get(itemId))
    return render_template("update.html", itemsList = trello_items.get_items(app.config))

        
