from supermemo2 import *
from datetime import *
from pprint import pprint
import json

#change to flash_id, set_id, user_id
class flashcard(object):
    def __init__(self, learning_history): 
        self.learning_history = learning_history
        self.next_review = None
        self.update_learning_history()
        

    def update_learning_history(self):
        smTwo = first_review(3, date.today())
        current_learning_history = json.loads(self.learning_history)
        print(date.today())
        correct_date = date.fromisoformat(current_learning_history["review_date"])
        # correct_date = current_learning_history["review_date"].replace("-", "/")
        # correct_date = datetime.strptime(current_learning_history["review_date"], "%y/%m/%d")
        smTwo = modify(smTwo, current_learning_history["quality"], current_learning_history["easiness"], current_learning_history["interval"], current_learning_history["repetitions"], correct_date) #input with the dbData values (easiness, history, etc. )
        print(smTwo.quality)
        #retrieve data, make a new SMTwo instance, and calculate new review date, etc.

    def calculate_next_review_day(self, newQuality, new_review_date=date.today()):
        smTwo = SMTwo()
        current_learning_history = json.loads(self.learning_history)
        smTwo.calc(newQuality, self.learning_historyeasiness, self.learning_history.interval, self.learning_history.repetitions, new_review_date)
        self.learning_history = smTwo.json()
        return smTwo.review_date

    def send_to_database(self):
        smTwo = first_review(3, date.today())
        print(self.learning_history)
        modify(smTwo, self.learning_history.quality, self.learning_history.easiness, self.learning_history.interval, self.learning_history.repetitions, self.learning_history.review_date)
        print(smTwo.json())
    
    def updateReviewDate(self, time, correct):
        #if correct button is pressed:
        if correct:
            if time > 10:
                self.review_date = self.calculate_next_review_day(3)
            elif time > 5:
                self.review_date = self.calculate_next_review_day(4)
            elif time < 5:
                self.review_date = self.calculate_next_review_day(5)
        else:
            if time > 10:
                self.review_date = self.calculate_next_review_day(0)
            elif time > 5:
                self.review_date = self.calculate_next_review_day(1)
            elif time < 5:
                self.review_date = self.calculate_next_review_day(2)
        #else if didn't know button is pressed:
            # flashcard.review_date = flashcard.calculate_next_review_day(0)

    '''def make_flashcard(self, front, back):
        if user decides to input string:
            whatever is in database front = front
        elif user decides to input picture:
            whatever is in database front = cv2.imread('pulled picture from frontend.png') #image type can be basically anything except .gif https://docs.opencv.org/master/d4/da8/group__imgcodecs.html
        
        if user decides to input string:
            #whatever is in database back = back
        elif user decides to input picture:
            whatever is in database back = cv2.imread('pulled picture from frontend.png')
        whatever is in database id = id + 1
        first_review(0, date.today())
        pass'''

    # def print(self):
    #     print('My id is {id}, from set {set}, my question is "{front}", my answer is "{back}".'.format(id = self.card_id, set = self.set_id, front = self.front, back = self.back))



