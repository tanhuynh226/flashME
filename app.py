# from flashME.database import db_create_set, db_get_set
from flask import Flask, request, redirect, url_for, render_template, session, jsonify, abort
from flask.helpers import send_from_directory
from flask_dance.contrib.google import make_google_blueprint, google
from database import *
import requests
import secret
# from flask_login import logout_user
import json

app = Flask(__name__) #Change name

# == USER ==
# GET /api/user/get/<userid>
# Gets a user by their ID
@app.route('/api/user/get/me', methods=['GET'])
def get_user():
    email = google_oauth2_validate(request.headers['authorization'])
    if not email:
        abort(401, description="Token could not be linked to any email.")
    user = db_get_user(email)
    print(user)
    if "error" in user:
        abort(404, description=user["error"])
    else:
        return json.dumps(user)

# GET /api/user/sets/<userid>
# Gets all sets that a user has, and their data
@app.route('/api/user/sets/me', methods=['GET'])
def get_all_sets():
    email = google_oauth2_validate(request.headers['authorization'])
    if not email:
        abort(401, description="Token could not be linked to any email.")
    sets = db_get_sets_of_user(email)
    return json.dumps(sets)

# POST /api/user/create/<userid>
# Create a user with their ID

@app.route('/api/user/create/me', methods=['POST'])
def create_user():
    email = google_oauth2_validate(request.headers['authorization'])
    if not email:
        abort(401, description="Token could not be linked to any email.")
    else:

    # find that user in the database
    # send that data back to the web browser (client)


# POST /api/user/update/<userid>
# Update a user with their ID
@app.route('/api/user/update/me', methods=['POST'])
def update_user(user_id):
    email = google_oauth2_validate(request.headers['authorization'])
    if not email:
        abort(401, description="Token could not be linked to any email.")
    json = request.json
    # get the user id from the URL
    print(request.json)
    user = db_update_user(user_id, json)
    if "error" in user:
        abort(404, description=user["error"])
    else:
        return user
    # find that user in the database
    # send that data back to the web browser (client)

# POST /api/user/delete/<userid>
# Update a user with their ID
@app.route('/api/user/delete/me', methods=['POST'])
def delete_user(user_id):
    email = google_oauth2_validate(request.headers['authorization'])
    if not email:
        abort(401, description="Token could not be linked to any email.")
    user = db_delete_user(user_id)
    if "error" in user:
        abort(404, description=user["error"])
    else:
        return user


# == SETS ==
# GET /api/sets/get/<setid>
# Gets a set by its ID
@app.route('/api/sets/get/<set_id>', methods=['GET'])
def get_set(set_id):
    email = google_oauth2_validate(request.headers['authorization'])
    if not email:
        abort(401, description="Token could not be linked to any email.")
    set = db_get_set(set_id)
    print(set)
    if "error" in set:
        abort(404, description=set["error"])
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

# POST /api/sets/create/me
# Create a set with that ID (it will have all the cards)
@app.route('/api/set/create/me', methods=['POST'])
def create_set():
    email = google_oauth2_validate(request.headers['authorization'])
    if not email:
        abort(401, description="Token could not be linked to any email.")
    json = request.json
    db_create_set(email, json.name, json.description, json.cards)

# POST /api/sets/delete/<setid>
# Create a set with that ID (it will have all the cards)
'''
No other info is needed, besides the user_id and set_id!
Also, changing delete route to method: 'DELETE'
'''
@app.route('/api/set/delete/me/<set_id>', methods=['DELETE'])
def delete_set(user_id, set_id):
    email = google_oauth2_validate(request.headers['authorization'])
    if not email:
        abort(401, description="Token could not be linked to any email.")
    json = request.json
    set = db_delete_set(user_id, set_id)
    if "error" in set:
        abort(404, description=set["error"])
    db_delete_set(set_id)


# POST /api/sets/update/<userid>
# Update a set with that ID
@app.route('/api/set/update/me/<set_id>', methods=['POST'])
def update_set(user_id, set_id):
    email = google_oauth2_validate(request.headers['authorization'])
    if not email:
        abort(401, description="Token could not be linked to any email.")
    json = request.json
    set = db_update_set(set_id, json)
    if "error" in set:
        abort(404, description=set["error"])
    db_update_set(user_id, json.name, json.description, json.cards)


# == FLASHCARDS ==
# GET /api/flashcard/get/<flashcardid>
@app.route('/api/flashcard/get/<flashcard_id>', methods=['GET'])
def get_flashcard(flashcard_id):
    email = google_oauth2_validate(request.headers['authorization'])
    if not email:
        abort(401, description="Token could not be linked to any email.")
    print(flashcard_id)
    flashcard = db_get_flashcard(flashcard_id)
    if "error" in flashcard:
        abort(404, description=flashcard["error"])
    else:
        return jsonify(flashcard)

