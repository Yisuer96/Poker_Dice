# not a phase, occurs during battle section
from Deck import Deck
from Player import Player
from Card import Card, init_card


class Solver:
    """
    The Solver of battle
    """

    def __init__(self, players=[Player() for _ in range(4)], deck=Deck()):
        self.n = 4
        self.host = 0
        self.deck = deck
        self.operators = players
        self.game_decisions = []
        self.battle_results = []
        self.board_cards = []
        pass

    def solve(self, table):
        pass

    def find_order(self, turn):
        return (turn + self.host) % self.n

    def find_operator(self, turn):
        return self.operators[(turn + self.host) % self.n]

    def set_game(self):
        for i in range(2):
            self.ph_draw()

    def ph_start(self):
        for p in range(self.n):
            operator = self.find_operator(p)
            o = self.find_order(p)
            if operator.skill and 'start' in operator.skill['phase']:
                operator.skill['launch'](self)

    def ph_draw(self):
        for p in range(self.n):
            operator = self.find_operator(p)
            if operator.skill and 'draw' in operator.skill['phase']:
                operator.skill['launch'](self)
            card = self.deck.draw()
            card = operator.deck.ss[card.decor][card.point]
            if card.spell and 'draw' in card.spell['phase']:
                card.spell['launch'](self)
            card.status = 'in_hand'
            operator.hand_card.append(card)

    def ph_place(self, decisions):
        for p in range(self.n):
            operator = self.find_operator(p)
            o = self.find_order(p)
            # noinspection PyBroadException
            try:
                operator.hand_card.remove(decisions[o]['card'])
            except Exception as e:
                print(e)
            if operator.skill and 'place' in operator.skill['phase']:
                operator.skill['launch'](self)
            card = decisions[o]
            if card['card'].spell and 'place' in card['card'].spell['phase']:
                card['card'].spell['launch'](self)
            card['card'].status = 'on_table'
            self.board_cards.append(card)
        self.game_decisions.append(decisions)

    def ph_battle(self):
        damages = [0 for _ in range(4)]
        attacks = [0 for _ in range(4)]
        blocks = [0 for _ in range(4)]
        shields = [0 for _ in range(4)]
        for p in range(self.n):
            pos = (p + self.host) % self.n
            operator = self.find_operator(p)
            o = self.find_order(p)
            card = self.game_decisions[-1][o]
            if card['card'].status == 'on_table':
                if operator.skill and 'display' in operator.skill['phase']:
                    operator.skill['launch'](self)
                if card['card'].spell and 'display' in card['card'].spell['phase']:
                    card['card'].spell['launch'](self)
                if card['form'] == 1:
                    attacks[pos] += card['card'].attack
                    shields[pos] += card['card'].attack_shield
                elif card['form'] == 2:
                    shields[pos] += card['card'].defend_shield
                    blocks[pos] += card['card'].defend_block
                card['card'].status = 'exposed'
            if card['form'] == 1:
                for t in range(1, self.n):
                    d_pos = (pos + t) % 4
                    if operator.skill and 'attack' in operator.skill['phase']:
                        operator.skill['launch'](self)
                    if card['card'].spell and 'attack' in card['card'].spell['phase']:
                        card['card'].spell['launch'](self)
                    if self.operators[d_pos].skill and 'defend' in operator.skill['phase']:
                        operator.skill['launch'](self)
                    def_card = self.game_decisions[-1][d_pos]
                    if operator.skill and 'defense' in operator.skill['phase']:
                        operator.skill['launch'](self)
                    if def_card['card'].status == 'on_table':
                        if def_card['card'].spell and 'display' in def_card['card'].spell['phase']:
                            def_card['card'].spell['launch'](self)
                        if def_card['form'] == 1:
                            attacks[d_pos] += def_card['card'].attack
                            shields[d_pos] += def_card['card'].attack_shield
                        elif def_card['form'] == 2:
                            shields[d_pos] += def_card['card'].defend_shield
                            blocks[d_pos] += def_card['card'].defend_block
                        def_card['card'].status = 'exposed'
                    if def_card['card'].spell and 'defense' in def_card['card'].spell['phase']:
                        def_card['card'].spell['launch'](self)
                    damage = attacks[pos]
                    if def_card['form'] == 1:
                        if attacks[pos] > attacks[d_pos]:
                            damage += 1
                        elif attacks[pos] < attacks[d_pos]:
                            damage = max(damage - 1, 0)
                        damage = max(damage - blocks[d_pos], 0)
                        rest_shield = shields[d_pos] - damage
                        shields[d_pos] = max(rest_shield, 0)
                        damage = max(-rest_shield, 0)
                        damages[d_pos] += damage
                pass
            elif card['form'] == 2:
                pass
            else:
                pass
        result = {
            "damages": damages,
            "attacks": attacks,
            "shields": shields,
            "blocks": blocks
        }
        self.battle_results.append(result)
        return result

    def ph_settle(self):
        for p in range(self.n):
            operator = self.find_operator(p)
            if operator.skill and 'settle' in operator.skill['phase']:
                operator.skill['launch'](self, self.battle_results[-1])
        pass

    def ph_end(self):
        for p in range(self.n):
            pos = (p + self.host) % self.n
            operator = self.find_operator(p)
            if operator.skill and 'end' in operator.skill['phase']:
                operator.skill['launch'](self)
            i_card = init_card(self.board_cards[pos]['card'])
            self.deck.discard(i_card)
        self.host = (self.host + 1) % 4
        pass
