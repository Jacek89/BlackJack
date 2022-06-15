from itertools import repeat
import random


class Card:
    num_of_decks = 1
    deck = []

    def __init__(self, rank, color, points):
        self.rank = rank
        self.color = color
        self.points = points

        Card.deck.extend(repeat(self, self.num_of_decks))

    @classmethod
    def creating(cls, num):
        Card.num_of_decks = num
        Card.deck.clear()
        colors = ["Spades", "Hearts", "Diamonds", "Clubs"]
        rank_dict = {
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
            "Six": 6,
            "Seven": 7,
            "Eight": 8,
            "Nine": 9,
            "Ten": 10,
            "Jack": 10,
            "Queen": 10,
            "King": 10,
            "Ace": 11
        }
        for color in colors:
            for rank in rank_dict:
                Card(rank, color, rank_dict[rank])

    @staticmethod
    def shuffle_deck():
        random.shuffle(Card.deck)

    def __repr__(self):
        return f"Card('{self.rank}', '{self.color}', {self.points})"

    def __str__(self):
        return f"{self.rank} of {self.color}"
