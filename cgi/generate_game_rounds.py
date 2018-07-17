__author__ = 's1005849'

import json
import random

CardValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
CardIndices = [0, 1, 2, 3]


def generate_game_spec():
    values_same = True
    while values_same:
        game_cards = [random.choice(CardValues) for _ in range(4)]
        if (game_cards[0] * game_cards[1]) != (game_cards[2] * game_cards[3]):
            values_same = False
    flip_order = CardIndices[:]
    random.shuffle(flip_order)
    return {'gameCards': game_cards, 'flipOrder': flip_order}

def get_first_card_value(game_spec):
    return game_spec['gameCards'][game_spec['flipOrder'][0]]

def all_cards_exist(first_card_values):
    for i in range(1, 11):
        num = len([j for j in first_card_values if j == i])
        if num <= 2:
            return False
    return True

all_values_exist = False
while not all_values_exist:
    smallest_game_specs = [generate_game_spec() for a in range(50)]
    smallest_first_card_values = [get_first_card_value(spec) for spec in smallest_game_specs]
    biggest_game_specs = [generate_game_spec() for b in range(50)]
    biggest_first_card_values = [get_first_card_value(spec) for spec in biggest_game_specs]
    all_values_exist = all_cards_exist(smallest_first_card_values) and all_cards_exist(biggest_first_card_values)

print 'Smallest Counts'
for i in range(1, 11):
    print 'Card %s: %s' % (i, len([j for j in smallest_first_card_values if j == i]))

print
print 'Biggest Counts'
for i in range(1, 11):
    print 'Card %s: %s' % (i, len([j for j in biggest_first_card_values if j == i]))
game_rounds = {'smallest': smallest_game_specs,
               'biggest': biggest_game_specs}
with open('games.json', 'w') as f:
    json.dump(game_rounds, f)






