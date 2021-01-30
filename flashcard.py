from supermemo2 import *
from datetime import date
from cv2 import *

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
        self.super_mem = SMTwo()
        self.next_review = first_review(0, date.today()).review_date
        #object.__init__(self, id, front, back)
        self.make_flashcard(front, back)
        

    def make_flashcard(self, front, back):
        #if user decides to input string:
            #whatever is in database front = front
        #elif user decides to input picture:
            #whatever is in database front = cv2.imread('pulled picture from frontend.png') #image type can be basically anything except .gif https://docs.opencv.org/master/d4/da8/group__imgcodecs.html
        
        #if user decides to input string:
            #whatever is in database back = back
        #elif user decides to input picture:
            #whatever is in database back = cv2.imread('pulled picture from frontend.png')
        #whatever is in database id = id + 1
        #first_review(0, date.today())
        pass
     
    def deleteFlashcard(self, card_id):
        #make delete request to db 
        pass

    def study(self, quality):
        self.super_mem.modify(quality)


    def print(self):
        print('My id is {id}, from set {set}, my question is "{front}", my answer is "{back}".'.format(id = self.card_id, set = self.set_id, front = self.front, back = self.back))

class flashcard_set():
    def __init__(self, set_id):
        super().__init__()
        self.flashcards = dict()
        self.set_id = set_id
        

    def add_flashcard(self, newFlashcard):
        self.flashcards[newFlashcard.card_id] = newFlashcard
        
        
        
    def update_flashcard(self, card_id, newData):
        self.flashcards[card_id] = newData
        next_review = SMTwo()
        next_review.calc()
    
    def remove_flashcard(self, card_id):
        del self.flashcards[card_id]
    
    #get the flashcards that are needed to complete
      #{'1': data, '2': data, }
    def to_do_flashcards(self):
        new_dict = dict()
        for id in self.flashcards:
            currentCard = self.flashcards[id]
            if(currentCard.next_review < date.today()):
                new_dict[id] = currentCard
        return new_dict
    

