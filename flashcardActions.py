from supermemo2 import *
from flashcard import *
import time

def updateReviewDate(flashcard):
    start = time.time();
    #if correct button is pressed:
        end = time.time();
        if (end - time) > 10:
            flashcard.review_date = flashcard.calculate_next_review_day(3)
        elif (end - time) > 5:
            flashcard.review_date = flashcard.calculate_next_review_day(4)
        elif (end - time) < 5:
            flashcard.review_date = flashcard.calculate_next_review_day(5)
    #else if wrong button is pressed:
        end = time.time();
        if (end - time) > 5:
            flashcard.review_date = flashcard.calculate_next_review_day(1)
        elif (end - time) < 5:
            flashcard.review_date = flashcard.calculate_next_review_day(2)
    #else if didn't know button is pressed:
        flashcard.review_date = flashcard.calculate_next_review_day(0)

