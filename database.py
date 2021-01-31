from user import user
from flask.helpers import flash
import pymongo
from bson.objectid import ObjectId
from pprint import pprint
from supermemo2 import *
from flashcard import *
import secret
import os

# User
# username: String,
# flashcards: Dictionary
# token: String

# Flashcard
# Front: String, Image
# Back: String, Image
# card_id: string,
# set_id: string,
# user_id?: string ?
# learning_info : { ( comes from superMemo2.json() ) }
    # e.g. 
#  

# MongoDB Setup
db_uri = secret.db_uri
client = pymongo.MongoClient(db_uri)
db = client.flashDB
users = db.users 
sets = db.sets
flashcards = db.flashcards

'''
    NOTE: many of the methods here revolve around the mongoDB created ObjectId, so with creation we may need to change this up
    (with creation of users for example)
'''

#User Methods

def db_get_user(user_id):
    myquery = { "_id": user_id }
    foundUsers = users.find(myquery)
    user = None if foundUsers.explain()['executionStats']['nReturned'] <= 0 else foundUsers[0]
    user_data = {}
    if not user == None:
        user_data = user
        user_data['flashcard_sets'] = db_get_sets_of_user(user_id)
    else:
        user_data = {
            "error": "No user found."
        }
    return user_data

def db_create_user(user_name, user_bio, user_flashcards, user_email):
    query = {"_id": user_email, "user_name": user_name}
    duplicateUsers = users.find(query)
    new_user_data = {"error": "User already has this username or email."} if duplicateUsers.explain()['executionStats']['nReturned'] > 0 else {}
    if not "error" in new_user_data:
        new_user = {
            "user_name": user_name,
            "user_bio": user_bio,
            "flashcard_sets": user_flashcards,
            "_id": user_email
        }
        #created from mongoDB, may need to be changed with OAuth
        userid = users.insert(new_user)
        return user_email
    else:
        return new_user_data


'''
For users, sets, and cards, there's both a update_field and update_{object} (ex: update_user)
    - the update_field will update a singular field, when given the field (ex: user --> user_name) and new value 
        - very useful for inside methods, where I may update just one field after making a change 
        - (ex: deleting flashcard --> change flashcardSet "cards")
    - the update_{user, set, card} (ex: db_update_user) will update multiple fields, when given a dictionary of the values ex: { "username": "Chris" }
        - Much more useful for API which will send requests in JSON or in {} form
'''

def db_update_user_field(user_id, field, newValue):
    if not "error" in user_id:
        query = {"_id": user_id}
        userUpdated = users.update(query, {"$set": {field: newValue}})
        data = {"error": f"User {user_id} wasn't updated"} if userUpdated['nModified'] <= 0 else {"success": f"User {user_id} was updated"}
        return data
    else:
        return {"error": "User "+ user_id + " could not be updated."}

def db_update_user(user_id, newUser):
    query = {"_id": user_id}
    userUpdated = users.update(query, {"$set": newUser})
    if(userUpdated['nModified'] > 0): 
        return {"success": "User " + user_id + " has been updated"}
    else:
        return {"error": "User "+ user_id + " could not be updated."}


def db_delete_user(user_id):
    myquery = { "_id": user_id }
    deletedUser = users.find_one_and_delete(myquery)
    data = {"error": f"User {user_id} could not be deleted."} if deletedUser == None else {"success": f"User {str(deletedUser['_id'])} was deleted."}
    if not "error" in data: 
        db_delete_all_sets(user_id)
    return data

#flashcard_set Methods
def db_get_set(set_id):
        myquery = { "_id": ObjectId(set_id) }
        foundSets = sets.find(myquery)
        set = None if foundSets.explain()['executionStats']['nReturned'] <= 0 else foundSets[0]
        if not set == None:
            cards = db_get_flashcards_of_set(set_id)
            set_data = {
                "title": set["set_name"],
                "description": set["set_desc"],
                "cards": cards,
                "id": str(set["_id"]), #Object id -> str
            }
        else:
            set_data = {
                "error": "No set found."
            }
        return set_data

    

def db_get_sets_of_user(user_id):
    myquery = { "user_email": user_id } 
    found_sets = sets.find(myquery)
    numReturned = found_sets.explain()['executionStats']['nReturned']
    sets_in_users = []
    for i in range(numReturned):
        sets_in_users.append(found_sets[i])
    for user_set in sets_in_users:
        user_set["_id"] = str(user_set["_id"])
        # user_set["user_id"] = str(user_set["user_id"])
    pprint(sets_in_users)
    return sets_in_users

def db_create_set(user_email, set_name, description, cards):
    new_set = {
        "user_email": user_email,
        "set_name": set_name,
        "set_desc": description,
        "cards": cards
    }
    user = db_get_user(user_email)
    newuser = user
    set_id = sets.insert(new_set)
    newuser_sets = user["flashcard_sets"]
    newuser_sets.append(set_id)
    newuser["flashcard_sets"] = newuser_sets
    db_update_user(user_email, newuser)
    return set_id 

def db_update_set_field(set_id, field, newValue):
    query = {"_id": ObjectId(set_id)}
    setUpdated = sets.update(query, {"$set": {field: newValue}})
    data = {"error": f"Set {set_id} wasn't updated"} if setUpdated['nModified'] <= 0 else {"success": f"Set {set_id} was updated"}
    return data

def db_update_set(set_id, newSet):
    query = {"_id": ObjectId(set_id)}
    setUpdated = sets.update(query, {"$set": newSet})
    data = {"error": f"Set {set_id} wasn't updated"} if setUpdated['nModified'] <= 0 else {"success": f"Set {set_id} was updated"}
    return data


