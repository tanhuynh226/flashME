from user import user
from flask.helpers import flash
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

'''
    NOTE: many of the methods here revolve around the mongoDB created ObjectId, so with creation we may need to change this up
    (with creation of users for example)
'''

#User Methods

def db_get_user(user_id):
    myquery = { "_id": ObjectId(user_id) }
    foundUsers = users.find(myquery)
    user = None if foundUsers.explain()['executionStats']['nReturned'] <= 0 else foundUsers[0]
    return user

def db_create_user(user_name, user_bio, user_flashcards, user_token):
    new_user = {
        "user_name": user_name,
        "user_bio": user_bio,
        "flashcard_sets": user_flashcards,
        "user_token": user_token
    }
    userid = users.insert(new_user) #created from mongoDB, may need to be changed with OAuth
    return userid


'''
For users, sets, and cards, there's both a update_field and update_{object} (ex: update_user)
    - the update_field will update a singular field, when given the field (ex: user --> user_name) and new value 
        - very useful for inside methods, where I may update just one field after making a change 
        - (ex: deleting flashcard --> change flashcardSet "cards")
    - the update_{user, set, card} (ex: db_update_user) will update multiple fields, when given a dictionary of the values ex: { "username": "Chris" }
        - Much more useful for API which will send requests in JSON or in {} form
'''

def db_update_user_field(user_id, field, newValue):
    query = {"_id": ObjectId(user_id)}
    userUpdated = users.update(query, {"$set": {field: newValue}})
    pass

def db_update_user(user_id, newUser):
    query = {"_id": ObjectId(user_id)}
    userUpdated = users.update(query, {"$set": newUser})
    pass


def db_delete_user(user_id):
    myquery = { "_id": ObjectId(user_id) }
    deletedUser = users.find_one_and_delete(myquery)
    db_delete_all_sets(user_id)
    return deletedUser

#flashcard_set Methods
def db_get_set(set_id):
    myquery = { "_id": ObjectId(set_id) }
    foundSets = sets.find(myquery)
    set = None if foundSets.explain()['executionStats']['nReturned'] <= 0 else foundSets[0]
    return set

def db_get_sets_of_user(user_id):
    myquery = { "user_id": ObjectId(user_id) } 
    found_sets = sets.find(myquery)
    numReturned = found_sets.explain()['executionStats']['nReturned']
    sets_in_users = []
    for i in range(numReturned):
        sets_in_users.append(found_sets[i])
    return sets_in_users

def db_create_set(user_id, set_name, description, cards):
    new_set = {
        "user_id": user_id,
        "set_name": set_name,
        "set_desc": description,
        "cards": cards
    }
    set_id = sets.insert(new_set)
    user_sets = db_get_user(user_id)['flashcard_sets']
    user_sets.append((set_id))
    db_update_user_field(user_id, "flashcard_sets", user_sets)
    return set_id
    pass

def db_update_set_field(set_id, field, newValue):
    query = {"_id": ObjectId(set_id)}
    setUpdated = sets.update(query, {"$set": {field: newValue}})
    return setUpdated
    pass

def db_update_set(set_id, newSet):
    query = {"_id": ObjectId(set_id)}
    setUpdated = sets.update(query, {"$set": newSet})
    return setUpdated
    pass


def db_delete_set(user_id, set_id):
    # delete in sets collection
    query = {"_id": ObjectId(set_id)}
    sets.delete_one(query)
    # delete from user object
    user_sets = db_get_user(user_id)['flashcard_sets']
    user_sets.remove((set_id))
    db_update_user_field(user_id, "flashcard_sets", user_sets)
    #finally, delete all flashcards in set
    flashcards_in_set = db_get_flashcards_of_set(set_id)
    for flashcard in flashcards_in_set:
        db_delete_flashcard(set_id, flashcard["_id"])
    

def db_delete_all_sets(user_id):
    # deletes all sets belonging to that user_id
    query = {"_id": ObjectId(user_id)}
    print(users.remove(query))
    user_sets = db_get_sets_of_user(user_id)
     # deletes all flashcards underneath said sets (set_id)
    for set in user_sets:
        print(set['_id'])
        db_delete_all_flashcards(set['_id'])
        
    # clear user flashcard_sets
    db_update_user_field(user_id, "flashcard_sets", [])
    # sets.delete_many({})
    pass

#flashcard Methods

def db_get_flashcard(flashcard_id):
    myquery = { "_id": ObjectId(flashcard_id) }
    found_flashcards = flashcards.find(myquery)
    flashcard = None if found_flashcards.explain()['executionStats']['nReturned'] <= 0 else found_flashcards[0]
    return flashcard

def db_get_flashcards_of_set(set_id):
    myquery = { "set_id": ObjectId(set_id) } 
    found_flashcards = db.flashcards.find(myquery)
    numReturned = found_flashcards.explain()['executionStats']['nReturned']
    flashcards_in_set = []
    for i in range(numReturned):
        flashcards_in_set.append(found_flashcards[i])
    return flashcards_in_set

def db_create_flashcard(set_id, front, back):
    # create flashcard_id
    new_flashcard = {
        "set_id": set_id,
        "front": front,
        "back": back
    }
    flashcard_id = flashcards.insert(new_flashcard)
    set_cards = db_get_set(set_id)['cards']
    set_cards.append(flashcard_id)
    db_update_set_field(set_id, "cards", set_cards)
    return flashcard_id
    pass

def db_update_flashcard_field(flashcard_id, field, newValue):
    query = {"_id": ObjectId(flashcard_id)}
    updatedFlashcard = flashcards.update(query, {"$set": {field: newValue}})
    print(updatedFlashcard)
    return updatedFlashcard
    pass

def db_update_flashcard(flashcard_id, newFlashcard):
    query = {"_id": ObjectId(flashcard_id)}
    updatedFlashcard = flashcards.update(query, {"$set": newFlashcard})
    print(updatedFlashcard)
    return updatedFlashcard
    pass

def db_delete_flashcard(set_id, flashcard_id):
    # takes in set_id
    set = db_get_set(set_id)
    # deletes flashcard_id belonging to that set_id
    query = {"_id": ObjectId(flashcard_id)}
    flashcards.delete_one(query)
    # delete from set object
    print(set)
    set_cards = set['cards']
    set_cards.remove(flashcard_id)
    db_update_set_field(set_id, "cards", set_cards)
    pass

def db_delete_all_flashcards(set_id):
    # takes in set_id 
    set = db_get_set(set_id)
    print(set)
    # deletes all flashcards belonging to that set_id
    query = {"set_id": ObjectId(set_id)}
    flashcards.remove(query)

    db_update_set_field(set_id, "cards", [])

    pass



# print(collection.list_collection_names())



