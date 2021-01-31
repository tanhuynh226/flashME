# from flashME.database import db_create_set, db_get_set
from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from flask.helpers import send_from_directory
from database import *
import json

app = Flask("server") #Change name

# == USER ==
# GET /api/user/get/<userid>
# Gets a user by their ID
@app.route('/api/user/get/<user_id>', methods=['GET'])
def get_user(user_id):
    user = db_get_user(user_id)
    if not user:
        abort(404)
    else:
        return jsonify(user)

# GET /api/user/sets/<userid>
# Gets all sets that a user has, and their data
@app.route('/api/user/sets/<user_id>', methods=['GET'])
def get_user(user_id):
    user = db_get_user(user_id)
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
def delete_user():
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

# GET /api/sets/delete/<setid>
# Gets a set by its ID
@app.route('/api/sets/delete/<set_id>', methods=['POST'])
def get_set(set_id):
    set = db_get_set(set_id)
    if not set:
        abort(404)
    else:
        return jsonify(set)

'''
request.json (this is of type Dict)
{
    name: String,
    description: String,
    id: String (we don't have to use this)
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
@app.route('/api/sets/create/<user_id>', methods=['POST'])
def create_set(user_id):
    json = request.json
    db_create_set(user_id, json.name, json.description, json.cards)

# POST /api/sets/delete/<setid>
# Create a set with that ID (it will have all the cards)
@app.route('/api/sets/delete/<user_id>/<set_id>', methods=['POST'])
def delete_set(user_id, set_id):
    json = request.json
    db_delete_set(set_id)


# POST /api/sets/update/<userid>
# Update a set with that ID
@app.route('/api/sets/update/<user_id>/<set_id>', methods=['POST'])
def update_set(user_id, set_id):
    json = request.json
    db_update_set(user_id, json.name, json.description, json.cards)

@app.route('/api/sets/delete/<user_id>', methods=['POST'])
def delete_all_sets(user_id):
    pass

# == FLASHCARDS ==
# GET /api/flashcard/get/<flashcardid>
@app.route('/api/flashcard/get/<flashcard_id>', methods=['GET'])
def get_flashcard(flashcard_id):
    flashcard = db_get_flashcard(flashcard_id)
    if not flashcard:
        abort(404)
    else:
        return jsonify(flashcard)

# Gets a flashcard by its ID from URL
#find in database
#send back to web browser

# GET /api/flashcard/delete/<flashcardid>
@app.route('/api/flashcard/delete/<set_id>/<flashcard_id>', methods=['GET'])
def get_flashcard(user_id, flashcard_id):
    flashcard = db_get_flashcard(user_id, flashcard_id)
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
    db_create_flashcard(set_id, json.front, json.back)
# Create a flashcard with an ID

# POST /api/flashcard/delete/<flashcardid>
@app.route('/api/flashcard/delete/<set_id>/<flashcard_id>', methods=['POST'])
def delete_flashcard(set_id, flashcard_id):
    pass

# Create a flashcard with an ID
# POST /api/flashcard/update/<flashcardid>
@app.route('/api/flashcard/update/<set_id>/<flashcard_id>', methods=['POST'])
def update_flashcard(flashcard_id):
    pass
# Update a flashcard with an ID

# POST /api/flashcard/<studyid>
# Update a flashcard with the study results
@app.route('/api/flashcard/delete/<flashcard_id>/<set_id>', methods=['POST'])
def study_flashcard(flashcard_id):
    pass

@app.route('/a[i/flashcard/delete/<set_id>', methods=['POST'])
def delete_all_flashcards(set_id):
    pass

#serving static html files
app = Flask(__name__, static_url_path='')

@app.route('html/<path:path>')
def send_html(path):
    return send_from_directory('html', path)

if __name__ == "__main__":
    app.run()