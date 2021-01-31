from flask import Flask, request, redirect, url_for, render_template, session
import json
import sqlite3
import os
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

app = Flask("server") #Change name

@app.route('/')
def homeRoute():
    pass

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

def afterRequest():
    # Update data with new retrieved / sent data?
    pass

app.after_request(afterRequest) 

'''
CREATE A POST ROUTE
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        etc
    elif request.authorization !== 'authorization':
        abort(401)
        this_is_never_executed()

RETURN JSON
@app.route("/me")
def me_api():
    user = get_current_user()
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }

GET USERNAME
@app.route('/user/<username>')
def profile(username):
    user = mongodb.fetch_user('')
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }


'''
#oauth2 kinda code idk

GOOGLE_CLIENT_ID = os.environ.get("")
GOOGLE_CLIENT_SECRET = os.environ.get("")
#GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

#flask setup but idk if we need this or more as idk if this is right
app = Flask(__name__)
app.secret_key = os.environment.get("SECRET_KEY") or os.urandom()#size

#user session manage/setup
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    return "Message", #size

client = WebApplicationClient(GOOGLE_CLIENT_ID)

@app.route("/", methods=["GET","POST"])
def index():
    if current_user.is_authenticated: #is .is_authenticated django?
        return redirect('homepage')
    else:
        return render_template('index.html')

@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
     request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
     )
     return redirect(request_uri)

@app.route("/login/callback")
def callback():
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )

     token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    #parse tokens
    client.parse_request_body_response(json.dumps(token_response.json())) # from oauth 2 lib

    #where google gives user profile info
    #google profile pic and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    #verifies legitimacy of the email with google
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", #smth size goes here

    #This is where we create a user in the database with the info provided from google
     user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    #if the user doesn't exist then we add them to the database
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    #just login
    login_user(user)

    #sends them to HP
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


#Code for username and password



