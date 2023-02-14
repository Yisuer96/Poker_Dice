from Deck import Deck


class Player:
    def __init__(self, deck=Deck()):
        self.character = None
        self.health = 0
        self.skill = None
        self.deck = deck
        self.hand_card = []
