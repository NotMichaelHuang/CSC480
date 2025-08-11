import random


class Deck:
	def __init__(self):
		self.ranks = list(range(2, 15))
		self.suits = ["Clubs", "Spades", "Diamonds", "Hearts"]	
		self.created = False
		self.deck = []

	# Pre-shuffle it
	def create_deck(self):
		self.create = True
		self.deck = [(rank, suit) for rank in self.ranks for suit in self.suits]
		random.shuffle(self.deck)
		return self.deck

	def shuffle(self):
		if self.create:
			random.shuffle(self.deck)
			return self.deck
		return False