def db_delete_set(user_id, set_id):
    # delete in sets collection
    user_sets = db_get_user(user_id)
    if "error" in user_sets:
        return {"error": f"No set was deleted."}
    matching_sets = [set for set in user_sets['flashcard_sets'] if str(set["_id"]) == str(set_id)]
    if len(matching_sets) > 0:
        query = {"_id": ObjectId(set_id)}
        set = sets.remove(query)
        if set['n'] > 0:
            flashcards_in_set = db_get_flashcards_of_set(set_id)
            for flashcard in flashcards_in_set:
                db_delete_flashcard(set_id, flashcard["_id"])
            if(len(user_sets) > 0):
                keep_sets = [set for set in user_sets['flashcard_sets'] if str(set['_id']) != str(set_id)]
                db_update_user_field(user_id, "flashcard_sets", keep_sets)
            return {"success": f"Set {set_id} was deleted from user {user_id}"}
        else:
            return {"error": f"No set was deleted."}
    else:
        return {"error": f"Invalid request: User {user_id} does not own set {set_id}"}
    # delete from user object
    
        #finally, delete all flashcards in set
            

def db_delete_all_sets(user_id):
    # deletes all sets belonging to that user_id
    user_sets = db_get_sets_of_user(user_id)
    query = {"_id": user_id}
     # deletes all flashcards underneath said sets (set_id)
    for set in user_sets:
        db_delete_all_flashcards(set['_id']) # but don't return {"success": f"Set {set_id} was deleted from user {user_id}"} for every set deleted
    # clear user flashcard_sets
    db_update_user_field(user_id, "flashcard_sets", [])
    # one option is sets.delete_many({})
    pass

#flashcard Methods

def db_get_flashcard(flashcard_id):
    myquery = { "_id": ObjectId(flashcard_id) }
    found_flashcards = flashcards.find(myquery)
    flashcard = None if found_flashcards.explain()['executionStats']['nReturned'] <= 0 else found_flashcards[0]
    if not flashcard == None:
        flashcard_data = flashcard 
        del flashcard_data['set_id'] 
        del flashcard_data['_id']
    return flashcard_data

def db_get_flashcards_of_set(set_id):
    myquery = { "set_id": ObjectId(set_id) } 
    found_flashcards = db.flashcards.find(myquery)
    numReturned = found_flashcards.explain()['executionStats']['nReturned']
    flashcards_in_set = []
    for i in range(numReturned):
        flashcards_in_set.append(found_flashcards[i])
    for flashcard in flashcards_in_set:
        flashcard['_id'] = str(flashcard['_id'])
        flashcard['set_id'] = str(flashcard['set_id'])
    return flashcards_in_set

def db_create_flashcard(set_id, front, back):
    # create flashcard_id
    superMem = first_review(3)
    new_flashcard = {
        "set_id": set_id,
        "front": front,
        "back": back,
        "learning_history": superMem.json()
    }
    flashcard_id = flashcards.insert(new_flashcard)
    set_cards = db_get_set(set_id)['cards']
    set_cards.append(flashcard_id)
    db_update_set_field(set_id, "cards", set_cards)
    return flashcard_id

def db_update_flashcard_field(flashcard_id, field, newValue):
    query = {"_id": ObjectId(flashcard_id)}
    updatedFlashcard = flashcards.update(query, {"$set": {field: newValue}})
    return updatedFlashcard
    pass

def db_update_flashcard(flashcard_id, newFlashcard):
    query = {"_id": ObjectId(flashcard_id)}
    updatedFlashcard = flashcards.update(query, {"$set": newFlashcard})
    return updatedFlashcard
    pass

def db_delete_flashcard(set_id, flashcard_id):
    # takes in set_id
    set = db_get_set(set_id)
    print("SET IS:", set)
    # deletes flashcard_id belonging to that set_id
    query = {"_id": ObjectId(flashcard_id)}
    flashcards.delete_one(query)
    # delete from set object
    
    if not "error" in set:
        set_cards = set['cards']
        set_cards.remove(flashcard_id)
        db_update_set_field(set_id, "cards", set_cards)
    pass

def db_delete_all_flashcards(set_id):
    # takes in set_id 
    set = db_get_set(set_id)
    # deletes all flashcards belonging to that set_id
    query = {"set_id": ObjectId(set_id)}
    flashcards.remove(query)
    db_update_set_field(set_id, "cards", [])
    pass

def db_study_flashcard(flashcard_id, time, correct):
    # get current learning history (if any)
    flashcard_from_db = db_get_flashcard(flashcard_id)
    learning_history = flashcard_from_db["learning_history"]
    new_flashcard = flashcard(learning_history)
    new_flashcard.updateReviewDate(time, correct)
    db_update_flashcard_field(flashcard_id, "learning_history", new_flashcard.learning_history)
    return new_flashcard.learning_history

def db_get_cards_to_study_today(set_id):
    set_from_db = db_get_set(set_id)
    cards = set_from_db["cards"]
    cards_to_do = []
    for card in cards:
        curr_card = json.loads(card["learning_history"])
        print(curr_card["review_date"])
        correct_date = date.fromisoformat(curr_card["review_date"])
        if(correct_date <= date.today()):
            cards_to_do.append(card)
    # cards_to_do = [card for card in cards if card["learning-history"]["review_date"] >= datetime.datetime(2020, 5, 17)]
    return cards_to_do



    # take data -> create Flashcard (using flashcard class)
    # get next_review_day from flashcard.get_next_review_day()
    # update db, send to front-end with json



# print(collection.list_collection_names())

