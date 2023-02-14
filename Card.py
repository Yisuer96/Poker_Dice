DECORS = ["C", "D", "H", "S"]
STATUS = ["in_deck", "in_hand", "on_table", "exposed", "discarded"]


def init_card(card):
    return Card(card.decor, card.point)


class Card:
    """
    Card abstraction
    """

    def __init__(self, decor=None, point=0):
        self.DECORS = DECORS
        self.cid = -1
        self.status = 'in_deck'
        self.decor = decor
        self.point = point
        self.attack = 0
        self.attack_shield = 0
        self.defend_block = 0
        self.defend_shield = 0
        self.spell = None
