import pymongo
from bson.objectid import ObjectId
from pprint import pprint
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
db_uri = "mongodb+srv://chris:zumaJK8kuFPJlN7S@cluster0.yp3zl.mongodb.net/flashDB?retryWrites=true&w=majority"
client = pymongo.MongoClient(db_uri)
db = client.flashDB
users = db.users 
sets = db.sets
flashcards = db.flashcards

#user Methods
exampleUser = {
    "user_name": "Chris",
    "set_ids" : "",
    #"user_id" : ObjectId("23432423423"),
    "user_bio": "",
    "flashcard_sets": [],
}
def db_get_user(user_id):
    myquery = { "_id": ObjectId(user_id) }
    foundUsers = users.find(myquery)
    user = None if foundUsers.explain()['executionStats']['nReturned'] <= 0 else foundUsers[0]
    return user
    
def db_create_user(user_name, user_bio, user_info, user_token):
    new_user = {
        "user_name": user_name,
        "user_bio": user_bio,
        "user_info": user_info,
        "user_token": user_token
    }
    users.insert_one(new_user)
    pass

def db_update_user(new_user):
    userUpdated = users.update({"_id": ObjectId(user_id), user: new_user})
    userUpdated.explain()
    
    pass

def db_delete_user(user_id):
    myquery = { "_id": ObjectId(user_id) }
    users.delete_one(myquery)
    print(users.find().explain())
    #sets.delete_many({}) deleting users should delete all their sets
    pass

#flashcard_set Methods
def db_get_set(set_id):
    myquery = { "_id": ObjectId(set_id) }
    foundSets = sets.find(myquery)
    set = None if foundSets.explain()['executionStats']['nReturned'] <= 0 else foundSets[0]
    return set

def db_create_set(user_id, set_name, description, cards):
    new_set = {
        "user_id": user_id,
        "set_name": set_name,
        "set_desc": description,
        "cards": cards
    }
    set_id = sets.insert(new_set)
    print(set_id)
    pass

def db_update_set(user_id, set_id):
    '''setUpdated = sets.update({"": })
    setUpdated.explain()'''
    pass

def db_delete_set(user_id, set_id):
    # delete in sets collection
    query = {_id: ObjectId(set_id)}
    sets.delete_one(query)
    print(sets.find().explain())
    # delete from user object
    users.find_one
    
    pass

def db_delete_all_sets(user_id):
    # takes in user_id
    user = db_get_user(user_id)
    # deletes all sets belonging to that user_id
    
    # deletes all flashcards underneath said sets (set_id)
    for set_id in user_id:
        db_delete_all_flashcards(set_id)
    # clear user flashcard_sets
    db_update_user
    # sets.delete_many({})
    pass

#flashcard Methods

def db_get_flashcard(flashcard_id):
    myquery = { "_id": ObjectId(flashcard_id) }
    found_flashcards = sets.find(myquery)
    flashcard = None if found_flashcards.explain()['executionStats']['nReturned'] <= 0 else found_flashcards[0]
    return flashcard

def db_create_flashcard(set_id, front, back):
    # create flashcard_id
    new_flashcard = {
        "set_id": set_id,
        "front": front,
        "back": back
    }
    flashcard_id = sets.insert(new_flashcard)
    pass

def db_update_flashcard(set_id, flashcard_id):
    '''flashcardUpdated = flashcards.update({"": })
    flashcardUpdated.explain()'''
    pass

def db_delete_flashcard(set_id, flashcard_id):
    # takes in set_id
    set = db_get_set(set_id)
    # deletes flashcard_id belonging to that set_id
    myquery = {_id: ObjectId(flashcard_id)}
    flashcards.delete_one(myquery)
    # delete from set object
    pass

def db_delete_all_flashcards(set_id):
    # takes in set_id 
    set = db_get_set(set_id)
    # deletes all flashcards belonging to that set_id
    for flashcard_id in set_id:
        db_delete_flashcard(flashcard_id)
    pass



# print(collection.list_collection_names())

# user_id = users.insert_one(exampleUser).inserted_id
# print(user_id)

