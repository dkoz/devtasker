from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import requests
import os
import settings as settings

app = Flask(__name__, static_folder='assets')
# Added optional secret key to fix cookies issue
app.secret_key = settings.secret_flask_key

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

DISCORD_CLIENT_ID = settings.client_id
DISCORD_CLIENT_SECRET = settings.client_secret
DISCORD_REDIRECT_URI = settings.redirect_url
DISCORD_API_BASE_URL = "https://discord.com/api"
DISCORD_OAUTH_AUTHORIZE_URL = f"{DISCORD_API_BASE_URL}/oauth2/authorize"
DISCORD_OAUTH_TOKEN_URL = f"{DISCORD_API_BASE_URL}/oauth2/token"
DISCORD_USER_API_URL = f"{DISCORD_API_BASE_URL}/users/@me"
YOUR_DISCORD_USER_ID = settings.discord_id

class Tasker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

with app.app_context():
    db.create_all()

def is_logged_in():
    """Helper function to check if user is logged in and authorized."""
    return 'discord_user' in session and session['discord_user']['id'] == YOUR_DISCORD_USER_ID

@app.route("/")
def home():
    dev_list = db.session.query(Tasker).all()
    return render_template("base.html", dev_list=dev_list)

@app.route("/login")
def login():
    discord_login_url = f"{DISCORD_OAUTH_AUTHORIZE_URL}?client_id={DISCORD_CLIENT_ID}&redirect_uri={DISCORD_REDIRECT_URI}&response_type=code&scope=identify"
    return redirect(discord_login_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI,
        "scope": "identify"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(DISCORD_OAUTH_TOKEN_URL, data=data, headers=headers)
    response_json = response.json()
    access_token = response_json.get("access_token")
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    user_response = requests.get(DISCORD_USER_API_URL, headers=headers)
    discord_user = user_response.json()

    # Does a check for your discord id
    if discord_user["id"] == YOUR_DISCORD_USER_ID:
        session['discord_user'] = discord_user
        return redirect(url_for("home"))
    else:
        return "Unauthorized", 403

@app.route("/logout")
def logout():
    session.pop('discord_user', None)
    return redirect(url_for("home"))

@app.post("/add")
def add():
    if not is_logged_in():
        return redirect(url_for("login"))

    title = request.form.get("title")
    new_tasker = Tasker(title=title, complete=False)
    db.session.add(new_tasker)
    db.session.commit()
    return redirect(url_for("home"))

@app.get("/update/<int:tasker_id>")
def update(tasker_id):
    if not is_logged_in():
        return redirect(url_for("login"))

    tasker = db.session.query(Tasker).filter(Tasker.id == tasker_id).first()
    tasker.complete = not tasker.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.get("/delete/<int:tasker_id>")
def delete(tasker_id):
    if not is_logged_in():
        return redirect(url_for("login"))

    tasker = db.session.query(Tasker).filter(Tasker.id == tasker_id).first()
    db.session.delete(tasker)
    db.session.commit()
    return redirect(url_for("home"))

@app.get("/edit/<int:tasker_id>")
def edit(tasker_id):
    if not is_logged_in():
        return redirect(url_for("login"))

    tasker = db.session.query(Tasker).filter(Tasker.id == tasker_id).first()
    return render_template("edit.html", tasker=tasker)

@app.post("/edit/<int:tasker_id>")
def edit_post(tasker_id):
    if not is_logged_in():
        return redirect(url_for("login"))

    tasker = db.session.query(Tasker).filter(Tasker.id == tasker_id).first()
    new_title = request.form.get("title")
    tasker.title = new_title
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
