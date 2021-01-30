from supermemo2 import *
from flashcard import *
import time

def updateReviewDate(flashcard):
    start = time.time();
    #if correct button is pressed:
        end = time.time();
        if (end - time) > 10:
            flashcard.review_date = flashcard.modify(card_id, 3)
        elif (end - time) > 5:
            flashcard.review_date = flashcard.quality(4)
        elif (end - time) < 5:
            flashcard.review_date = flashcard.quality(5)
    #else if wrong button is pressed:
        end = time.time();
        if (end - time) > 5:
            flashcard.review_date = flashcard.quality(1)
        elif (end - time) < 5:
            flashcard.review_date = flashcard.quality(2)
    #else if didn't know button is pressed:
        flashcard.review_date = flashcard.quality(0)

