from Card import Card, DECORS
import random
import copy


def generate_basic_card_list():
    """
    generate basic cards with unmodified attack and defense
    """
    card_list = []
    cid = 0
    for decor in DECORS:
        for point in range(1, 14):
            card = Card()
            card.cid = cid
            card.decor = decor
            card.point = point
            card.attack = point
            card.attack_shield = 14 - point
            card.defend_block = (16 - point) // 2
            card.defend_shield = point % 2
            card_list.append(card)
            cid += 1
    return card_list


class Deck:
    """
    A set of cards
    """

    def __init__(self, card_list: list = None):
        if card_list is None:
            card_list = generate_basic_card_list()
        self.card_list = card_list
        self.cards = copy.deepcopy(card_list)
        self.discard_pile = []
        random.shuffle(self.cards)
        self.ss = {}  # search struct

        self._build_basic_search_struct(card_list)

    def _build_basic_search_struct(self, deck: list):
        assert len(deck) == 52
        ss = {}  # search struct
        for decor in DECORS:
            decor_ss = {}
            for i in range(1, 14):
                decor_ss[i] = None
            ss[decor] = decor_ss
        # validate card_list
        for card in deck:
            if ss[card.decor][card.point] is None:
                ss[card.decor][card.point] = card
        self.ss = ss
        return

    def shuffle(self, discard_pile: list = []):
        self.cards.extend(discard_pile)
        random.shuffle(self.cards)

    def add_cards(self, cards):
        self.cards.append(cards)

    def draw(self):
        if not self.cards:
            self.shuffle()
        return self.cards.pop()

    def discard(self, card):
        self.discard_pile.append(card)
        card.status = 'discarded'

    def find(self):
        pass
