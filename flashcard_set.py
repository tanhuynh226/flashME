from flashcard import *
from supermemo2 import *

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
    