# Gets a flashcard by its ID from URL
#find in database
#send back to web browser


# POST /api/flashcard/create/<flashcardid>
@app.route('/api/flashcard/create/<set_id>', methods=['POST'])
def create_flashcard(set_id):
    email = google_oauth2_validate(request.headers['authorization'])
    if not email:
        abort(401, description="Token could not be linked to any email.")
    json = request.json
    db_create_flashcard(set_id, json.front, json.back)
# Create a flashcard with an ID

# POST /api/flashcard/delete/<flashcardid>
@app.route('/api/flashcard/delete/<set_id>/<flashcard_id>', methods=['DELETE'])
def delete_flashcard(set_id, flashcard_id):
    email = google_oauth2_validate(request.headers['authorization'])
    if not email:
        abort(401, description="Token could not be linked to any email.")
    json = request.json
    flashcard = db_get_flashcard(flashcard_id)
    if "error" in flashcard:
        abort(404, description=flashcard["error"])
    db_delete_flashcard(set_id, flashcard_id)
    pass

# Update flashcard (review dates, quality, flashcard_id)
# POST /api/flashcard/update/<flashcardid>
@app.route('/api/flashcard/update/<set_id>/<flashcard_id>', methods=['POST'])
def update_flashcard(set_id, flashcard_id):
    email = google_oauth2_validate(request.headers['authorization'])
    if not email:
        abort(401, description="Token could not be linked to any email.")
    json = request.json
    flashcard = db_get_flashcard(flashcard_id)
    if "error" in flashcard:
        abort(404, description=flashcard["error"])
    db_update_flashcard(set_id, flashcard_id)
    pass

# POST /api/flashcard/<studyid>
# Update a flashcard with the study results
'''
    Needed info:
    - Time --> seconds to complete problem
    - Correct --> whether it's correct
    - ID --> flashcard ID

    Will return: (String Json, need to parse) 
    - quality --> quality calculated based on time and correctness
    - easiness --> easiness of retrieving answer?
    - repetitions --> number of times repeated
    - review_date --> next review date
    - interval --> how many days til next review date
    
    NOTE: all values with prefix prev_ are the previous value before calcualti
    {"quality": 4, "prev_easiness": 2.36, 
    "prev_interval": 14, "prev_repetitions": 4, 
    "prev_review_date": "2021-01-31", 
    "easiness": 2.36, "interval": 33, 
    "repetitions": 5, "review_date": "2021-03-05"}
'''
# Calculations after user inputs correct or wrong
@app.route('/api/flashcard/study/<set_id>/<flashcard_id>', methods=['POST'])
def study_flashcard(flashcard_id, time, correct):
    email = google_oauth2_validate(request.headers['authorization'])
    if not email:
        abort(401, description="Token could not be linked to any email.")
    db_study_flashcard(flashcard_id, time, correct)
    # Perform calculations to calculate the next review day for this specific flashcard_id
    pass

# All the flashcards that need to be studied today
@app.route('/api/flashcard/today/<set_id>', methods=['POST'])
def today_flashcard(flashcard_id):
    email = google_oauth2_validate(request.headers['authorization'])
    if not email:
        abort(401, description="Token could not be linked to any email.")
    # return array of cards that need to be studied today
    pass

# Delete all flashcards within a set
@app.route('/api/flashcard/delete/<set_id>', methods=['DELETE'])
def delete_all_flashcards(set_id):
    email = google_oauth2_validate(request.headers['authorization'])
    if not email:
        abort(401, description="Token could not be linked to any email.")
    json = request.json
    set = db_delete_all_flashcards(set_id)
    if "error" in set:
        abort(404, description=set["error"])
    db_delete_all_flashcards(set_id)
    pass

#serving static html files
#app = Flask(__name__, static_url_path='')

# @app.route('html/<path:path>')
# def send_html(path):
#     return send_from_directory('/html', path)\

#Google OAuth2
# app.secret_key = secret.google_client_secret  
# google_blueprint = make_google_blueprint(
#     client_id = secret.google_client_id,
#     client_secret = secret.google_client_secret,
#     scope= [
#         "https://www.googleapis.com/auth/plus.me",
#         "https://www.googleapis.com/auth/userinfo.email",
#     ]
# )
# app.register_blueprint(google_blueprint, url_prefix="/google_login")

# @app.route("/google")
# def google_index():
#     if not google.authorized:
#         return redirect(url_for("google.login"))
#     resp = google.get("/oauth2/v2/userinfo")
#     if resp.ok:
#         return '<h1>You are {email} on Google'.format(email=resp_.json()["email"])
#     else:
#         return "Request failed!"

def google_oauth2_validate(access_token):
    r = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            params={'access_token': access_token})
    response = r.json()
    return response['email']
    
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