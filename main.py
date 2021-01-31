
from database import *
import random
from flashcard import *
from flashcard_set import *
from user import *

def main():
    #User makes account
    #We get request from server with data
    #make a new user (ex: user1)
    user1 = user(1)
    #we ge
    flashCardSet = flashcard_set(2)
    flashcard1 = flashcard("How many murders did America's most prolific serial killer Samuel Little commit?", "80", 123, 2, 1)
    flashcard2 = flashcard("How do cells determine what size to grow to before dividing?", "Through Nuclear Cytoplasmic Ratio, Genetic Machinery, Contact Inhibition, and Time", 124, 2, 1)
    flashCardSet.add_flashcard(flashcard1)
    flashCardSet.add_flashcard(flashcard2)
    user1.add_flashcard_set(flashCardSet)

    for flashcardSet in user1.flashcard_sets:
        currentSet = user1.flashcard_sets[flashcardSet]
        for item in currentSet.flashcards:
            flashCardSet.flashcards[item].print()
    user1.get_flashcards_to_do(2)
    flashcard1.calculate_next_review_day(5)
    flashcard2.calculate_next_review_day(0)
    flashcard1.send_to_database()
    user1.get_review_dates(2)
    print(db_get_user("60160d48c81590872de83670"))
    print(db_get_set("60161419061e965e6ca7c645"))


    # db_delete_user("60160b96606dc4f598738570")
    # db_create_set(1, "Cats", "Cats are sometimes it.", dict())


    

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