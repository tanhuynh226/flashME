# from flashME.database import db_create_set, db_get_set
from flask import Flask, request, redirect, url_for, render_template, session, jsonify, abort
from flask.helpers import send_from_directory
from flask_dance.contrib.google import make_google_blueprint, google
from database import *
import requests
# from flask_login import logout_user
import json

app = Flask(__name__) #Change name

# == USER ==
# GET /api/user/get/<userid>
# Gets a user by their ID
@app.route('/api/user/get/<user_id>', methods=['GET'])
def get_user(user_id):
    user = db_get_user(user_id)
    print(user_id)
    if not user:
        print("HIT")
    else:
        return jsonify(user)

# GET /api/user/sets/<userid>
# Gets all sets that a user has, and their data
@app.route('/api/user/sets/<user_id>', methods=['GET'])
def user_sets(user_id):
    user = db_get_set(user_id) 
    if not user:
        abort(404)
    else:
        return jsonify([db_get_set(set_id) for set_id in user.sets])

# POST /api/user/create/<userid>
# Create a user with their ID

@app.route('/api/user/create/<user_id>', methods=['POST'])
def create_user(user_id):
    pass
    # find that user in the database
    # send that data back to the web browser (client)

# POST /api/user/update/<userid>
# Update a user with their ID
@app.route('/api/user/update/<user_id>', methods=['POST'])
def update_user():
    # get the user id from the URL
    # find that user in the database
    # send that data back to the web browser (client)
    pass

# POST /api/user/delete/<userid>
# Update a user with their ID
@app.route('/api/user/delete/<user_id>', methods=['POST'])
def delete_user(user_id):
    user = db_delete_user(user_id)
    if not user:
        abort(404)
    else:
        return user


# == SETS ==
# GET /api/sets/get/<setid>
# Gets a set by its ID
@app.route('/api/sets/get/<set_id>', methods=['GET'])
def get_set(set_id):
    set = db_get_set(set_id)
    if not set:
        abort(404)
    else:
        return jsonify(set)

'''
request.json (this is of type Dict)
{
    username: String,
    description: String,
    id: String (we don't have to use this)
    sets: [
        ...
    ]
    cards: [
        {
            front: String
            back: String
        },
        ...
    ]
}
'''

# POST /api/sets/create/<user_id>
# Create a set with that ID (it will have all the cards)
@app.route('/api/set/create/<user_id>', methods=['POST'])
def create_set(user_id):
    json = request.json
    token = request.headers['authorization']
    email = google_oauth2_validate(token)
    if not email:
        abort(401)
    db_create_set(user_id, json.name, json.description, json.cards)

# POST /api/sets/delete/<setid>
# Create a set with that ID (it will have all the cards)
@app.route('/api/set/delete/<user_id>/<set_id>', methods=['POST'])
def delete_set(user_id, set_id):
    json = request.json
    token = request.headers['authorization']
    email = google_oauth2_validate(token)
    if not email:
        abort(401)
    db_delete_set(set_id)


# POST /api/sets/update/<userid>
# Update a set with that ID
@app.route('/api/set/update/<user_id>/<set_id>', methods=['POST'])
def update_set(user_id, set_id):
    json = request.json
    token = request.headers['authorization']
    email = google_oauth2_validate(token)
    if not email:
        abort(401)
    db_update_set(user_id, json.name, json.description, json.cards)


# == FLASHCARDS ==
# GET /api/flashcard/get/<flashcardid>
@app.route('/api/flashcard/get/<flashcard_id>', methods=['GET'])
def get_flashcard(flashcard_id):
    flashcard = db_get_flashcard(flashcard_id)
    token = request.headers['authorization']
    email = google_oauth2_validate(token)
    if not email:
        abort(401)
    if not flashcard:
        abort(404)
    else:
        return jsonify(flashcard)

# Gets a flashcard by its ID from URL
#find in database
#send back to web browser


# POST /api/flashcard/create/<flashcardid>
@app.route('/api/flashcard/create/<set_id>', methods=['POST'])
def create_flashcard(set_id):
    json = request.json
    token = request.headers['authorization']
    email = google_oauth2_validate(token)
    if not email:
        abort(401)
    db_create_flashcard(set_id, json.front, json.back)
# Create a flashcard with an ID

# POST /api/flashcard/delete/<flashcardid>
@app.route('/api/flashcard/delete/<set_id>/<flashcard_id>', methods=['POST'])
def delete_flashcard(set_id, flashcard_id):
    json = request.json
    token = request.headers['authorization']
    email = google_oauth2_validate(token)
    if not email:
        abort(401)
    db_delete_flashcard(set_id, flashcard_id)
    pass

# Create a flashcard with an ID
# POST /api/flashcard/update/<flashcardid>
@app.route('/api/flashcard/update/<set_id>/<flashcard_id>', methods=['POST'])
def update_flashcard(set_id, flashcard_id):
    json = request.json
    token = request.headers['authorization']
    email = google_oauth2_validate(token)
    if not email:
        abort(401)
    db_update_flashcard(set_id, flashcard_id)
    pass
# Update a flashcard with an ID

# POST /api/flashcard/<studyid>
# Update a flashcard with the study results

# Calculations after user inputs correct or wrong
@app.route('/api/flashcard/delete/<flashcard_id>/<set_id>', methods=['POST'])
def study_flashcard(flashcard_id):
    pass

@app.route('/api/flashcard/delete/<set_id>', methods=['POST'])
def delete_all_flashcards(set_id):
    json = request.json
    token = request.headers['authorization']
    email = google_oauth2_validate(token)
    if not email:
        abort(401)
    db_delete_all_flashcards(set_id)
    pass

#serving static html files
#app = Flask(__name__, static_url_path='')

# @app.route('html/<path:path>')
# def send_html(path):
#     return send_from_directory('/html', path)\

#Google OAuth2
app.secret_key = "supersekrit"  # Replace this with your own secret!
google_blueprint = make_google_blueprint(
    client_id = "591191830884-iesl69sb9n8hukk9jldkhjjbdmgf2hpi.apps.googleusercontent.com",
    client_secret = "DwwVbC_7zBSHLB-_coC0bHbo",
    scope= [
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email",
    ]
)
app.register_blueprint(google_blueprint, url_prefix="/google_login")

@app.route("/google")
# def google_index():
#     if not google.authorized:
#         return redirect(url_for("google.login"))
#     resp = google.get("/oauth2/v2/userinfo")
#     if resp.ok:
#         resp_json = resp.json()
#         return 'You are {email} on Google'.format(email=resp_json["email"])
#     else:
#         return "Request failed!"

def google_oauth2_validate(access_token):
    r = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            params={'access_token': access_token})
    response = r.json()
    return response.email
    
    
    
# @app.route("/validate")
# def update_user(user_id):

    
# @app.route("/google/logout")
# def google_logout():
#     token = google_blueprint.token["access_token"]
#     resp = google.post(
#         "https://accounts.google.com/o/oauth2/revoke",
#         params={"token": token},
#         headers={"Content-Type": "application/x-www-form-urlencoded"}
#     )
#     assert resp.ok, resp.text
#     logout_user()        # Delete Flask-Login's session cookie
#     del google_blueprint.token  # Delete OAuth token from storage
#     return redirect(homepage) # redirect to after user has successfully logged in
    