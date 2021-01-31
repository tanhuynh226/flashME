from supermemo2 import *
from datetime import date

#change to flash_id, set_id, user_id
class flashcard(object):
    def __init__(self, front, back, card_id, set_id, user_id):
        self.front = front
        self.back = back
        self.card_id = card_id
        self.set_id = set_id
        self.user_id = user_id
        self.knowledge_level = 0
        self.days_passed = 0
        self.last_reviewed = 0
        self.learning_history = None
        self.next_review = None
        #object.__init__(self, id, front, back)
        self.get_learning_history()
        

    def get_learning_history(self, dbData = None):
        #if db has no data, then assume we're making a new card 
        if(dbData == None):
            self.learning_history = first_review(3, date.today())
            self.next_review = self.learning_history.review_date
        #push back to db
        else:
            smTwo = SMTwo()
            smTwo.modify() #input with the dbData values (easiness, history, etc. )
        #retrieve data, make a new SMTwo instance, and calculate new review date, etc.

    def calculate_next_review_day(self, newQuality, new_review_date=date.today()):
        smTwo = SMTwo()
        smTwo.calc(newQuality, self.learning_history.easiness, self.learning_history.interval, self.learning_history.repetitions, new_review_date)
        self.learning_history = smTwo
        self.next_review = self.learning_history.review_date
        print(smTwo)
        pass

    def send_to_database(self):
        smTwo = first_review(3, date.today())
        print(self.learning_history)
        modify(smTwo, self.learning_history.quality, self.learning_history.easiness, self.learning_history.interval, self.learning_history.repetitions, self.learning_history.review_date)
        print(smTwo.json())

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

    def print(self):
        print('My id is {id}, from set {set}, my question is "{front}", my answer is "{back}".'.format(id = self.card_id, set = self.set_id, front = self.front, back = self.back))



