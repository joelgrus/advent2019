from typing import List

Deck = List[int]

def deal_into_new_stack(deck: Deck) -> Deck:
    return list(reversed(deck))

def cut(deck: Deck, n: int) -> Deck:
    num_cards = len(deck)
    n = n % num_cards
    return deck[n:] + deck[:n]

def with_increment(deck: Deck, n: int) -> Deck:
    result = deck[:]
    num_cards = len(deck)
    pos = 0
    for card in deck:
        result[pos] = card
        pos = (pos + n) % num_cards

    return result

TEST_DECK = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
assert deal_into_new_stack(TEST_DECK) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
assert cut(TEST_DECK, 6) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
assert cut(TEST_DECK, -4) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
assert with_increment(TEST_DECK, 3) == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]

deck = list(range(10007))

with open('day22.txt') as f:
    for line in f:
        line = line.strip()
        if line == "deal into new stack":
            deck = deal_into_new_stack(deck)
        elif line.startswith("cut"):
            n = int(line.split()[-1])
            deck = cut(deck, n)
        elif line.startswith("deal with increment"):
            n = int(line.split()[-1])
            deck = with_increment(deck, n)

