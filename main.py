
from database import *
import random
from flashcard import *
from flashcard_set import *
from user import *

def main():
    #User makes account
    #We get request from server with data
    # make a new user (ex: user1)
    # user1 = user(1)
    # #we ge
    # flashCardSet = flashcard_set(2)
    # flashcard1 = flashcard("How many murders did America's most prolific serial killer Samuel Little commit?", "80", 123, 2, 1)
    # flashcard2 = flashcard("How do cells determine what size to grow to before dividing?", "Through Nuclear Cytoplasmic Ratio, Genetic Machinery, Contact Inhibition, and Time", 124, 2, 1)
    # flashCardSet.add_flashcard(flashcard1)
    # flashCardSet.add_flashcard(flashcard2)
    # user1.add_flashcard_set(flashCardSet)

    # for flashcardSet in user1.flashcard_sets:
    #     currentSet = user1.flashcard_sets[flashcardSet]
    #     for item in currentSet.flashcards:
    #         flashCardSet.flashcards[item].print()
    # user1.get_flashcards_to_do(2)
    # flashcard1.calculate_next_review_day(5)
    # flashcard2.calculate_next_review_day(0)
    # flashcard1.send_to_database()
    # user1.get_review_dates(2)
    mimicUser = {
        "user_name": "Chris",
        "user_bio": "Cool guy",
        "flashcard_sets": [],
        "user_token": "3432489238u9234832"
    }
    newUser = {
        "user_name": "Chris",
        "user_bio": "My dawg",
        "flashcard_sets": [],
        "user_token": "3432489238u9234832"
    }
    newSet = {
        "set_name": "Bowen's Set",
        "set_desc": "A set about bowen's weird facts"
    }
    userid = db_create_user(mimicUser["user_name"], mimicUser["user_bio"], mimicUser["flashcard_sets"], mimicUser["user_token"])
    db_update_user_field(userid, "user_bio", newUser["user_bio"])
    db_update_user(userid, newUser)
    flashcardSet = db_create_set(userid, "set dfmsl", "A cool set.", [])
    flashcardSet2 = db_create_set(userid, "set dfmsl", "A cool set.", [])
    flashcardSet3 = db_create_set(userid, "set dfmsl", "A cool set.", [])
    print("SET_ID: ",flashcardSet)
    flashcard = db_create_flashcard(flashcardSet, "Question", "Answer")
    print("HIT:", db_get_user(userid))
    db_update_set_field(flashcardSet,"set_desc", "A super cool set.")
    db_update_set(flashcardSet, newSet)
    print("HIT2:", db_get_set(flashcardSet))
    print("HIT3:", db_get_flashcard(flashcard))
    db_delete_flashcard(flashcardSet, flashcard)
    # db_delete_set(userid, flashcardSet)
    # print("HIT3:", db_get_user(userid))
    # print("HIT4:", db_get_set(flashcardSet))
    # db_update_flashcard_field(flashcard, "front", "Why are you cool?")
    # db_update_flashcard_field(flashcard, "back", "Trick question.")
    # print("HIT5:", db_get_flashcard(flashcard))
    print("HERE HERE HERE:", db_get_set(flashcardSet))
    db_delete_user(userid)
    print("HIT3:", db_get_user(userid))
    print("HIT3:", db_get_flashcard(flashcard))


    

if __name__ == "__main__":
    main()


    



'''
>>> from supermemo2 import first_review
>>> smtwo = first_review(3)
>>> print(smtwo.review_date)
2021-01-02
>>> record = smtwo.as_dict(curr=True)
>>> record["quality"] = 5
>>> smtwo.calc(**record)
>>> print(smtwo.review_date)
2021-01-08
'''