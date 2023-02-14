import copy
import random
from Card import Card, DECORS
from Player import Player
from Solver import Solver
from Deck import Deck


def demo():
    deck = Deck()
    deck.shuffle()
    players = [Player() for _ in range(4)]
    solver = Solver(players, deck)
    f = open("result.txt", "w")
    solver.set_game()
    for i in range(10):
        solver.ph_start()
        solver.ph_draw()
        ran_place = random.randint(1, 6)
        decisions = [{'card': players[_].hand_card[ran_place % 3], 'form': ran_place % 2} for _ in range(4)]
        solver.ph_place(decisions)
        result = solver.ph_battle()
        f.write(f"=======T {i + 1}=======\n")
        f.write("player: card\tstatus\tattack\tshield\tblock\tdamage\n")
        for j in range(4):
            f.write(
                f"{'*' if solver.host == j else '-'} {j}: {decisions[j]['card'].decor} {decisions[j]['card'].point}\t{'Atk' if decisions[j]['form'] == 1 else 'Dfs'}\t{result['attacks'][j]}\t{decisions[j]['card'].attack_shield if decisions[j]['form'] == 1 else decisions[j]['card'].defend_shield}\t{result['blocks'][j]}\t{result['damages'][j]}\n")
        solver.ph_settle()
        solver.ph_end()
    f.close()


if __name__ == "__main__":
    demo()
