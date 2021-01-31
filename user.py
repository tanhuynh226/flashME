from flashcard import *



class user:
    def __init__(self, user_id, flashcard_sets=dict()):
        super().__init__()
        self.flashcard_sets = flashcard_sets #will be filled with ids
        self.user_id = user_id
    
    def add_flashcard_set(self, newSet):
        print(newSet)
        self.flashcard_sets[newSet.set_id] = newSet

    def get_flashcards_to_do(self, set_id):
        print("The current flashcards you need to study are: \n")
        cardsToDo = self.flashcard_sets[set_id].to_do_flashcards()
        for card_id in cardsToDo:
            cardsToDo[card_id].print()
    
    def get_review_dates(self, set_id):
        print("The current review dates are: \n")
        cardsToDo = self.flashcard_sets[set_id].flashcards
        for card_id in cardsToDo:
            print(cardsToDo[card_id].next_review)



