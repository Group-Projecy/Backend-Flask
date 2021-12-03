from flask import Flask, render_template, session, url_for, redirect, flash, jsonify, request
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from functools import wraps

from flask_sqlalchemy import SQLAlchemy

import json
import os
import time, threading

# we want access to the functionality defined in the my_db.py file
#from . import my_db

app = Flask(__name__)

# set these up and test them - user - root ??
# set them up in ssl wsgi environment file
#mysql_user = os.getenv('mysql_user')
#mysql_password = os.getenv('mysql_password')

#app.config['SQLALCHEMY_DATABASE_URL']='mysql://'+mysql_user+':'+mysql_password+'@localhost/sd3biot22'
#app.config['SQL_TRACK_MODIFICATIONS'] = False;
#db = SQLAlchemy(app)

# add environment variables to ubuntu instance
#facebook_app_id = os.getenv("sd3bFacebookApp")
#facebook_app_secret = os.getenv("sd3bFacebookSecret")

#facebook_blueprint = make_facebook_blueprint(client_id=facebook_app_id, client_secret=facebook_app_secret, redirect_url='/facebook_login')
#app.register_blueprint(facebook_blueprint, url_prefix='/facebook_login')

alive = 0
data = {}


@app.route('/')
def index():
    # return render_template("login.html")
    return render_template("adminHome.html")

@app.route('/facebok_login')
def facebook_login():
    if not facebook.authorized:
        # this will redirect to facebook login
        return redirect((url_for('facebook.login')))
    account_info = facebook.get('/me')
    if account_info.ok:
        print("Access token", facebook.access_token)
        me = account_info.json()
        session['logged_in'] = True
        session['facebook_token'] = facebook.access_token
        session['user'] = me['name']
        session['user_id'] = me['id']
        return redirect(url_for('main'))
    return redirect(url_for('login'))

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)

        flash("Please log in first")
        return redirect(url_for('login'))
    return wrapper

@app.route('/main')
@login_required
def main():
    flash(session['user'])
    my_db.add_user_and_login(session['user'], int(session['user_id']))
    my_db.view_all()
    return render_template("index.html")

def clear_user_session():
    session['facebook_token'] = None
    session['user'] = None
    session['user_id'] = None

# @app.route("/login")
# def login():
#     clear_user_session()
#     return render_template("login.html")

@app.route("/logout")
def logout():
    flash("You just logged out!")
    my_db.user_logout(session['user_id'])
    my_db.view_all()
    clear_user_session()
    return redirect(url_for('login'))

@app.route('/keep_alive')
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data['keep_alive'] = keep_alive_count
    parsed_json = json.dumps(data)
    return str(parsed_json)

#################################### New Endpoints #########################################################

@app.route("/login", methods=['GET', 'POST'])
def login():
    email = "pgarfield@gmail.com"
    password = "password"
    content = request.json
    # must add in encryption and decryption in future
    if content['email'] == email and content['password'] == password:
        result = {
            "Result": "True",
                  "HouseID": "1234567"
                  }
        return result
    else:
        return "False"


# returns the house main room details
@app.route("/house_room/<house_id>", methods=['GET', 'POST'])
# returns the rooms that the house has
def home_rooms(house_id):
    rooms = [{
        "temperature": 10,
        "dateTime": "24:00:15T2021:12:02",
        "room": "Bedroom #1"
    },
        {
            "temperature": 20,
            "dateTime": "24:00:15T2021:12:02",
            "room": "Kitchen #2"
        }]
    if house_id == "1234567":
        return jsonify(rooms)
    else:
        return str(house_id)


@app.route("/oil_level_current/<house_id>", methods=['GET', 'POST'])
# returns the rooms that the house has
def current_levels(house_id):
    # get the most recent recording of the oil
    result = {
        "oil_level": 10,  # percent out a hundred in number
    }
    if house_id == "1234567":
        return jsonify(result)
    else:
        return str(house_id)

#################################### New Endpoints End #########################################################

if __name__ == '__main__':
    app.run()





